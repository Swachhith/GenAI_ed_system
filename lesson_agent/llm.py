"""Thin model-provider layer.

Every node in the graph talks to an `LLM` with two methods: `text()` for free-form
writing and `structured()` for schema-validated JSON (judge verdicts, revisions).
Keeping the interface this small is what makes the provider swappable and lets the
tests drive the whole graph with a scripted fake.

Works with any chat model:
  * anthropic - Claude via the official SDK (native structured output)
  * gemini    - Gemini / Gemma via google-genai (native JSON schema where supported)
  * openai    - any OpenAI-compatible endpoint: OpenAI, OpenRouter, Groq, Together,
                DeepSeek, Ollama, LM Studio, vLLM... (set OPENAI_BASE_URL)
If a model has no native structured output (or rejects it), `structured()` falls back
to asking for JSON in plain text, validating it against the schema, and sending the
validation error back once for a repair. So small and open models work too.
"""
from __future__ import annotations

import json
import os
import re
import time
from typing import Callable, Literal, Protocol, TypeVar

from pydantic import BaseModel, ValidationError

from .config import Settings

T = TypeVar("T", bound=BaseModel)
Role = Literal["generator", "evaluator"]


class LLMError(RuntimeError):
    pass


class LLM(Protocol):
    def text(self, system: str, prompt: str, *, role: Role) -> str: ...
    def structured(self, system: str, prompt: str, schema: type[T], *, role: Role) -> T: ...


# ---- JSON-in-text fallback (provider independent) ---------------------------------------

def extract_json(raw: str) -> str:
    """Pull the JSON object out of a reply that may wrap it in prose or ``` fences."""
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", raw, re.S)
    if fenced:
        return fenced.group(1)
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end <= start:
        raise LLMError(f"No JSON object in model reply: {raw[:200]!r}")
    return raw[start:end + 1]


def json_instructions(schema: type[BaseModel]) -> str:
    return ("\n\nReply with ONE JSON object only, no prose and no code fences. It must match this JSON "
            "schema exactly (all required fields present, correct types):\n"
            + json.dumps(schema.model_json_schema(), ensure_ascii=False))


def structured_via_text(text_fn: Callable[[str, str], str], system: str, prompt: str, schema: type[T]) -> T:
    """Ask for JSON as text, validate, and give the model one chance to repair its output."""
    raw = text_fn(system, prompt + json_instructions(schema))
    try:
        return schema.model_validate_json(extract_json(raw))
    except (LLMError, ValidationError) as e:
        repair = (f"{prompt}{json_instructions(schema)}\n\nYour previous reply was invalid:\n{str(e)[:1500]}\n"
                  f"Previous reply:\n{raw[:4000]}\n\nReturn the corrected JSON object only.")
        raw = text_fn(system, repair)
        try:
            return schema.model_validate_json(extract_json(raw))
        except (LLMError, ValidationError) as e2:
            raise LLMError(f"Structured output invalid after repair: {str(e2)[:300]}") from e2


# ---- providers -------------------------------------------------------------------------

class AnthropicLLM:
    """Claude via the official SDK."""

    # Writing is mostly fluent prose; judging needs careful reading, so it gets more effort.
    _EFFORT = {"generator": "medium", "evaluator": "high"}

    def __init__(self, settings: Settings):
        import anthropic

        self._anthropic = anthropic
        self._client = anthropic.Anthropic(max_retries=4)
        self._models = {"generator": settings.generator_model, "evaluator": settings.evaluator_model}
        self._fallbacks = settings.anthropic_fallbacks != "off"
        self._extras = True  # effort + fallbacks; dropped once if an older model rejects them

    def _kwargs(self, system: str, prompt: str, role: Role) -> dict:
        kw = dict(model=self._models[role], max_tokens=16000, system=system,
                  messages=[{"role": "user", "content": prompt}])
        if self._extras:
            kw["output_config"] = {"effort": self._EFFORT[role]}
            if self._fallbacks:
                # On a (rare) policy decline, the API re-runs the request on a fallback model.
                kw.update(betas=["server-side-fallback-2026-07-01"], fallbacks="default")
        return kw

    def _call(self, method, **extra):
        try:
            return method(**extra)
        except self._anthropic.BadRequestError as e:
            if not self._extras:
                raise LLMError(f"Anthropic API error: {e}") from e
            self._extras = False  # older Claude models: retry without effort/fallbacks
            extra = {k: v for k, v in extra.items() if k not in ("output_config", "betas", "fallbacks")}
            return method(**extra)

    @staticmethod
    def _check(resp) -> None:
        if resp.stop_reason == "refusal":
            raise LLMError(f"Model refused the request: {getattr(resp, 'stop_details', None)}")
        if resp.stop_reason == "max_tokens":
            raise LLMError("Model output was truncated (max_tokens).")

    def text(self, system: str, prompt: str, *, role: Role) -> str:
        resp = self._call(self._client.beta.messages.create, **self._kwargs(system, prompt, role))
        self._check(resp)
        return "".join(b.text for b in resp.content if b.type == "text").strip()

    def structured(self, system: str, prompt: str, schema: type[T], *, role: Role) -> T:
        try:
            resp = self._call(self._client.beta.messages.parse, **self._kwargs(system, prompt, role),
                              output_format=schema)
            self._check(resp)
            if resp.parsed_output is not None:
                return resp.parsed_output
        except (LLMError, ValidationError, self._anthropic.BadRequestError):
            pass
        return structured_via_text(lambda s, p: self.text(s, p, role=role), system, prompt, schema)


class GeminiLLM:
    """Google Gemini (and Gemma) via google-genai. Has a free tier."""

    _MAX_RETRIES = 6

    def __init__(self, settings: Settings):
        from google import genai

        self._client = genai.Client()
        self._models = {"generator": settings.generator_model, "evaluator": settings.evaluator_model}
        # Some models (e.g. Gemma) reject system instructions or JSON mode; learned on first 400.
        self._no_system: set[str] = set()
        self._no_json: set[str] = set()

    def _generate(self, role: Role, system: str, prompt: str, schema=None):
        """generate_content with retries on rate limits (429) and overload (5xx).

        Free-tier keys allow ~15 requests/minute, and one run makes ~20 calls, so waiting
        out a 429 (Google says how long, in RetryInfo) is the normal path, not an edge case.
        """
        from google.genai import errors, types

        model = self._models[role]
        for attempt in range(self._MAX_RETRIES + 1):
            # No temperature override: Gemini 3+ models are tuned for their default sampling settings.
            kw, contents = {}, prompt
            if model in self._no_system:
                contents = f"{system}\n\n{prompt}"
            else:
                kw["system_instruction"] = system
            if schema is not None:
                kw.update(response_mime_type="application/json", response_schema=schema)
            try:
                return self._client.models.generate_content(
                    model=model, contents=contents, config=types.GenerateContentConfig(**kw))
            except errors.APIError as e:
                msg = str(e).lower()
                if e.code == 400 and "instruction" in msg and model not in self._no_system:
                    self._no_system.add(model)
                    continue
                if e.code == 400 and schema is not None and ("json" in msg or "schema" in msg):
                    self._no_json.add(model)
                    raise LLMError("JSON mode not supported") from e
                retryable = e.code == 429 or (e.code or 0) >= 500
                if not retryable or attempt == self._MAX_RETRIES:
                    raise LLMError(f"Gemini API error {e.code}: {e.message}") from e
                m = re.search(r"retry in ([\d.]+)s", str(e)) or re.search(r"'retryDelay': '(\d+)s'", str(e))
                delay = float(m.group(1)) + 1 if m else min(60, 5 * 2 ** attempt)
                print(f"    (Gemini {e.code}: waiting {delay:.0f}s before retrying)", flush=True)
                time.sleep(delay)
        raise LLMError("Gemini: retries exhausted")

    def text(self, system: str, prompt: str, *, role: Role) -> str:
        resp = self._generate(role, system, prompt)
        if not resp.text:
            raise LLMError("Gemini returned an empty response.")
        return resp.text.strip()

    def structured(self, system: str, prompt: str, schema: type[T], *, role: Role) -> T:
        if self._models[role] not in self._no_json:
            try:
                resp = self._generate(role, system, prompt, schema)
                if isinstance(resp.parsed, schema):
                    return resp.parsed
                if resp.text:
                    return schema.model_validate_json(resp.text)
            except (ValidationError, LLMError) as e:
                if "API error" in str(e):
                    raise
        return structured_via_text(lambda s, p: self.text(s, p, role=role), system, prompt, schema)


class OpenAICompatLLM:
    """Any OpenAI-compatible chat endpoint.

    Examples (.env):
      OpenAI      OPENAI_API_KEY=sk-...
      OpenRouter  OPENAI_BASE_URL=https://openrouter.ai/api/v1   OPENAI_API_KEY=sk-or-...
      Groq        OPENAI_BASE_URL=https://api.groq.com/openai/v1  OPENAI_API_KEY=gsk_...
      Ollama      OPENAI_BASE_URL=http://localhost:11434/v1        OPENAI_API_KEY=ollama
    """

    def __init__(self, settings: Settings):
        import openai

        self._openai = openai
        self._client = openai.OpenAI(base_url=os.getenv("OPENAI_BASE_URL") or None,
                                     api_key=os.getenv("OPENAI_API_KEY") or "not-needed", max_retries=6)
        self._models = {"generator": settings.generator_model, "evaluator": settings.evaluator_model}
        self._native_json = os.getenv("OPENAI_STRUCTURED", "auto") != "text"

    def text(self, system: str, prompt: str, *, role: Role) -> str:
        try:
            resp = self._client.chat.completions.create(
                model=self._models[role],
                messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}])
        except self._openai.APIError as e:
            raise LLMError(f"OpenAI-compatible API error: {e}") from e
        choice = resp.choices[0]
        if choice.finish_reason == "length":
            raise LLMError("Model output was truncated (length).")
        if not choice.message.content:
            raise LLMError("Model returned an empty response.")
        return choice.message.content.strip()

    def structured(self, system: str, prompt: str, schema: type[T], *, role: Role) -> T:
        if self._native_json:
            try:
                resp = self._client.chat.completions.parse(
                    model=self._models[role], response_format=schema,
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}])
                if resp.choices[0].message.parsed is not None:
                    return resp.choices[0].message.parsed
            except (self._openai.BadRequestError, self._openai.UnprocessableEntityError,
                    self._openai.NotFoundError):
                self._native_json = False  # endpoint/model has no json_schema support
            except (ValidationError, self._openai.LengthFinishReasonError, self._openai.ContentFilterFinishReasonError):
                pass
        return structured_via_text(lambda s, p: self.text(s, p, role=role), system, prompt, schema)


_BACKENDS = {"anthropic": AnthropicLLM, "gemini": GeminiLLM, "openai": OpenAICompatLLM}


class RoutedLLM:
    """Sends each role to its own provider (e.g. writer on Gemini, judge on Claude)."""

    def __init__(self, backends: dict[str, LLM]):
        self._backends = backends

    def text(self, system: str, prompt: str, *, role: Role) -> str:
        return self._backends[role].text(system, prompt, role=role)

    def structured(self, system: str, prompt: str, schema: type[T], *, role: Role) -> T:
        return self._backends[role].structured(system, prompt, schema, role=role)


def make_llm(settings: Settings) -> LLM:
    gen, ev = settings.generator_provider, settings.evaluator_provider
    if gen == ev:
        return _BACKENDS[gen](settings)
    return RoutedLLM({"generator": _BACKENDS[gen](settings), "evaluator": _BACKENDS[ev](settings)})

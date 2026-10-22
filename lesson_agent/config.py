"""Runtime settings, read once from environment / .env."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

_DEFAULT_MODELS = {
    # provider: (generator, evaluator)
    "anthropic": ("claude-sonnet-5-5", "claude-opus-5-5"),
    "gemini": ("gemini-2.5-flash", "gemini-2.5-pro"),
    # Any OpenAI-compatible endpoint (OpenAI, OpenRouter, Groq, Together, DeepSeek, Ollama,
    # LM Studio, vLLM...). There is no sensible default model across all of them, so you name it.
    "openai": ("", ""),
}
PROVIDERS = tuple(_DEFAULT_MODELS)


def split_model(spec: str, default_provider: str) -> tuple[str, str]:
    """'gemini:gemini-3.5-flash' -> ('gemini', 'gemini-3.5-flash'); a bare name keeps the default provider.

    Lets the writer and the judge come from different providers (e.g. a cheap open model
    writes, Claude judges), which also avoids a model grading its own work.
    """
    head, sep, tail = spec.partition(":")
    if sep and head.lower() in _DEFAULT_MODELS:
        return head.lower(), tail
    return default_provider, spec


@dataclass
class Settings:
    provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "anthropic").lower())
    generator_model: str = ""
    evaluator_model: str = ""
    generator_provider: str = ""
    evaluator_provider: str = ""
    # Max regeneration attempts after the first draft (assessment: 1-2). Guarantees termination.
    max_retries: int = field(default_factory=lambda: int(os.getenv("MAX_RETRIES", "2")))
    # Parallel judge calls. Lower this on free-tier keys with tight rate limits.
    eval_concurrency: int = field(default_factory=lambda: int(os.getenv("EVAL_CONCURRENCY", "4")))
    # A check must fail this many times (across all runs) before the learner writes a guideline for it.
    learn_min_failures: int = field(default_factory=lambda: int(os.getenv("LEARN_MIN_FAILURES", "2")))
    # Independent judge samples per LLM check, combined by majority per item (ties fail).
    # 1 is fine for strong judges; 3 steadies small or noisy models at 3x the judge cost.
    judge_votes: int = field(default_factory=lambda: int(os.getenv("JUDGE_VOTES", "1")))
    max_guidelines: int = 10
    # Web research (Tavily): fresh facts + learning resources. On whenever a key is set.
    tavily_api_key: str = field(default_factory=lambda: os.getenv("TAVILY_API_KEY", ""))
    web_research: bool = field(default_factory=lambda: os.getenv("WEB_RESEARCH", "auto").lower() != "off")
    # Live-check every resource link before the writer may use it (off only for offline tests).
    verify_links: bool = field(default_factory=lambda: os.getenv("VERIFY_LINKS", "on").lower() != "off")
    # Claude only: server-side refusal fallback ("default" or "off").
    anthropic_fallbacks: str = field(default_factory=lambda: os.getenv("ANTHROPIC_FALLBACKS", "default"))
    memory_path: Path = field(default_factory=lambda: Path(os.getenv("MEMORY_PATH", ROOT / "memory" / "memory.json")))
    runs_dir: Path = ROOT / "runs"
    output_dir: Path = ROOT / "output"
    knowledge_dir: Path = ROOT / "knowledge"

    def __post_init__(self) -> None:
        if self.provider not in _DEFAULT_MODELS:
            raise ValueError(f"LLM_PROVIDER must be one of {sorted(_DEFAULT_MODELS)}, got {self.provider!r}")
        gen, ev = _DEFAULT_MODELS[self.provider]
        for role, default in (("generator", gen), ("evaluator", ev)):
            spec = getattr(self, f"{role}_model") or os.getenv(f"{role.upper()}_MODEL", default)
            provider, model = split_model(spec, getattr(self, f"{role}_provider") or self.provider)
            if not model:
                raise ValueError(f"Set {role.upper()}_MODEL (provider {provider!r} has no default model).")
            setattr(self, f"{role}_provider", provider)
            setattr(self, f"{role}_model", model)
        self.max_retries = max(0, min(self.max_retries, 3))
        self.judge_votes = max(1, min(self.judge_votes, 5))
        self.web_research = self.web_research and bool(self.tavily_api_key)

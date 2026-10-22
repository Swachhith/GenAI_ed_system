"""Reference sheets: the ONLY place topic knowledge lives.

The writer template, the rubric and the defect injections are topic-free; everything they
need to know about a topic comes from its reference sheet:

  short_name, prerequisite, must_cover, facts, misconceptions, jargon, resources

A curated sheet (knowledge/*.json) is used when the topic matches one of its aliases (whole
words, so "Paragraphs" does not match "rag"). For any other topic the model drafts a sheet,
grounded in web search results when internet access is configured; it is cached and marked
trust="generated" so the rejection log makes clear the grounding is weaker.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .llm import LLM
from .prompts import REFERENCE_BUILDER_SYSTEM
from .schemas import ReferenceSheet


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def matches(topic: str, aliases: list[str]) -> bool:
    return any(re.search(rf"(?<![a-z0-9]){re.escape(a.lower())}(?![a-z0-9])", topic.lower()) for a in aliases)


def load_reference(topic: str, knowledge_dir: Path, llm: LLM | None, settings=None, log=print) -> dict:
    for path in sorted(knowledge_dir.glob("*.json")):
        ref = json.loads(path.read_text(encoding="utf-8"))
        if matches(topic, ref.get("aliases", [])):
            return {**ref, "path": str(path)}

    cache = knowledge_dir / "generated" / f"{_slug(topic)}.json"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    if llm is None:
        raise FileNotFoundError(f"No reference sheet for {topic!r} and no LLM to build one.")

    grounding = ""
    if settings is not None and settings.web_research:
        from .web import search
        results = search(settings, f"{topic} explained for beginners", max_results=6)
        if results:
            grounding = "\n\nWeb search results to ground the sheet:\n" + "\n\n".join(
                f"[{r['url']}] {r['title']}\n{r.get('content', '')[:700]}" for r in results)
    log(f"[prepare] no curated sheet for {topic!r}: drafting one"
        + (" from web search results" if grounding else " from the model's own knowledge"))
    sheet = llm.structured(REFERENCE_BUILDER_SYSTEM,
                           f"Topic: {topic}\nAudience: absolute beginners (class-12 graduates in India).{grounding}",
                           ReferenceSheet, role="evaluator")
    ref = {"topic": topic, "aliases": [topic.lower()], "trust": "generated" + ("+web" if grounding else ""),
           **sheet.model_dump(), "resources": [], "path": str(cache)}
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(ref, indent=2, ensure_ascii=False), encoding="utf-8")
    return ref

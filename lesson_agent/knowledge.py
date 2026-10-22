"""Reference sheets that ground the accuracy and coverage checks.

A curated sheet (knowledge/*.json) is used when the topic matches one. For any other
topic the model drafts a sheet once; it is cached and marked trust="generated" so the
rejection log makes clear the grounding is weaker.
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


def load_reference(topic: str, knowledge_dir: Path, llm: LLM | None) -> dict:
    t = topic.lower()
    for path in sorted(knowledge_dir.glob("*.json")):
        ref = json.loads(path.read_text(encoding="utf-8"))
        if any(a in t for a in ref.get("aliases", [])):
            return {**ref, "path": str(path)}

    cache = knowledge_dir / "generated" / f"{_slug(topic)}.json"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    if llm is None:
        raise FileNotFoundError(f"No reference sheet for {topic!r} and no LLM to build one.")
    sheet = llm.structured(REFERENCE_BUILDER_SYSTEM,
                           f"Topic: {topic}\nAudience: absolute beginners. Give 6-9 must-cover points, "
                           "10-15 facts, 4-7 common misconceptions, and the technical terms a lesson would use.",
                           ReferenceSheet, role="evaluator")
    ref = {"topic": topic, "aliases": [t], "trust": "generated", **sheet.model_dump(), "path": str(cache)}
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(ref, indent=2, ensure_ascii=False), encoding="utf-8")
    return ref

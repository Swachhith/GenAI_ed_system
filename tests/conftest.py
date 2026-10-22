"""Shared test fixtures. Every lesson-level test runs once per topic in tests/fixtures/topics/.

The topics are deliberately different (RAG, and LLMs as a stand-in for any other subject),
so a test can only pass if the template, rubric, injections and graph are topic-general.
Adding a topic = adding a folder with lesson.md (+ reference.json if not curated).
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import pytest

from lesson_agent.config import ROOT, Settings
from lesson_agent.inject import describe
from lesson_agent.schemas import GuidelineDecision, ItemCheck, JudgeVerdict, NewCheck, Revision

FIXTURES = Path(__file__).parent / "fixtures" / "topics"


@dataclass
class Topic:
    key: str
    topic: str
    lesson: str
    reference: dict
    signature: list[str]  # words that belong to THIS topic only; they must never appear in shared code text

    @property
    def proof(self) -> str:
        return self.lesson.splitlines()[0].lstrip("# ")  # a quote that really is in the lesson


def _load(key: str, signature: list[str]) -> Topic:
    folder = FIXTURES / key
    ref_file = folder / "reference.json"
    ref = json.loads((ref_file if ref_file.exists() else ROOT / "knowledge" / f"{key}.json").read_text(encoding="utf-8"))
    return Topic(key, ref["topic"], (folder / "lesson.md").read_text(encoding="utf-8"), ref, signature)


TOPICS = [
    _load("rag", ["RAG", "retrieval", "chunk", "embedding", "vector"]),
    _load("llm", ["LLM", "large language model", "token", "parameter"]),
]


@pytest.fixture(params=TOPICS, ids=[t.key for t in TOPICS])
def topic(request) -> Topic:
    return request.param


def requested_items(prompt: str) -> list[str]:
    """The numbered ITEMS TO VERIFY list from a judge prompt."""
    block = prompt.split("ITEMS TO VERIFY", 1)[1].split("\n\n", 1)[0]
    return re.findall(r"^\d+\. (.*)$", block, flags=re.M)


class FakeLLM:
    """Writes the topic's known-good lesson. Judges FAIL accuracy iff the planted misconception
    is present; `stubborn=True` makes accuracy fail forever, to test the retry budget."""

    def __init__(self, t: Topic, stubborn: bool = False):
        self.t, self.stubborn = t, stubborn
        self.planted = describe("factual", t.lesson, t.reference)
        self.calls = {"text": 0, "revise": 0, "judge": 0, "learn": 0}

    def text(self, system, prompt, *, role):
        self.calls["text"] += 1
        return self.t.lesson

    def structured(self, system, prompt, schema, *, role):
        if schema is JudgeVerdict:
            self.calls["judge"] += 1
            items = [ItemCheck(item=i, met=True, quote=self.t.proof) for i in requested_items(prompt)]
            planted = self.planted in prompt.split("LESSON:", 1)[-1]
            if "CHECK L1_ACCURACY" in prompt and (self.stubborn or planted):
                items[0] = ItemCheck(item=items[0].item, met=False, quote=self.planted if planted else "")
                return JudgeVerdict(items=items, reasoning="States a misconception.", verdict="FAIL",
                                    evidence=[], fix="Remove the false claim.")
            return JudgeVerdict(items=items, reasoning="Requirement met.", verdict="PASS", evidence=[], fix="")
        if schema is Revision:
            self.calls["revise"] += 1
            lesson = prompt.split("CURRENT LESSON:\n", 1)[1].replace(self.planted, "")
            return Revision(lesson_markdown=lesson, change_log=[{"check_id": "L1_ACCURACY", "change": "Removed false claim."}])
        if schema is GuidelineDecision:
            self.calls["learn"] += 1
            return GuidelineDecision(action="new", duplicate_of="",
                                     guideline="Never state a misconception from the reference sheet, even softened.")
        if schema is NewCheck:
            return NewCheck(name="No English idioms", dimension="beginner-friendly language",
                            criterion="The lesson contains no English idioms.")
        raise AssertionError(f"unexpected schema {schema}")


@pytest.fixture
def settings(tmp_path):
    s = Settings(provider="anthropic", generator_model="fake-gen", evaluator_model="fake-eval")
    s.runs_dir, s.output_dir = tmp_path / "runs", tmp_path / "output"
    s.memory_path = tmp_path / "memory.json"
    # A knowledge dir holding every test topic's sheet, so load_reference finds each by alias.
    s.knowledge_dir = tmp_path / "knowledge"
    s.knowledge_dir.mkdir()
    for t in TOPICS:
        (s.knowledge_dir / f"{t.key}.json").write_text(json.dumps(t.reference), encoding="utf-8")
    s.max_retries, s.learn_min_failures = 2, 2
    s.web_research, s.verify_links = False, False  # offline: no Tavily, no link checks
    return s


def quiet(_):
    pass



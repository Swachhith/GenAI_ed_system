"""Offline tests: a scripted fake LLM drives the real graph, rules, memory and reports.

These prove the control logic (routing, termination, regeneration strategy, memory,
learning, injection detection). The quality of the real model's judgments is shown by
the live runs in runs/ and the demo, not here.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from lesson_agent import rules
from lesson_agent.config import ROOT, Settings
from lesson_agent.graph import run
from lesson_agent.inject import INJECTIONS, inject
from lesson_agent.memory import Memory
from lesson_agent.schemas import GuidelineDecision, ItemCheck, JudgeVerdict, NewCheck, Revision

GOOD = (Path(__file__).parent / "fixtures" / "good_lesson.md").read_text(encoding="utf-8")
FACTUAL_ERROR = INJECTIONS["factual"]["text"]


def requested_items(prompt: str) -> list[str]:
    """The numbered ITEMS TO VERIFY list from a judge prompt."""
    block = prompt.split("ITEMS TO VERIFY", 1)[1].split("\n\n", 1)[0]
    return re.findall(r"^\d+\. (.*)$", block, flags=re.M)


PROOF = GOOD.splitlines()[0].lstrip("# ")  # a quote that really is in the lesson


class FakeLLM:
    """Judges FAIL the accuracy check iff the planted misconception is present.
    `stubborn=True` makes accuracy fail forever, to test the retry budget."""

    def __init__(self, stubborn: bool = False):
        self.stubborn = stubborn
        self.calls = {"text": 0, "revise": 0, "judge": 0, "learn": 0}

    def text(self, system, prompt, *, role):
        self.calls["text"] += 1
        return GOOD

    def structured(self, system, prompt, schema, *, role):
        if schema is JudgeVerdict:
            self.calls["judge"] += 1
            items = [ItemCheck(item=t, met=True, quote=PROOF) for t in requested_items(prompt)]
            planted = "retraining the AI model" in prompt
            if "CHECK L1_ACCURACY" in prompt and (self.stubborn or planted):
                items[0] = ItemCheck(item=items[0].item, met=False, quote=FACTUAL_ERROR if planted else "")
                return JudgeVerdict(items=items, reasoning="States RAG retrains the model.", verdict="FAIL",
                                    evidence=[], fix="Remove the claim; RAG adds retrieved text to the prompt.")
            return JudgeVerdict(items=items, reasoning="Requirement met.", verdict="PASS", evidence=[], fix="")
        if schema is Revision:
            self.calls["revise"] += 1
            lesson = prompt.split("CURRENT LESSON:\n", 1)[1].replace(FACTUAL_ERROR, "")
            return Revision(lesson_markdown=lesson, change_log=[{"check_id": "L1_ACCURACY", "change": "Removed false claim."}])
        if schema is GuidelineDecision:
            self.calls["learn"] += 1
            return GuidelineDecision(action="new", duplicate_of="",
                                     guideline="Never say RAG retrains or changes the model; say it adds text to the prompt.")
        if schema is NewCheck:
            return NewCheck(name="No English idioms", dimension="beginner-friendly language",
                            criterion="The lesson contains no English idioms.")
        raise AssertionError(f"unexpected schema {schema}")


@pytest.fixture
def settings(tmp_path):
    s = Settings(provider="anthropic", generator_model="fake-gen", evaluator_model="fake-eval")
    s.runs_dir, s.output_dir = tmp_path / "runs", tmp_path / "output"
    s.memory_path = tmp_path / "memory.json"
    s.knowledge_dir = ROOT / "knowledge"
    s.max_retries, s.learn_min_failures = 2, 2
    return s


def quiet(_):
    pass


def test_rules_pass_on_good_lesson():
    for check_id, fn in rules.RULES.items():
        passed, evidence, *_ = fn(GOOD)
        assert passed, (check_id, evidence)


def test_rules_catch_long_sentence_injection():
    passed, evidence, *_ = rules.check_sentences(inject(GOOD, "long-sentence"))
    assert not passed and any("words)" in e for e in evidence)


def test_clean_draft_ships_first_time(settings):
    llm = FakeLLM()
    state = run("Introduction to RAG", settings, llm, Memory(settings.memory_path), log=quiet)
    assert state["status"] == "PASSED" and len(state["history"]) == 1
    assert Path(state["outputs"]["lesson"]).name == "final_lesson.md"


def test_injected_error_is_caught_and_fixed(settings):
    llm = FakeLLM()
    state = run("Introduction to RAG", settings, llm, Memory(settings.memory_path), inject_mode="factual", log=quiet)
    first, second = state["history"]
    assert not first["passed"]
    assert [r["check_id"] for r in first["results"] if not r["passed"]] == ["L1_ACCURACY"]
    assert second["passed"] and second["strategy"] == "revise"
    log = Path(state["outputs"]["log_md"]).read_text(encoding="utf-8")
    assert "caught by:** L1_ACCURACY" in log and "Removed false claim." in log


def test_loop_terminates_and_escalates(settings):
    llm = FakeLLM(stubborn=True)
    memory = Memory(settings.memory_path)
    state = run("Introduction to RAG", settings, llm, memory, log=quiet)
    assert state["status"] == "NEEDS_HUMAN_REVIEW"
    assert [h["strategy"] for h in state["history"]] == ["generate", "revise", "regenerate"]
    assert len(state["history"]) == settings.max_retries + 1
    assert Path(state["outputs"]["lesson"]).name == "best_attempt_NEEDS_REVIEW.md"
    # Repeated failure -> learner wrote a guideline, persisted to disk.
    reloaded = Memory(settings.memory_path)
    assert reloaded.guideline_texts() and reloaded.data["runs"][-1]["status"] == "NEEDS_HUMAN_REVIEW"


def test_learned_guideline_reaches_next_run_prompt(settings):
    memory = Memory(settings.memory_path)
    run("Introduction to RAG", settings, FakeLLM(stubborn=True), memory, log=quiet)
    seen = {}

    class Spy(FakeLLM):
        def text(self, system, prompt, *, role):
            seen["prompt"] = prompt
            return super().text(system, prompt, role=role)

    run("Introduction to RAG", settings, Spy(), Memory(settings.memory_path), log=quiet)
    assert "Never say RAG retrains" in seen["prompt"]


def test_human_feedback_adds_rubric_check(settings):
    from lesson_agent.learner import add_human_feedback
    from lesson_agent.rubric import CORE_CHECKS, build_rubric
    memory = Memory(settings.memory_path)
    add_human_feedback(memory, "Learners got confused by 'piece of cake'.", as_check=True, llm=FakeLLM())
    rubric = build_rubric(memory.learned_checks())
    assert len(rubric) == len(CORE_CHECKS) + 1 and rubric[-1].source == "human"


def test_jargon_prescreen_flags_unexplained_term():
    lesson = GOOD.replace("## Quick recap\n", "## Quick recap\n\n- RAG does not change the model weights.\n")
    suspects = dict(rules.undefined_at_first_use(lesson, ["weights", "chunk", "hallucination"]))
    assert list(suspects) == ["weights"]

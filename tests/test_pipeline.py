"""Offline tests: a scripted fake LLM drives the real graph, rules, memory and reports.

These prove the control logic (routing, termination, regeneration strategy, memory,
learning, injection detection) for every test topic. The quality of the real model's
judgments is shown by the live runs in runs/ and by `calibrate`, not here.
"""
from __future__ import annotations

import re
from pathlib import Path

from lesson_agent import prompts, rules
from lesson_agent.evaluator import _EXTRA_NOTES, _STATIC_ITEMS
from lesson_agent.graph import run
from lesson_agent.inject import inject
from lesson_agent.knowledge import matches
from lesson_agent.memory import Memory
from lesson_agent.rubric import CORE_CHECKS, REQUIRED_SECTIONS

from .conftest import TOPICS, FakeLLM, quiet


def test_shared_code_text_names_no_topic():
    """The cardinal rule: template, rubric and judge items must not know any topic."""
    shared = "\n".join([prompts.GENERATOR_SYSTEM, prompts.REVISER_SYSTEM, prompts.JUDGE_SYSTEM,
                        prompts.REFERENCE_BUILDER_SYSTEM, str(REQUIRED_SECTIONS)]
                       + [c.criterion + c.name for c in CORE_CHECKS]
                       + [i.text for items in _STATIC_ITEMS.values() for i in items]
                       + list(_EXTRA_NOTES.values())).lower()
    for t in TOPICS:
        leaked = [w for w in t.signature if re.search(rf"\b{re.escape(w.lower())}", shared)]
        assert not leaked, f"topic words from {t.key!r} in shared code text: {leaked}"


def test_rules_pass_on_good_lesson(topic):
    for check_id, fn in rules.RULES.items():
        passed, evidence, *_ = fn(topic.lesson)
        assert passed, (topic.key, check_id, evidence)
    assert rules.check_resources(topic.lesson, topic.reference["resources"])[0]


def test_rules_catch_long_sentence_injection(topic):
    passed, evidence, *_ = rules.check_sentences(inject(topic.lesson, "long-sentence", topic.reference))
    assert not passed and any("words)" in e for e in evidence)


def test_clean_draft_ships_first_time(settings, topic):
    state = run(topic.topic, settings, FakeLLM(topic), Memory(settings.memory_path), log=quiet)
    assert state["reference"]["topic"] == topic.topic  # the right sheet was picked for the topic
    assert state["status"] == "PASSED" and len(state["history"]) == 1
    assert Path(state["outputs"]["lesson"]).name == "final_lesson.md"


def test_injected_error_is_caught_and_fixed(settings, topic):
    llm = FakeLLM(topic)
    state = run(topic.topic, settings, llm, Memory(settings.memory_path), inject_mode="factual", log=quiet)
    first, second = state["history"]
    assert topic.reference["misconceptions"][0]["wrong"].rstrip(".") in state["planted"]
    assert [r["check_id"] for r in first["results"] if not r["passed"]] == ["L1_ACCURACY"]
    assert second["passed"] and second["strategy"] == "revise"
    log = Path(state["outputs"]["log_md"]).read_text(encoding="utf-8")
    assert "caught by:** L1_ACCURACY" in log and "Removed false claim." in log and llm.planted in log


def test_loop_terminates_and_escalates(settings, topic):
    memory = Memory(settings.memory_path)
    state = run(topic.topic, settings, FakeLLM(topic, stubborn=True), memory, log=quiet)
    assert state["status"] == "NEEDS_HUMAN_REVIEW"
    assert [h["strategy"] for h in state["history"]] == ["generate", "revise", "regenerate"]
    assert len(state["history"]) == settings.max_retries + 1
    assert Path(state["outputs"]["lesson"]).name == "best_attempt_NEEDS_REVIEW.md"
    # Repeated failure -> learner wrote a guideline, persisted to disk.
    reloaded = Memory(settings.memory_path)
    assert reloaded.guideline_texts() and reloaded.data["runs"][-1]["status"] == "NEEDS_HUMAN_REVIEW"


def test_learned_guideline_reaches_next_run_prompt(settings, topic):
    run(topic.topic, settings, FakeLLM(topic, stubborn=True), Memory(settings.memory_path), log=quiet)
    seen = {}

    class Spy(FakeLLM):
        def text(self, system, prompt, *, role):
            seen["prompt"] = prompt
            return super().text(system, prompt, role=role)

    run(topic.topic, settings, Spy(topic), Memory(settings.memory_path), log=quiet)
    assert "Never state a misconception" in seen["prompt"]
    assert f"Short name to use in headings: {topic.reference['short_name']}" in seen["prompt"]


def test_human_feedback_adds_rubric_check(settings, topic):
    from lesson_agent.learner import add_human_feedback
    from lesson_agent.rubric import build_rubric
    memory = Memory(settings.memory_path)
    add_human_feedback(memory, "Learners got confused by 'piece of cake'.", as_check=True, llm=FakeLLM(topic))
    rubric = build_rubric(memory.learned_checks())
    assert len(rubric) == len(CORE_CHECKS) + 1 and rubric[-1].source == "human"


def test_topic_matching_uses_whole_words():
    assert matches("Introduction to RAG", ["rag"])
    assert not matches("Introduction to Paragraphs", ["rag"])  # substring, not the topic
    assert not matches("Drag and drop in Figma", ["rag"])


def test_jargon_prescreen_flags_unexplained_term():
    lesson = ("# T\n\n## How does it work?\n\nA widget is a small tool. You turn the gizmo on. "
              "Each step is called a sprocket.\n")
    suspects = dict(rules.undefined_at_first_use(lesson, ["widget", "gizmo", "sprocket"]))
    assert list(suspects) == ["gizmo"]

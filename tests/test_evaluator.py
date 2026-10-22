"""Offline tests for the evaluator's defences against unreliable judges, and the provider layer.

Each scripted judge below misbehaves the way real (especially small) models do: skipping
items, inventing quotes, waving items through without proof, returning broken JSON.
"""
from __future__ import annotations

import json

import pytest

from lesson_agent import rules
from lesson_agent.calibrate import calibrate, render
from lesson_agent.config import Settings, split_model
from lesson_agent.evaluator import _run_llm_check, evaluate
from lesson_agent.inject import INJECTIONS, inject
from lesson_agent.llm import LLMError, extract_json, structured_via_text
from lesson_agent.rubric import CORE_CHECKS
from lesson_agent.schemas import ItemCheck, JudgeVerdict

from .test_pipeline import GOOD, PROOF, FakeLLM, requested_items

REF = json.loads((__import__("pathlib").Path(__file__).parent.parent / "knowledge" / "rag.json").read_text(encoding="utf-8"))
CHECK = {c.id: c for c in CORE_CHECKS}


class ScriptedJudge:
    """Returns whatever `respond(items, prompt)` builds; records prompts."""

    def __init__(self, respond):
        self.respond, self.prompts = respond, []

    def structured(self, system, prompt, schema, *, role):
        self.prompts.append(prompt)
        return self.respond(requested_items(prompt), prompt)


def verdict(items, verdict="PASS", evidence=()):
    return JudgeVerdict(items=items, reasoning="r", verdict=verdict, evidence=list(evidence), fix="")


def test_skipped_items_are_reasked_then_fail_closed():
    judge = ScriptedJudge(lambda items, p: verdict([]))  # lazy judge: no items, "PASS"
    res = _run_llm_check(judge, CHECK["L5_LEARNER_FIT"], GOOD, REF)
    assert len(judge.prompts) == 2 and "answer EVERY item" in judge.prompts[1]
    assert not res["passed"] and all("did not check" in e for e in res["evidence"])


def test_pass_without_real_quote_does_not_count_as_proof():
    judge = ScriptedJudge(lambda items, p: verdict(
        [ItemCheck(item=t, met=True, quote="RAG is taught with a lovely song about elephants") for t in items]))
    res = _run_llm_check(judge, CHECK["L2_COVERAGE"], GOOD, REF)
    assert not res["passed"] and "quote not found" in res["evidence"][0]


def test_invented_extra_problem_is_dropped_but_real_one_counts():
    def respond(items, p):
        met = [ItemCheck(item=t, met=True, quote="") for t in items]
        return verdict(met + [ItemCheck(item="other", met=False, quote="RAG was invented in 1850 by monks")])
    res = _run_llm_check(ScriptedJudge(respond), CHECK["L5_LEARNER_FIT"], GOOD, REF)
    assert res["passed"] and res["metrics"]["ungrounded_dropped"] == 1

    real = rules.sentences(GOOD)[5]
    res = _run_llm_check(ScriptedJudge(lambda items, p: verdict(
        [ItemCheck(item=t, met=True, quote="") for t in items], "FAIL", [real])), CHECK["L5_LEARNER_FIT"], GOOD, REF)
    assert not res["passed"] and real in res["evidence"][0]


def test_votes_take_the_majority_per_item():
    calls = iter([False, True, True])  # one noisy sample out of three flags item 1

    def respond(items, p):
        first = next(calls)
        return verdict([ItemCheck(item=items[0], met=first, quote="")] +
                       [ItemCheck(item=t, met=True, quote="") for t in items[1:]])
    assert _run_llm_check(ScriptedJudge(respond), CHECK["L5_LEARNER_FIT"], GOOD, REF, votes=3)["passed"]


def test_accuracy_items_cover_every_claim_and_flag_absolutes():
    lesson = inject(GOOD, "overclaim")
    judge = ScriptedJudge(lambda items, p: verdict([ItemCheck(item=t, met=True, quote="") for t in items]))
    _run_llm_check(judge, CHECK["L1_ACCURACY"], lesson, REF)
    prompt = "\n".join(judge.prompts)
    assert "ABSOLUTE CLAIM: \"Because the AI reads your real documents, RAG stops it from making up answers.\" The word 'stops'" in prompt
    n_claims = len(rules.technical_claims(lesson))
    assert n_claims > 20 and len(judge.prompts) == -(-(n_claims + len(REF["misconceptions"]) + 1) // 40)


def test_grounded_tolerates_formatting_but_not_invention():
    s = rules.sentences(GOOD)[3]
    assert rules.grounded(s.upper(), GOOD)
    assert rules.grounded(" ... ".join([" ".join(s.split()[:4]), " ".join(s.split()[-4:])]), GOOD)
    assert not rules.grounded("The model learns every document forever", GOOD)


def test_every_injection_changes_the_lesson():
    for mode in INJECTIONS:
        assert inject(GOOD, mode) != GOOD, mode
    assert "## What RAG cannot do" not in inject(GOOD, "missing-limits")
    assert not rules.check_structure(inject(GOOD, "missing-limits"))[0]


def test_calibration_reports_recall_and_false_alarms(tmp_path):
    s = Settings(provider="anthropic", generator_model="g", evaluator_model="e")
    report = calibrate(GOOD, CORE_CHECKS, REF, FakeLLM(), s, modes=["factual", "long-sentence", "idiom"],
                       log=lambda _: None)
    rows = {r["case"]: r for r in report["rows"]}
    assert rows["clean"]["failed"] == []
    assert rows["factual"]["caught"] == ["L1_ACCURACY"] and rows["long-sentence"]["caught"] == ["R2_SENTENCES"]
    assert rows["idiom"]["missed"] == ["L5_LEARNER_FIT"]  # the fake judge is blind to idioms
    assert report["summary"]["defects_caught"] == 2 and "MISSED L5_LEARNER_FIT" in render(report)


# ---- provider layer ----------------------------------------------------------------------

def test_split_model_routes_providers():
    assert split_model("gemini:gemini-3.5-flash", "openai") == ("gemini", "gemini-3.5-flash")
    assert split_model("llama3.1:8b", "openai") == ("openai", "llama3.1:8b")  # Ollama tag, not a provider
    s = Settings(provider="gemini", generator_model="gemini-x", evaluator_model="anthropic:claude-opus-5-5")
    assert (s.generator_provider, s.evaluator_provider, s.evaluator_model) == ("gemini", "anthropic", "claude-opus-5-5")


def test_openai_provider_requires_a_model_name(monkeypatch):
    monkeypatch.delenv("GENERATOR_MODEL", raising=False)
    monkeypatch.delenv("EVALUATOR_MODEL", raising=False)
    with pytest.raises(ValueError, match="GENERATOR_MODEL"):
        Settings(provider="openai")


def test_json_fallback_extracts_and_repairs():
    assert json.loads(extract_json('Sure!\n```json\n{"a": 1}\n```')) == {"a": 1}
    replies = iter(['{"verdict": "MAYBE"}',  # invalid -> repair round
                    'Here you go: {"items": [], "reasoning": "ok", "verdict": "PASS", "evidence": [], "fix": ""}'])
    seen = []

    def text_fn(system, prompt):
        seen.append(prompt)
        return next(replies)
    v = structured_via_text(text_fn, "sys", "judge this", JudgeVerdict)
    assert v.verdict == "PASS" and "previous reply was invalid" in seen[1]
    with pytest.raises(LLMError):
        structured_via_text(lambda s, p: "no json here", "sys", "x", JudgeVerdict)


def test_full_rubric_on_good_lesson_with_honest_fake():
    results = evaluate(GOOD, CORE_CHECKS, REF, FakeLLM())
    assert all(r["passed"] for r in results), [r["check_id"] for r in results if not r["passed"]]


def test_grounded_accepts_real_quote_with_nested_quotes():
    # Regression from live calibration: a judge's genuine quote was rejected because of 'quote marks'.
    q = "Step 3: Augment. The system makes a prompt. It contains Priya's question, the two chunks and the instruction 'Answer using only this information.'"
    assert rules.grounded(q, GOOD)

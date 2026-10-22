"""Offline tests for the evaluator's defences against unreliable judges, and the provider layer.

Each scripted judge below misbehaves the way real (especially small) models do: skipping
items, inventing quotes, waving items through without proof, returning broken JSON.
Lesson-level tests run once per test topic (see conftest.py).
"""
from __future__ import annotations

import json
import re

import pytest

from lesson_agent import rules
from lesson_agent.calibrate import calibrate, render
from lesson_agent.config import Settings, split_model
from lesson_agent.evaluator import _run_llm_check, evaluate
from lesson_agent.inject import FAKE_VIDEO, INJECTIONS, describe, inject
from lesson_agent.llm import LLMError, extract_json, structured_via_text
from lesson_agent.rubric import CORE_CHECKS
from lesson_agent.schemas import ItemCheck, JudgeVerdict

from .conftest import FakeLLM, requested_items

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


def all_met(items, p):
    return verdict([ItemCheck(item=t, met=True, quote="") for t in items])


# ---- defences against unreliable judges ---------------------------------------------------------

def test_skipped_items_are_reasked_then_fail_closed(topic):
    judge = ScriptedJudge(lambda items, p: verdict([]))  # lazy judge: no items, "PASS"
    res = _run_llm_check(judge, CHECK["L5_LEARNER_FIT"], topic.lesson, topic.reference)
    assert len(judge.prompts) == 2 and "answer EVERY item" in judge.prompts[1]
    assert not res["passed"] and all("did not check" in e for e in res["evidence"])


def test_pass_without_real_quote_does_not_count_as_proof(topic):
    judge = ScriptedJudge(lambda items, p: verdict(
        [ItemCheck(item=t, met=True, quote="This is taught with a lovely song about elephants") for t in items]))
    res = _run_llm_check(judge, CHECK["L2_COVERAGE"], topic.lesson, topic.reference)
    assert not res["passed"] and "quote not found" in res["evidence"][0]


def test_invented_extra_problem_is_dropped_but_real_one_counts(topic):
    def respond(items, p):
        return verdict(all_met(items, p).items + [ItemCheck(item="other", met=False, quote="It was invented in 1850 by monks")])
    res = _run_llm_check(ScriptedJudge(respond), CHECK["L5_LEARNER_FIT"], topic.lesson, topic.reference)
    assert res["passed"] and res["metrics"]["ungrounded_dropped"] == 1

    real = rules.sentences(topic.lesson)[5]
    res = _run_llm_check(ScriptedJudge(lambda items, p: verdict(all_met(items, p).items, "FAIL", [real])),
                         CHECK["L5_LEARNER_FIT"], topic.lesson, topic.reference)
    assert not res["passed"] and real in res["evidence"][0]


def test_votes_take_the_majority_per_item(topic):
    calls = iter([False, True, True])  # one noisy sample out of three flags item 1

    def respond(items, p):
        first = next(calls)
        return verdict([ItemCheck(item=items[0], met=first, quote="")] + all_met(items[1:], p).items)
    assert _run_llm_check(ScriptedJudge(respond), CHECK["L5_LEARNER_FIT"], topic.lesson, topic.reference, votes=3)["passed"]


def test_accuracy_items_cover_every_claim_and_flag_absolutes(topic):
    lesson = inject(topic.lesson, "overclaim", topic.reference)
    planted = describe("overclaim", topic.lesson, topic.reference)
    judge = ScriptedJudge(all_met)
    _run_llm_check(judge, CHECK["L1_ACCURACY"], lesson, topic.reference)
    prompt = "\n".join(judge.prompts)
    assert f"ABSOLUTE CLAIM: \"{planted}\" The word 'stops'" in prompt
    n_claims = len(rules.technical_claims(lesson))
    n_items = n_claims + len(topic.reference["misconceptions"]) + 1
    assert n_claims > 20 and len(judge.prompts) == -(-n_items // 40)  # batches of 40, none skipped


def test_full_rubric_on_good_lesson_with_honest_fake(topic):
    results = evaluate(topic.lesson, CORE_CHECKS, topic.reference, FakeLLM(topic))
    assert all(r["passed"] for r in results), [r["check_id"] for r in results if not r["passed"]]


# ---- injections and calibration, per topic -----------------------------------------------------

def test_every_injection_is_built_from_the_topic_and_changes_the_lesson(topic):
    for mode in INJECTIONS:
        assert inject(topic.lesson, mode, topic.reference) != topic.lesson, mode
    assert topic.reference["misconceptions"][0]["wrong"].rstrip(".") in describe("factual", topic.lesson, topic.reference)
    assert topic.reference["short_name"] in describe("overclaim", topic.lesson, topic.reference)
    # The jargon defect uses the topic's own terms that the lesson never explains.
    jargon_text = describe("jargon", topic.lesson, topic.reference)
    assert any(t in jargon_text for t in topic.reference["jargon"])
    assert not rules.find_jargon(topic.lesson, [t for t in topic.reference["jargon"] if t in jargon_text])
    removed = inject(topic.lesson, "missing-limits", topic.reference)
    assert not re.search(r"^##\s.*(cannot|limit)", removed, re.M | re.I)
    assert not rules.check_structure(removed)[0]


def test_calibration_reports_recall_and_false_alarms(topic):
    s = Settings(provider="anthropic", generator_model="g", evaluator_model="e")
    report = calibrate(topic.lesson, CORE_CHECKS, topic.reference, FakeLLM(topic), s,
                       modes=["factual", "long-sentence", "idiom", "fake-link"], log=lambda _: None)
    rows = {r["case"]: r for r in report["rows"]}
    assert rows["clean"]["failed"] == []
    assert rows["factual"]["caught"] == ["L1_ACCURACY"] and rows["long-sentence"]["caught"] == ["R2_SENTENCES"]
    assert rows["fake-link"]["caught"] == ["R6_RESOURCES"]
    assert rows["idiom"]["missed"] == ["L5_LEARNER_FIT"]  # the fake judge is blind to idioms
    assert report["summary"]["defects_caught"] == 3 and "MISSED L5_LEARNER_FIT" in render(report)
    assert report["summary"]["topic"] == topic.topic


# ---- rule helpers ----------------------------------------------------------------------------

def test_grounded_tolerates_formatting_but_not_invention(topic):
    s = rules.sentences(topic.lesson)[3]
    assert rules.grounded(s.upper(), topic.lesson)
    assert rules.grounded(" ... ".join([" ".join(s.split()[:4]), " ".join(s.split()[-4:])]), topic.lesson)
    assert not rules.grounded("The moon is made of green cheese and sings at night", topic.lesson)


def test_grounded_accepts_real_quote_with_nested_quotes():
    # Regression from live calibration: a judge's genuine quote was rejected because of 'quote marks'.
    md = 'Step 3. The system writes a note. It contains the question and the line "Use only this text."'
    assert rules.grounded("Step 3. The system writes a note. It contains the question and the line 'Use only this text.'", md)


def test_resources_rule_rejects_invented_links(topic):
    res = topic.reference["resources"]
    passed, evidence, *_ = rules.check_resources(inject(topic.lesson, "fake-link", topic.reference), res)
    assert not passed and FAKE_VIDEO in evidence[0]
    article = next(r["url"] for r in res if r["type"] == "article")
    no_video = re.sub(r"https://www\.youtube\.com/watch\?v=[\w-]{11}", article, topic.lesson)
    passed, evidence, *_ = rules.check_resources(no_video, res)
    assert not passed and any("No video" in e for e in evidence)
    # Nothing verified (offline): links aren't required, but none may appear.
    assert not rules.check_resources(topic.lesson, [])[0]
    assert rules.check_resources(rules.without_resources(topic.lesson), [])[0]


def test_link_list_is_not_judged_as_prose(topic):
    assert "youtube" not in " ".join(s for s, _ in rules.technical_claims(topic.lesson))
    assert rules.check_sentences(topic.lesson)[0]


# ---- web research ------------------------------------------------------------------------------

def test_research_keeps_only_live_links_and_sourced_facts(monkeypatch, tmp_path):
    from lesson_agent import web

    s = Settings(provider="anthropic", generator_model="g", evaluator_model="e")
    s.knowledge_dir, s.tavily_api_key, s.web_research, s.verify_links = tmp_path, "k", True, True
    fake_results = {
        "explained for beginners": [{"url": "https://www.youtube.com/watch?v=AAAAAAAAAAA", "title": "v"},
                                    {"url": "https://www.youtube.com/watch?v=DEADDEADDEA", "title": "gone"}],
        "in Hindi": [{"url": "https://www.youtube.com/watch?v=HHHHHHHHHHH", "title": "h"}],
        "latest developments": [{"url": "https://news.example/topic", "title": "Topic today", "content": "..."}],
    }
    monkeypatch.setattr(web, "search", lambda settings, q, **kw: next(v for k, v in fake_results.items() if k in q))
    live = {"https://www.youtube.com/watch?v=AAAAAAAAAAA": "Topic X for beginners",
            "https://www.youtube.com/watch?v=HHHHHHHHHHH": "Topic X kya hai? Hindi mein",
            "https://www.youtube.com/watch?v=CCCCCCCCCCC": "Curated explainer"}
    monkeypatch.setattr(web, "verify", lambda url: {"url": url, "type": "video", "title": live[url], "source": "ch"}
                        if url in live else None)

    class FactLLM:
        def structured(self, system, prompt, schema, *, role):
            return web.WebFacts(facts=[web.WebFact(fact="Topic X is widely used today.", source_url="https://news.example/topic"),
                                       web.WebFact(fact="Invented.", source_url="https://made-up.example")])

    ref = {"short_name": "Topic X", "facts": [], "resources": [{"url": "https://www.youtube.com/watch?v=CCCCCCCCCCC",
                                                               "type": "video", "title": "x", "why": "curated note"}]}
    data = web.research("Topic X", ref, FactLLM(), s, log=lambda _: None)
    urls = [r["url"] for r in data["resources"]]
    assert urls[0].endswith("CCCCCCCCCCC") and data["resources"][0]["why"] == "curated note"  # curated first
    assert "https://www.youtube.com/watch?v=DEADDEADDEA" not in urls  # failed the live check
    assert any(r["language"] == "Hindi" for r in data["resources"])
    assert [f["source_url"] for f in data["web_facts"]] == ["https://news.example/topic"]  # invented source dropped
    assert list((tmp_path / "web").glob("*.json"))  # cached for the day


def test_uncurated_topic_gets_a_generated_reference_sheet(tmp_path):
    from lesson_agent.knowledge import load_reference
    from lesson_agent.schemas import MustCover, Misconception, ReferenceSheet

    class SheetLLM:
        def structured(self, system, prompt, schema, *, role):
            assert schema is ReferenceSheet and "Topic: Introduction to Photosynthesis" in prompt
            return ReferenceSheet(short_name="Photosynthesis", prerequisite="what a plant cell is",
                                  must_cover=[MustCover(id="M1", point="What it is")], facts=["Plants use light."],
                                  misconceptions=[Misconception(wrong="Plants eat soil.", right="They make food.")],
                                  jargon=["chlorophyll"])
    ref = load_reference("Introduction to Photosynthesis", tmp_path, SheetLLM(), log=lambda _: None)
    assert ref["trust"] == "generated" and ref["short_name"] == "Photosynthesis" and ref["resources"] == []
    assert load_reference("Introduction to Photosynthesis", tmp_path, None)["short_name"] == "Photosynthesis"  # cached


# ---- provider layer ----------------------------------------------------------------------------

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

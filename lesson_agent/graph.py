"""The agent: a LangGraph state machine.

    prepare -> research -> generate -> evaluate --pass--------------------------> finalize -> learn -> END
                  ^           |                                         ^
                  |           +--fail, retries left, new failures--> revise --> evaluate
                  |           +--fail, same check failed twice-----> generate (fresh draft)
                  |           +--fail, no retries left ---------------------------+
                  +-------------------------------------------------------------- (loop)

Why a graph and not a while-loop: the routing decision is explicit and testable on its
own, every node's input/output is a typed state slice that we log, and the loop bound
(max_retries) is enforced in one place, so the run always terminates.
"""
from __future__ import annotations

import difflib
import json
import operator
from datetime import datetime
from pathlib import Path
from typing import Annotated, Callable, TypedDict

from langgraph.graph import END, StateGraph

from .config import Settings
from .evaluator import evaluate, summarize
from .inject import INJECTIONS, describe, inject
from .knowledge import load_reference
from .learner import learn_from_run
from .llm import LLM
from .memory import Memory, now
from .prompts import GENERATOR_SYSTEM, REVISER_SYSTEM, generate_prompt, revise_prompt
from .report import append_learning, write_outputs
from .rubric import build_rubric
from .schemas import Revision
from .web import research as web_research


class LessonState(TypedDict, total=False):
    topic: str
    inject: str | None
    planted: str  # the exact defect text planted by --inject
    run_id: str
    run_dir: str
    reference: dict
    guidelines: list[str]
    attempt: int
    lesson: str
    strategy: str  # how the current draft was produced: generate | revise | regenerate
    change_log: list[dict]
    history: Annotated[list[dict], operator.add]  # one record per evaluated attempt
    status: str  # PASSED | NEEDS_HUMAN_REVIEW
    outputs: dict
    learned: list[str]


def _repeat_failures(history: list[dict]) -> list[str]:
    """Checks that failed in each of the last two attempts."""
    if len(history) < 2:
        return []
    fails = [{r["check_id"] for r in h["results"] if not r["passed"]} for h in history[-2:]]
    return sorted(fails[0] & fails[1])


def build_graph(settings: Settings, llm: LLM, memory: Memory, log: Callable[[str], None] = print):
    rubric = build_rubric(memory.learned_checks())

    def save(state: LessonState, name: str, content: str) -> str:
        path = Path(state["run_dir"]) / name
        path.write_text(content, encoding="utf-8")
        return str(path)

    # ---- nodes ----------------------------------------------------------------------
    def prepare(state: LessonState) -> LessonState:
        run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
        run_dir = settings.runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        reference = load_reference(state["topic"], settings.knowledge_dir, llm, settings, log)
        guidelines = memory.guideline_texts()
        log(f"[prepare] run {run_id} | reference: {reference.get('trust')} | "
            f"rubric: {len(rubric)} checks | learned guidelines in prompt: {len(guidelines)}")
        return {"run_id": run_id, "run_dir": str(run_dir), "reference": reference,
                "guidelines": guidelines, "attempt": 0, "change_log": []}

    def research(state: LessonState) -> LessonState:
        """Fresh facts and verified learning resources from the web (best-effort, cached per day)."""
        data = web_research(state["topic"], state["reference"], llm, settings, log)
        reference = {**state["reference"], "resources": data["resources"], "web_facts": data["web_facts"],
                     "web_sources": data["sources"]}
        return {"reference": reference}

    def generate(state: LessonState) -> LessonState:
        attempt = state["attempt"] + 1
        history = state.get("history", [])
        avoid, change_log = [], []
        strategy = "generate"
        if history:  # we got here from the router: a fresh rewrite after repeated failures
            strategy = "regenerate"
            last = {r["check_id"]: r for r in history[-1]["results"]}
            repeated = _repeat_failures(history)
            avoid = [f"[{cid}] {last[cid]['criterion']} Last problem: {'; '.join(last[cid]['evidence'][:2])}"
                     for cid in repeated]
            change_log = [{"check_id": cid, "change": "Targeted edits failed twice, so the lesson was rewritten "
                           "from scratch with this failure given as an explicit constraint."} for cid in repeated]
        log(f"[{strategy}] attempt {attempt}: writing draft with {settings.generator_model}...")
        lesson = llm.text(GENERATOR_SYSTEM,
                          generate_prompt(state["topic"], state["reference"], state["guidelines"], avoid),
                          role="generator")
        planted = {}
        if attempt == 1 and state.get("inject"):
            planted = {"planted": describe(state["inject"], lesson, state["reference"])}
            lesson = inject(lesson, state["inject"], state["reference"])
            log(f"[inject] planted a deliberate '{state['inject']}' error; "
                f"expect {INJECTIONS[state['inject']]['expected']} to fail")
        save(state, f"attempt_{attempt}.md", lesson)
        return {"attempt": attempt, "lesson": lesson, "strategy": strategy, "change_log": change_log, **planted}

    def revise(state: LessonState) -> LessonState:
        attempt = state["attempt"] + 1
        last = state["history"][-1]["results"]
        failures = [r for r in last if not r["passed"]]
        passed_ids = [r["check_id"] for r in last if r["passed"]]
        log(f"[revise] attempt {attempt}: fixing {[f['check_id'] for f in failures]}...")
        rev = llm.structured(REVISER_SYSTEM,
                             revise_prompt(state["lesson"], failures, passed_ids, state["reference"],
                                           state["guidelines"]),
                             Revision, role="generator")
        lesson = rev.lesson_markdown.strip()
        save(state, f"attempt_{attempt}.md", lesson)
        diff = "".join(difflib.unified_diff(state["lesson"].splitlines(True), lesson.splitlines(True),
                                            f"attempt_{attempt - 1}.md", f"attempt_{attempt}.md"))
        save(state, f"attempt_{attempt}.diff", diff)
        return {"attempt": attempt, "lesson": lesson, "strategy": "revise",
                "change_log": [c.model_dump() for c in rev.change_log]}

    def evaluate_node(state: LessonState) -> LessonState:
        attempt = state["attempt"]
        log(f"[evaluate] attempt {attempt}: {len(rubric)} checks with {settings.evaluator_model}...")
        results = evaluate(state["lesson"], rubric, state["reference"], llm, settings.eval_concurrency, settings.judge_votes)
        memory.record_evaluation(results, state["run_id"], attempt)
        memory.save()
        passed = all(r["passed"] for r in results)
        log(f"[evaluate] attempt {attempt}: {summarize(results)}")
        record = {"attempt": attempt, "strategy": state["strategy"], "passed": passed,
                  "n_passed": sum(r["passed"] for r in results), "results": results,
                  "change_log": state.get("change_log", []), "lesson_file": f"attempt_{attempt}.md",
                  "injected": state.get("inject") if attempt == 1 else None, "timestamp": now()}
        save(state, f"attempt_{attempt}_eval.json", json.dumps(record, indent=2, ensure_ascii=False))
        return {"history": [record]}

    def finalize(state: LessonState) -> LessonState:
        history = state["history"]
        winner = next((h for h in reversed(history) if h["passed"]), None)
        status = "PASSED" if winner else "NEEDS_HUMAN_REVIEW"
        if winner is None:
            # Nothing cleared the bar: surface the closest attempt, clearly labelled, for a human.
            winner = max(history, key=lambda h: (h["n_passed"], h["attempt"]))
        lesson = (Path(state["run_dir"]) / winner["lesson_file"]).read_text(encoding="utf-8")
        outputs = write_outputs(settings, state, history, winner, lesson, status)
        log(f"[finalize] {status} after {len(history)} attempt(s); lesson -> {outputs['lesson']}")
        return {"status": status, "outputs": outputs}

    def learn(state: LessonState) -> LessonState:
        failed = {r["check_id"] for h in state["history"] for r in h["results"] if not r["passed"]}
        notes = learn_from_run(memory, rubric, failed, llm, settings.learn_min_failures, settings.max_guidelines)
        memory.record_run({
            "run_id": state["run_id"], "topic": state["topic"], "timestamp": now(), "status": state["status"],
            "attempts": len(state["history"]), "injected": state.get("inject"),
            "failed_per_attempt": [[r["check_id"] for r in h["results"] if not r["passed"]] for h in state["history"]],
            "learned": notes,
        })
        memory.save()
        append_learning(state["outputs"], notes, memory)
        for n in notes:
            log(f"[learn] {n}")
        if not notes:
            log("[learn] nothing new to learn this run")
        return {"learned": notes}

    # ---- routing --------------------------------------------------------------------
    def route(state: LessonState) -> str:
        last = state["history"][-1]
        if last["passed"]:
            return "finalize"
        if state["attempt"] > settings.max_retries:
            log(f"[route] retry budget ({settings.max_retries}) used up -> finalize for human review")
            return "finalize"
        if _repeat_failures(state["history"]):
            log(f"[route] {_repeat_failures(state['history'])} failed twice in a row -> fresh rewrite")
            return "generate"
        return "revise"

    g = StateGraph(LessonState)
    g.add_node("prepare", prepare)
    g.add_node("research", research)
    g.add_node("generate", generate)
    g.add_node("revise", revise)
    g.add_node("evaluate", evaluate_node)
    g.add_node("finalize", finalize)
    g.add_node("learn", learn)
    g.set_entry_point("prepare")
    g.add_edge("prepare", "research")
    g.add_edge("research", "generate")
    g.add_edge("generate", "evaluate")
    g.add_edge("revise", "evaluate")
    g.add_conditional_edges("evaluate", route, {"finalize": "finalize", "revise": "revise", "generate": "generate"})
    g.add_edge("finalize", "learn")
    g.add_edge("learn", END)
    return g.compile()


def run(topic: str, settings: Settings, llm: LLM, memory: Memory, inject_mode: str | None = None,
        log: Callable[[str], None] = print) -> LessonState:
    app = build_graph(settings, llm, memory, log)
    return app.invoke({"topic": topic, "inject": inject_mode, "history": []},
                      {"recursion_limit": 25})

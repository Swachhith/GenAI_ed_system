"""Writes the run's deliverables: the lesson and the rejection log (Markdown + JSON)."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from .inject import INJECTIONS


def _diff_stats(run_dir: Path, attempt: int) -> str:
    p = run_dir / f"attempt_{attempt}.diff"
    if not p.exists():
        return ""
    lines = p.read_text(encoding="utf-8").splitlines()
    added = sum(1 for line in lines if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in lines if line.startswith("-") and not line.startswith("---"))
    return f"Diff vs previous draft: +{added} / -{removed} lines (`{p.name}`)"


def _render_log(settings, state, history, winner, status) -> str:
    run_dir = Path(state["run_dir"])
    ref = state["reference"]
    out = [f"# Rejection log: {state['topic']}", "",
           f"- **Run:** `{state['run_id']}`",
           f"- **Status:** {'✅ PASSED, shipped' if status == 'PASSED' else '⚠️ NEEDS HUMAN REVIEW, not shipped'}",
           f"- **Shipped attempt:** {winner['attempt']} of {len(history)} (retry budget: {settings.max_retries})",
           f"- **Generator:** `{settings.generator_provider}:{settings.generator_model}` | **Evaluator:** `{settings.evaluator_provider}:{settings.evaluator_model}` (judge votes: {settings.judge_votes})",
           f"- **Grounding:** reference sheet `{Path(ref.get('path', '?')).name}` (trust: {ref.get('trust')})",
           f"- **Learned guidelines in the prompt at start:** {len(state.get('guidelines', []))}"]
    if state.get("inject"):
        spec = INJECTIONS[state["inject"]]
        caught = [c for c in spec["expected"] if any(r["check_id"] == c and not r["passed"] for r in history[0]["results"])]
        out += [f"- **Deliberate error injected into attempt 1:** `{state['inject']}`: \"{spec.get('text') or 'deleted the section: ' + spec['remove_section']}\"",
                f"- **Expected to be caught by:** {', '.join(spec['expected'])} -> "
                f"**caught by:** {', '.join(caught) or 'NONE (evaluator missed it)'}"]
    out += ["", "## Summary", "", "| Attempt | How produced | Result | Failed checks |", "|---|---|---|---|"]
    for h in history:
        fails = [r["check_id"] for r in h["results"] if not r["passed"]]
        out.append(f"| {h['attempt']} | {h['strategy']} | {'PASS' if h['passed'] else 'FAIL'} "
                   f"({h['n_passed']}/{len(h['results'])}) | {', '.join(fails) or '-'} |")

    for i, h in enumerate(history):
        out += ["", f"## Attempt {h['attempt']} ({h['strategy']}): {'PASS' if h['passed'] else 'FAIL'}", ""]
        if h["change_log"]:
            out.append("**What changed in this draft (in response to the previous rejection):**")
            out += [f"- `{c['check_id']}`: {c['change']}" for c in h["change_log"]]
            stats = _diff_stats(run_dir, h["attempt"])
            if stats:
                out.append(f"- {stats}")
            out.append("")
        fails = [r for r in h["results"] if not r["passed"]]
        if not fails:
            out.append("All checks passed.")
            continue
        out.append("**What failed and why:**")
        for r in fails:
            out += ["", f"- **{r['check_id']}: {r['name']}** _({r['dimension']}, {r['kind']} check)_",
                    f"  - Requirement: {r['criterion']}"]
            out += [f"  - Evidence: {e}" for e in r["evidence"][:6]]
            if r["reasoning"]:
                out.append(f"  - Judge reasoning: {r['reasoning']}")
            if r["fix"]:
                out.append(f"  - Fix requested: {r['fix']}")
        if i == len(history) - 1 and not h["passed"]:
            out += ["", "_Retry budget exhausted, so the loop stopped here._"]

    out += ["", "## Final scorecard (shipped attempt)", "", "| Check | Dimension | Result | Metrics |", "|---|---|---|---|"]
    for r in winner["results"]:
        metrics = ", ".join(f"{k}={v}" for k, v in r["metrics"].items() if not isinstance(v, list))
        out.append(f"| {r['check_id']} {r['name']} | {r['dimension']} | {'PASS' if r['passed'] else 'FAIL'} | {metrics} |")
    return "\n".join(out) + "\n"


def write_outputs(settings, state, history, winner, lesson: str, status: str) -> dict:
    run_dir = Path(state["run_dir"])
    lesson_name = "final_lesson.md" if status == "PASSED" else "best_attempt_NEEDS_REVIEW.md"
    paths = {"lesson": run_dir / lesson_name, "log_md": run_dir / "rejection_log.md",
             "log_json": run_dir / "rejection_log.json"}
    paths["lesson"].write_text(lesson, encoding="utf-8")
    paths["log_md"].write_text(_render_log(settings, state, history, winner, status), encoding="utf-8")
    paths["log_json"].write_text(json.dumps({
        "run_id": state["run_id"], "topic": state["topic"], "status": status, "shipped_attempt": winner["attempt"],
        "generator_model": settings.generator_model, "evaluator_model": settings.evaluator_model,
        "injected": state.get("inject"), "guidelines_used": state.get("guidelines", []), "attempts": history,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    # Stable "latest" copies for the submission.
    settings.output_dir.mkdir(parents=True, exist_ok=True)
    for key in ("lesson", "log_md", "log_json"):
        shutil.copyfile(paths[key], settings.output_dir / paths[key].name)
    paths["log_md_latest"] = settings.output_dir / "rejection_log.md"
    return {k: str(v) for k, v in paths.items()}


def append_learning(outputs: dict, notes: list[str], memory) -> None:
    lines = ["", "## What the system learned from this run", ""]
    lines += [f"- {n}" for n in notes] or ["- No check has failed often enough to change the prompt yet."]
    lines += ["", f"Active guidelines now in memory: {len(memory.active_guidelines())} | "
                  f"learned rubric checks: {len(memory.learned_checks())}"]
    for key in ("log_md", "log_md_latest"):
        with Path(outputs[key]).open("a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

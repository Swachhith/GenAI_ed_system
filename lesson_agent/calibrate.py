"""Calibrate the rubric: does the evaluator catch known defects, and leave good lessons alone?

A rubric is only as good as its judges, and judge quality depends on the model. So
instead of trusting the evaluator, we test it: take a known-good lesson, plant each
defect from inject.py into a copy, evaluate every copy, and report

  * recall      - planted defects caught by the check that owns them,
  * false alarms - checks failing on the clean lesson,
  * spillover    - unrelated checks failing on a planted copy (noise).

Run it whenever you change the judge model, a prompt or a threshold:
  python -m lesson_agent calibrate [--lesson FILE] [--modes factual,idiom]
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from .evaluator import evaluate
from .inject import INJECTIONS, inject


def calibrate(lesson: str, rubric, reference: dict, llm, settings, modes: list[str] | None = None,
              log=print) -> dict:
    cases = [("clean", lesson, [], [])]
    for mode in modes or list(INJECTIONS):
        spec = INJECTIONS[mode]
        cases.append((mode, inject(lesson, mode), spec["expected"], spec["also"]))

    rows = []
    for name, text, expected, also in cases:
        t0 = time.time()
        results = evaluate(text, rubric, reference, llm, settings.eval_concurrency, settings.judge_votes)
        failed = [r["check_id"] for r in results if not r["passed"]]
        row = {
            "case": name, "expected": expected, "failed": failed,
            "caught": [c for c in expected if c in failed],
            "missed": [c for c in expected if c not in failed],
            "spillover": [c for c in failed if c not in expected and c not in also],
            "evidence": {r["check_id"]: r["evidence"][:3] for r in results if not r["passed"]},
            "seconds": round(time.time() - t0, 1),
        }
        rows.append(row)
        status = ("clean " + ("OK" if not failed else f"FALSE ALARM {failed}") if name == "clean" else
                  ("CAUGHT" if not row["missed"] else f"MISSED {row['missed']}") +
                  (f" (spillover {row['spillover']})" if row["spillover"] else ""))
        log(f"  {name:<15} {status}")

    planted = [r for r in rows if r["case"] != "clean"]
    expected_total = sum(len(r["expected"]) for r in planted)
    summary = {
        "evaluator": f"{settings.evaluator_provider}:{settings.evaluator_model}",
        "judge_votes": settings.judge_votes,
        "defects_caught": sum(not r["missed"] for r in planted), "defects_planted": len(planted),
        "expected_checks_fired": sum(len(r["caught"]) for r in planted), "expected_checks_total": expected_total,
        "false_alarms_on_clean": rows[0]["failed"],
        "spillover_failures": sum(len(r["spillover"]) for r in planted),
    }
    return {"summary": summary, "rows": rows}


def render(report: dict) -> str:
    s = report["summary"]
    out = ["# Rubric calibration", "",
           f"- **Evaluator:** `{s['evaluator']}` (judge votes: {s['judge_votes']})",
           f"- **Defects caught:** {s['defects_caught']}/{s['defects_planted']} "
           f"(expected checks fired: {s['expected_checks_fired']}/{s['expected_checks_total']})",
           f"- **False alarms on the clean lesson:** {', '.join(s['false_alarms_on_clean']) or 'none'}",
           f"- **Spillover failures (unrelated checks):** {s['spillover_failures']}", "",
           "| Case | Planted defect | Must fail | Failed | Result |", "|---|---|---|---|---|"]
    for r in report["rows"]:
        spec = INJECTIONS.get(r["case"], {})
        planted = spec.get("text") or (f"deleted section '{spec['remove_section']}'" if spec else "(none)")
        if r["case"] == "clean":
            result = "OK" if not r["failed"] else "FALSE ALARM"
        else:
            result = ("CAUGHT" if not r["missed"] else "MISSED " + ", ".join(r["missed"])) + \
                     (f"; spillover: {', '.join(r['spillover'])}" if r["spillover"] else "")
        out.append(f"| {r['case']} | {planted[:90]}{'...' if len(planted) > 90 else ''} | "
                   f"{', '.join(r['expected']) or '-'} | {', '.join(r['failed']) or '-'} | {result} |")
    out += ["", "## Evidence for each failure", ""]
    for r in report["rows"]:
        for cid, ev in r["evidence"].items():
            out.append(f"- **{r['case']} / {cid}:** " + " | ".join(e[:200] for e in ev))
    return "\n".join(out) + "\n"


def write_report(report: dict, settings) -> Path:
    stamp = time.strftime("%Y%m%d-%H%M%S")
    run_dir = settings.runs_dir / f"calibration-{stamp}"
    run_dir.mkdir(parents=True, exist_ok=True)
    md = render(report)
    (run_dir / "calibration.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    (run_dir / "calibration.md").write_text(md, encoding="utf-8")
    settings.output_dir.mkdir(parents=True, exist_ok=True)
    (settings.output_dir / "calibration.md").write_text(md, encoding="utf-8")
    return run_dir / "calibration.md"

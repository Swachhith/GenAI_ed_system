"""CLI.

  python -m lesson_agent run [--topic T] [--inject factual|jargon|long-sentence] [--max-retries N]
  python -m lesson_agent evaluate path/to/lesson.md [--topic T]
  python -m lesson_agent calibrate [--lesson FILE] [--modes factual,idiom]
  python -m lesson_agent feedback "comment" [--as-check]
  python -m lesson_agent memory show|reset
  python -m lesson_agent graph
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import Settings
from .inject import INJECTIONS
from .memory import Memory

DEFAULT_TOPIC = "Introduction to RAG (Retrieval-Augmented Generation)"


def _scorecard(results: list[dict]) -> str:
    rows = []
    for r in results:
        rows.append(f"  {'PASS' if r['passed'] else 'FAIL'}  {r['check_id']:<16} {r['name']}")
        for e in r["evidence"][:3]:
            rows.append(f"          - {e[:160]}")
    return "\n".join(rows)


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(prog="lesson_agent", description="Self-evaluating lesson generator")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="generate -> evaluate -> regenerate until it passes")
    r.add_argument("--topic", default=DEFAULT_TOPIC)
    r.add_argument("--inject", choices=sorted(INJECTIONS), help="plant a deliberate error in draft 1")
    r.add_argument("--max-retries", type=int)

    e = sub.add_parser("evaluate", help="run the rubric on an existing lesson file (no regeneration)")
    e.add_argument("file")
    e.add_argument("--topic", default=DEFAULT_TOPIC)

    c = sub.add_parser("calibrate", help="plant known defects in a good lesson and measure what the rubric catches")
    c.add_argument("--lesson", default=str(Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "good_lesson.md"))
    c.add_argument("--modes", help="comma-separated injection modes (default: all)")
    c.add_argument("--topic", default=DEFAULT_TOPIC)

    f = sub.add_parser("feedback", help="teach the system from a human review comment")
    f.add_argument("text")
    f.add_argument("--as-check", action="store_true", help="turn the comment into a new rubric check")

    m = sub.add_parser("memory", help="inspect or reset persistent memory")
    m.add_argument("action", choices=["show", "reset"])

    sub.add_parser("graph", help="print the agent graph as Mermaid")

    args = p.parse_args(argv)
    settings = Settings()
    if getattr(args, "max_retries", None) is not None:
        settings.max_retries = args.max_retries
    memory = Memory(settings.memory_path)

    if args.cmd == "memory":
        if args.action == "reset":
            memory.reset()
            print(f"Memory reset: {settings.memory_path}")
        else:
            print(json.dumps({k: memory.data[k] for k in ("guidelines", "learned_checks", "check_stats")},
                             indent=2, ensure_ascii=False))
            print(f"\nruns recorded: {len(memory.data['runs'])}")
            for run in memory.data["runs"][-10:]:
                print(f"  {run['run_id']}  {run['status']:<19} attempts={run['attempts']} "
                      f"failed={run['failed_per_attempt']} injected={run.get('injected')}")
        return 0

    if args.cmd == "graph":
        from .graph import build_graph
        print(build_graph(settings, llm=None, memory=memory).get_graph().draw_mermaid())
        return 0

    from .llm import make_llm
    llm = make_llm(settings)

    if args.cmd == "feedback":
        from .learner import add_human_feedback
        msg = add_human_feedback(memory, args.text, args.as_check, llm)
        memory.save()
        print(msg)
        return 0

    if args.cmd == "calibrate":
        from .calibrate import calibrate, write_report
        from .knowledge import load_reference
        from .rubric import build_rubric
        modes = args.modes.split(",") if args.modes else None
        print(f"Calibrating evaluator {settings.evaluator_provider}:{settings.evaluator_model} "
              f"(votes={settings.judge_votes}) on {args.lesson}")
        report = calibrate(Path(args.lesson).read_text(encoding="utf-8"), build_rubric(memory.learned_checks()),
                           load_reference(args.topic, settings.knowledge_dir, llm), llm, settings, modes)
        s = report["summary"]
        print(f"\nCaught {s['defects_caught']}/{s['defects_planted']} planted defects | false alarms on clean: "
              f"{s['false_alarms_on_clean'] or 'none'} | spillover: {s['spillover_failures']}")
        print(f"Report: {write_report(report, settings)}")
        return 0 if s["defects_caught"] == s["defects_planted"] and not s["false_alarms_on_clean"] else 1

    if args.cmd == "evaluate":
        from .evaluator import evaluate, summarize
        from .knowledge import load_reference
        from .rubric import build_rubric
        lesson = Path(args.file).read_text(encoding="utf-8")
        reference = load_reference(args.topic, settings.knowledge_dir, llm)
        results = evaluate(lesson, build_rubric(memory.learned_checks()), reference, llm, settings.eval_concurrency, settings.judge_votes)
        print(_scorecard(results))
        print(f"\nVerdict: {'SHIP' if all(x['passed'] for x in results) else 'REJECT'} | {summarize(results)}")
        out = Path(args.file).with_suffix(".eval.json")
        out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Details: {out}")
        return 0 if all(x["passed"] for x in results) else 1

    from .graph import run
    print(f"Topic: {args.topic}\nGenerator: {settings.generator_provider}:{settings.generator_model} | "
          f"Evaluator: {settings.evaluator_provider}:{settings.evaluator_model} (votes={settings.judge_votes}) "
          f"| max retries: {settings.max_retries}\n")
    state = run(args.topic, settings, llm, memory, inject_mode=args.inject)
    print(f"\nStatus: {state['status']}")
    print(f"Lesson:        {state['outputs']['lesson']}")
    print(f"Rejection log: {state['outputs']['log_md']}")
    return 0 if state["status"] == "PASSED" else 2


if __name__ == "__main__":
    raise SystemExit(main())

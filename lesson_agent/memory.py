"""Persistent memory shared by every run: a single JSON file.

What it holds and who reads it:
  runs          - one summary per run (rejection history)        -> learner, `memory show`
  check_stats   - per-check evaluated / failed counts             -> learner (what keeps failing)
  failures      - recent failure evidence per check               -> learner (what to write a rule about)
  guidelines    - learned + human writing rules                   -> generator & reviser prompts
  learned_checks- rubric checks created from human feedback       -> evaluator
  feedback      - raw human comments, kept for audit

JSON (not a DB) because the data is small, human-readable, diffable in git and easy to
show in a demo. Writes are atomic (temp file + rename) so a crash can't corrupt it.
"""
from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

EMPTY = {"version": 1, "runs": [], "check_stats": {}, "failures": {}, "guidelines": [],
         "learned_checks": [], "feedback": []}
MAX_FAILURES_PER_CHECK = 20


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Memory:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return {**json.loads(json.dumps(EMPTY)), **data}
        return json.loads(json.dumps(EMPTY))

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, self.path)

    def reset(self) -> None:
        self.data = json.loads(json.dumps(EMPTY))
        self.save()

    # ---- reads --------------------------------------------------------------------
    def active_guidelines(self) -> list[dict]:
        return [g for g in self.data["guidelines"] if g.get("active", True)]

    def guideline_texts(self) -> list[str]:
        return [g["text"] for g in self.active_guidelines()]

    def learned_checks(self) -> list[dict]:
        return self.data["learned_checks"]

    # ---- writes -------------------------------------------------------------------
    def record_evaluation(self, results: list[dict], run_id: str, attempt: int) -> None:
        for r in results:
            st = self.data["check_stats"].setdefault(r["check_id"], {"evaluated": 0, "failed": 0, "first_draft_failed": 0})
            st["evaluated"] += 1
            if not r["passed"]:
                st["failed"] += 1
                if attempt == 1:
                    st["first_draft_failed"] += 1
                log = self.data["failures"].setdefault(r["check_id"], [])
                log.append({"run_id": run_id, "attempt": attempt, "evidence": r["evidence"][:4], "fix": r["fix"]})
                del log[:-MAX_FAILURES_PER_CHECK]

    def record_run(self, summary: dict) -> None:
        self.data["runs"].append(summary)

    def add_guideline(self, text: str, source: str, check_id: str | None) -> dict:
        g = {"id": f"G{len(self.data['guidelines']) + 1}", "text": text, "source": source,
             "check_id": check_id, "created": now(), "hits": 1, "active": True}
        self.data["guidelines"].append(g)
        return g

    def bump_guideline(self, gid: str) -> None:
        for g in self.data["guidelines"]:
            if g["id"] == gid:
                g["hits"] += 1

    def enforce_guideline_cap(self, cap: int) -> None:
        """Keep the prompt short: retire the least-used learned guidelines beyond the cap."""
        active = sorted(self.active_guidelines(), key=lambda g: (g["source"] == "human", g["hits"]), reverse=True)
        for g in active[cap:]:
            g["active"] = False

    def add_learned_check(self, check: dict) -> dict:
        check = {"id": f"H{len(self.data['learned_checks']) + 1}_{check['name'].upper().replace(' ', '_')[:20]}",
                 **check}
        self.data["learned_checks"].append(check)
        return check

    def add_feedback(self, text: str, kind: str) -> None:
        self.data["feedback"].append({"text": text, "kind": kind, "created": now()})

"""Self-evolution: turn repeated failures and human feedback into lasting changes.

Two levers, both persisted in memory:
  1. Generator prompt  - checks that keep failing produce a preventive guideline that
     is injected into every future generate/revise prompt ("lessons learned").
  2. Rubric            - human feedback can be turned into a brand-new pass/fail check,
     so a problem the rubric missed once is caught automatically from then on.
"""
from __future__ import annotations

from .llm import LLM, LLMError
from .memory import Memory
from .prompts import FEEDBACK_TO_CHECK_SYSTEM, LEARNER_SYSTEM, learner_prompt
from .schemas import GuidelineDecision, NewCheck


def learn_from_run(memory: Memory, rubric: list, failed_ids: set[str], llm: LLM,
                   min_failures: int, cap: int) -> list[str]:
    """Called after every run. Returns human-readable notes on what was learned."""
    notes = []
    by_id = {c.id: c for c in rubric}
    for check_id in sorted(failed_ids):
        stats = memory.data["check_stats"].get(check_id, {})
        if stats.get("failed", 0) < min_failures or check_id not in by_id:
            continue  # one-off failures are noise; only repeated ones change the prompt
        failures = memory.data["failures"].get(check_id, [])
        try:
            d = llm.structured(LEARNER_SYSTEM,
                               learner_prompt(by_id[check_id].to_dict(), failures, memory.active_guidelines()),
                               GuidelineDecision, role="evaluator")
        except LLMError as e:
            notes.append(f"{check_id}: learner skipped ({e})")
            continue
        if d.action == "duplicate" and d.duplicate_of:
            memory.bump_guideline(d.duplicate_of)
            notes.append(f"{check_id}: reinforced existing guideline {d.duplicate_of}")
        elif d.guideline.strip():
            g = memory.add_guideline(d.guideline.strip(), source="learned", check_id=check_id)
            notes.append(f"{check_id}: new guideline {g['id']} -> {g['text']}")
    memory.enforce_guideline_cap(cap)
    return notes


def add_human_feedback(memory: Memory, text: str, as_check: bool, llm: LLM | None) -> str:
    if not as_check:
        memory.add_feedback(text, "guideline")
        g = memory.add_guideline(text, source="human", check_id=None)
        return f"Added human guideline {g['id']}: {text}"
    if llm is None:
        raise ValueError("An LLM is needed to turn feedback into a check.")
    nc = llm.structured(FEEDBACK_TO_CHECK_SYSTEM, f"Reviewer comment:\n{text}", NewCheck, role="evaluator")
    memory.add_feedback(text, "check")
    c = memory.add_learned_check(nc.model_dump())
    return f"Added rubric check {c['id']}: {c['criterion']}"

"""Runs the full rubric against one lesson draft.

Rule checks run in-process; LLM checks run in parallel, one narrow call per check.
One-call-per-check costs more than a single "grade everything" call, but each judge
sees one question, so verdicts don't bleed into each other and a failure is traceable
to exactly one criterion.

The judge is treated as an unreliable witness, whatever model it is:
  * it verifies a fixed list of concrete items, and the verdict is computed in code
    from those items (a holistic "looks fine" cannot override an unmet item);
  * every item must be answered; skipped items are asked again, then count as unmet;
  * items that need proof only pass with a quote that is really in the lesson, and
    extra problems the judge raises only count if their quote is really in the lesson;
  * long item lists are split into batches so small models don't skim the tail;
  * optionally several independent samples vote per item (JUDGE_VOTES).
"""
from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from .llm import LLM, LLMError
from .prompts import JUDGE_SYSTEM, judge_prompt
from .rubric import Check
from .rules import (ABSOLUTE_RE, RULES, RULES_WITH_REFERENCE, find_jargon, grounded, repeated_definitions, technical_claims,
                    undefined_at_first_use)
from .schemas import ItemCheck, JudgeVerdict

_BATCH = 40  # max items per judge call


@dataclass
class Item:
    text: str
    proof: bool = False  # met=true only counts with a quote that is found in the lesson


def _result(check: Check, passed: bool, evidence: list[str], fix: str, reasoning: str = "",
            metrics: dict | None = None) -> dict:
    return {
        "check_id": check.id, "name": check.name, "dimension": check.dimension, "kind": check.kind,
        "criterion": check.criterion, "source": check.source,
        "passed": passed, "evidence": evidence, "fix": fix, "reasoning": reasoning, "metrics": metrics or {},
    }


# Each LLM check is decomposed into concrete items. The judge verifies items one by one
# (with quotes) and the verdict is computed from them in code.
_STATIC_ITEMS = {
    "L4_EXAMPLES": [
        Item("There is an everyday analogy a young Indian learner would recognise.", True),
        Item("The analogy is mapped to the topic correctly (each part of the analogy matches a real part of the "
             "topic, and nothing in the mapping is wrong).", True),
        Item("There is a worked example that follows ONE concrete case (one question, one situation, one input) "
             "from start to finish.", True),
        Item("The worked example goes through EVERY step listed in the 'How does it work?' section, in the same "
             "order, applied to that one case (name any step it skips).", True),
        Item("The worked example ends with the concrete result for that case.", True),
    ],
    "L5_LEARNER_FIT": [
        Item("No English idioms, slang or figures of speech (quote any you find)."),
        Item("No uncommon or formal English words where an everyday word would do (quote any you find)."),
        Item("No assumed knowledge of coding, advanced maths or AI beyond what the lesson itself explains."),
        Item("Grammar is correct and simple, e.g. no verb used where a noun is needed, no wrong word form "
             "(quote any grammar mistakes)."),
        Item("The tone is warm, encouraging and speaks to the learner as 'you'."),
    ],
    "L6_FLOW": [
        Item("Sections follow the planned order: what you will learn -> before we start (the prerequisite) -> "
             "what is it -> why -> how -> example -> limits -> recap -> check yourself -> key words -> learn more. "
             "(This order is required; do not fail it for having the prerequisite before the definition.)"),
        Item("Every idea or term is introduced before it is used (quote any used before being introduced)."),
        Item("Each section connects to the previous one; there are no abrupt jumps."),
        Item("Nothing is repeated without purpose, and analogies are discussed where they are introduced."),
    ],
}

_EXTRA_NOTES = {
    "L1_ACCURACY": (
        "For items that quote a sentence: met=true only if the sentence is accurate according to the reference "
        "facts AND would not give a beginner a wrong belief. Words like always, never, stops, prevents, "
        "completely, guarantees make a sentence FALSE unless it is literally always true; check them against "
        "what the reference facts say about limits. Over-general claims about all AI models are also false. "
        "A true claim that the reference "
        "sheet simply doesn't mention is fine. Judge truth only: difficulty, jargon and style are checked by other "
        "reviewers. When such an item is met, the quote may be empty."),
}

# Checks whose item list fully defines them: extra problems the judge raises are ignored,
# so issues owned by other checks (e.g. a false claim) aren't double-reported here.
_EXHAUSTIVE = {"L2_COVERAGE"}


def _items_for(check: Check, lesson: str, reference: dict) -> list[Item]:
    if check.id == "L1_ACCURACY":
        claims = technical_claims(lesson)
        # Absolute-wording claims go first, each with the exact trigger word: small judges
        # read them as fine unless asked point-blank whether the absolute is literally true.
        flagged = [s for s, flag in claims if flag]
        return ([Item(f"ABSOLUTE CLAIM: \"{s}\" The word '{ABSOLUTE_RE.search(s).group(0)}' makes this an "
                      f"all-or-nothing claim. met=true ONLY if it is literally true with no exceptions according "
                      f"to the reference facts (check the facts about limits).")
                 for s in flagged]
                + [Item(f"The lesson does NOT state or imply: \"{m['wrong']}\"") for m in reference.get("misconceptions", [])]
                + [Item(f"Accurate, not overclaimed: \"{s}\"") for s, flag in claims if not flag]
                + [Item("Every technical claim NOT listed above agrees with the reference facts "
                        "(quote any claim that is false or misleading, even slightly).")])
    if check.id == "L2_COVERAGE":
        return [Item(f"[{m['id']}] is taught (explained, not just named): {m['point']}", True)
                for m in reference.get("must_cover", [])]
    if check.id == "L3_JARGON":
        found = find_jargon(lesson, reference.get("jargon", []))
        suspects = dict(undefined_at_first_use(lesson, found))
        return ([Item(f"'{t}' is explained in simple words at or before its FIRST use in the body. AUTOMATIC "
                      f"PRE-CHECK found no explanation in the sentence of first use: \"{suspects[t]}\". Mark met=true "
                      f"ONLY if you can quote an earlier explanation." if t in suspects else
                      f"'{t}' is explained in simple words at or before its FIRST use in the body", True) for t in found]
                + [Item("Every OTHER technical or uncommon word (not in this list) is explained at first use "
                        "(quote any that are not).")])
    if check.id == "L6_FLOW":
        found = find_jargon(lesson, reference.get("jargon", []))
        return _STATIC_ITEMS["L6_FLOW"] + [
            Item(f"'{t}' is explained {n} times in the body (AUTOMATIC PRE-CHECK). met=true only if every repeat "
                 f"adds something new; re-glossing the same meaning is padding.")
            for t, n in repeated_definitions(lesson, found)]
    return _STATIC_ITEMS.get(check.id, [Item(check.criterion)])


def _key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()[:40]


def _align(items: list[Item], got: list[ItemCheck]) -> tuple[list[ItemCheck | None], list[ItemCheck]]:
    """Match returned items to requested ones (by text, else by position); the rest are extras."""
    by_key: dict[str, int] = {}
    for j, g in enumerate(got):
        by_key.setdefault(_key(g.item), j)
    used, aligned = set(), []
    for i, it in enumerate(items):
        j = by_key.get(_key(it.text))
        if j is None or j in used:
            j = i if i < len(got) and i not in used else None
        aligned.append(None if j is None else got[j])
        used.add(j)
    return aligned, [g for j, g in enumerate(got) if j not in used]


def _ask(llm: LLM, check: Check, lesson: str, reference: dict, items: list[Item]):
    """One judge call over a batch of items. Re-asks once if the judge skipped items."""
    texts = [i.text for i in items]
    extra = _EXTRA_NOTES.get(check.id, "")
    v = llm.structured(JUDGE_SYSTEM, judge_prompt(check.to_dict(), lesson, reference, texts, extra),
                       JudgeVerdict, role="evaluator")
    aligned, extras = _align(items, v.items)
    if any(a is None for a in aligned):
        note = (f"{extra}\n\nIMPORTANT: answer EVERY item. Return exactly {len(items)} entries in `items`, one per "
                "numbered item, in order, copying each item's text into `item`.").strip()
        v2 = llm.structured(JUDGE_SYSTEM, judge_prompt(check.to_dict(), lesson, reference, texts, note),
                            JudgeVerdict, role="evaluator")
        a2, e2 = _align(items, v2.items)
        if sum(a is None for a in a2) < sum(a is None for a in aligned):
            v, aligned, extras = v2, a2, e2
    return v, aligned, extras


def _judge_once(llm: LLM, check: Check, lesson: str, reference: dict, items: list[Item]) -> dict:
    """One full sample: per-item (met, quote), grounded extra problems, reasoning, fix."""
    per_item, extras, reasoning, fixes, dropped = [], [], [], [], 0
    for start in range(0, len(items), _BATCH):
        batch = items[start:start + _BATCH]
        v, aligned, extra_items = _ask(llm, check, lesson, reference, batch)
        for it, a in zip(batch, aligned):
            if a is None:
                per_item.append((False, "(the judge did not check this item)"))
            elif a.met and it.proof and not (a.quote and grounded(a.quote, lesson)):
                per_item.append((False, f"(no proof: quote not found in the lesson) {a.quote}".strip()))
            else:
                per_item.append((a.met, a.quote))
        if check.id not in _EXHAUSTIVE:
            raised = [g.quote for g in extra_items if not g.met]
            if v.verdict == "FAIL":
                raised += v.evidence
            for q in raised:
                # A problem only counts if the judge can show where it is.
                if q and grounded(q, lesson):
                    extras.append(q)
                else:
                    dropped += 1
        reasoning.append(v.reasoning)
        if v.fix:
            fixes.append(v.fix)
    return {"per_item": per_item, "extras": extras, "reasoning": " ".join(reasoning),
            "fix": " ".join(fixes), "dropped": dropped}


def _run_llm_check(llm: LLM, check: Check, lesson: str, reference: dict, votes: int = 1) -> dict:
    items = _items_for(check, lesson, reference)
    try:
        samples = [_judge_once(llm, check, lesson, reference, items) for _ in range(votes)]
    except LLMError as e:
        # A judge that cannot answer must not let content through.
        return _result(check, False, [f"Judge error: {e}"], "Re-run evaluation.", "judge failed")

    evidence = []
    for i, it in enumerate(items):
        answers = [s["per_item"][i] for s in samples]
        unmet = [q for met, q in answers if not met]
        if 2 * len(unmet) >= votes:  # majority, ties fail
            quote = next((q for q in unmet if q), "")
            evidence.append(f"{it.text} -> \"{quote}\"" if quote else f"{it.text} -> (not found)")
    extras = list(dict.fromkeys(q for s in samples for q in s["extras"]))
    evidence += [f"Other problem -> \"{q}\"" for q in extras]
    passed = not evidence
    fix = next((s["fix"] for s in samples if s["fix"]), "") or ("" if passed else "Fix each unmet item listed in the evidence.")
    return _result(check, passed, evidence, "" if passed else fix, samples[0]["reasoning"],
                   metrics={"items_checked": len(items), "items_unmet": len(evidence) - len(extras),
                            "extra_problems": len(extras), "ungrounded_dropped": sum(s["dropped"] for s in samples),
                            "votes": votes})


def evaluate(lesson: str, rubric: list[Check], reference: dict, llm: LLM, concurrency: int = 4,
             votes: int = 1) -> list[dict]:
    results: dict[str, dict] = {}
    for check in rubric:
        if check.kind == "rule":
            fn = RULES_WITH_REFERENCE.get(check.id)
            passed, evidence, fix, metrics = fn(lesson, reference) if fn else RULES[check.id](lesson)
            results[check.id] = _result(check, passed, evidence, fix, metrics=metrics)

    llm_checks = [c for c in rubric if c.kind == "llm"]
    with ThreadPoolExecutor(max_workers=max(1, concurrency)) as pool:
        for res in pool.map(lambda c: _run_llm_check(llm, c, lesson, reference, votes), llm_checks):
            results[res["check_id"]] = res
    return [results[c.id] for c in rubric]


def summarize(results: list[dict]) -> str:
    passed = sum(r["passed"] for r in results)
    fails = [r["check_id"] for r in results if not r["passed"]]
    return f"{passed}/{len(results)} passed" + (f" | FAILED: {', '.join(fails)}" if fails else "")

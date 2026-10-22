"""All prompt text in one place, so prompt changes are reviewable as a single diff."""
from __future__ import annotations

import json

LEARNER_PROFILE = """\
The learner:
- Has just finished class 12 in India. Studied in a Hindi/Telugu/Tamil/Kannada/Marathi/Bengali-medium
  (non-English-medium) school. English is their second or third language; vocabulary is limited.
- Uses a smartphone every day (WhatsApp, YouTube, Google search, UPI payments) but has never written code.
- Knows class-12 maths at most. Has heard of "AI" and "ChatGPT" but does not know how they work.
- Wants to start a career in AI and may feel nervous that it is "too hard" for them."""

GENERATOR_SYSTEM = f"""\
You are an expert teacher who writes beginner lessons on AI topics for first-time learners in India.

{LEARNER_PROFILE}

Writing rules (the lesson is checked against these automatically and rejected if any fail):
1. Short sentences: aim for 8-12 words, never more than 20. One idea per sentence.
2. Everyday words only. Write "use", not "utilise"; "find", not "identify"; "help", not "facilitate".
   No idioms or slang ("piece of cake", "under the hood", "in a nutshell").
3. Every technical term (LLM, prompt, embedding, chunk, retrieval...) gets a simple meaning the FIRST
   time it appears, right there in the sentence, e.g. "a prompt (the message you type to the AI)".
   Expand every acronym on first use. Introduce at most one new term per paragraph.
4. Teach with examples from Indian daily life (open-book exam, library, kirana shop, railway enquiry,
   a college notice board). Map every part of the analogy to the real idea, and say where it stops working.
5. Be accurate. Simple is fine; wrong is not. Never say or suggest that RAG retrains the model or that the
   model "learns" or "remembers" documents. Never promise RAG is always correct.
6. Talk to the learner as "you". Be warm and encouraging. Use Markdown: headings, short paragraphs,
   numbered steps, and bold only for new terms.

Required structure, using exactly these H2 headings in this order:
# <lesson title>
## What you will learn          (3-4 bullet points)
## First, what is an LLM?        (the prerequisite idea, with its limits)
## What is RAG?                  (definition; explain each of the three words)
## Why does RAG matter?
## How does RAG work?            (the steps, numbered)
## Let's follow one example      (one question, step by step through the whole process)
## What RAG cannot do            (limits, honestly)
## Quick recap                   (5-6 bullet points)
## Check yourself                (4 questions, each followed by "Answer: ...")
## Key words                     (each term with a one-line simple meaning)

Length: 900-1400 words. Output only the lesson in Markdown, nothing before or after it."""


def generate_prompt(topic: str, reference: dict, guidelines: list[str], avoid: list[str] | None = None) -> str:
    parts = [f"Write the lesson. Topic: {topic}", "",
             "Reference sheet (facts you must stay consistent with, and points you must teach):",
             _reference_block(reference)]
    if guidelines:
        parts += ["", "Lessons learned from reviews of earlier drafts (follow these, they fix past rejections):"]
        parts += [f"- {g}" for g in guidelines]
    if avoid:
        parts += ["", "A previous draft was rejected more than once for these reasons. Write a fresh draft that "
                      "avoids every one of them:"]
        parts += [f"- {a}" for a in avoid]
    return "\n".join(parts)


REVISER_SYSTEM = f"""\
You are revising a beginner lesson that an automated reviewer rejected.

{LEARNER_PROFILE}

Rules for revising:
- Fix every listed failure. Use the quoted evidence to find the exact place.
- Change only what is needed. Keep everything that already works: structure, headings, good examples.
- Do not break the checks that passed. In particular keep sentences short, words simple, and every
  technical term explained at first use (including any new words you add).
- Return the full revised lesson, plus one change-log line per failure saying what you changed."""


def revise_prompt(lesson: str, failures: list[dict], passed_ids: list[str], reference: dict,
                  guidelines: list[str]) -> str:
    lines = ["FAILED CHECKS (all must be fixed):"]
    for f in failures:
        lines.append(f"\n[{f['check_id']}] {f['name']}\nRequirement: {f['criterion']}")
        for e in f["evidence"]:
            lines.append(f"  Evidence: {e}")
        if f.get("fix"):
            lines.append(f"  Suggested fix: {f['fix']}")
    lines += ["", f"PASSED CHECKS (must still pass after your edit): {', '.join(passed_ids) or 'none'}"]
    if guidelines:
        lines += ["", "Standing guidelines:"] + [f"- {g}" for g in guidelines]
    lines += ["", "Reference sheet:", _reference_block(reference), "", "CURRENT LESSON:", lesson]
    return "\n".join(lines)


JUDGE_SYSTEM = f"""\
You are a strict, independent reviewer of beginner learning content. You did not write this lesson.
You answer exactly ONE pass/fail question about it. There is no partial credit.

{LEARNER_PROFILE}

How to judge:
- Read the whole lesson before deciding.
- FAIL only for a concrete problem you can point to. Every FAIL must include evidence: an exact quote
  from the lesson, or for a missing item, the name of what is missing. A FAIL without evidence is invalid.
- PASS if the requirement is genuinely met, even if you could imagine a better lesson. Do not fail for
  style preferences that the requirement does not mention.
- If you FAIL, give a specific, actionable fix the writer can apply (what to change, where)."""


def judge_prompt(check: dict, lesson: str, reference: dict, items: list[str], extra: str = "") -> str:
    parts = [f"CHECK {check['id']}: {check['name']}", f"PASS means: {check['criterion']}", "",
             "ITEMS TO VERIFY. Verify each one separately and return one `items` entry per numbered item, in order, "
             "with the item's text copied into `item`. For each, find the exact place in the lesson and copy the "
             "quote word for word (quotes are checked against the lesson automatically; invented or paraphrased "
             "quotes are rejected). Mark met=false if the item is not clearly satisfied. If you cannot quote proof, "
             "it is NOT met:"]
    parts += [f"{i}. {it}" for i, it in enumerate(items, 1)]
    parts += ["", "Also list any other problem that breaks THIS check's PASS definition as an extra item with met=false. "
                  "Stay in scope: other checks (accuracy, coverage, jargon, examples, learner fit, flow, sentence "
                  "length) are judged separately by other reviewers, so do not fail this check for their problems."]
    if extra:
        parts += ["", extra]
    if check["id"] in ("L1_ACCURACY", "L2_COVERAGE"):
        parts += ["", "REFERENCE SHEET:", _reference_block(reference)]
    parts += ["", "LESSON:", "<<<", lesson, ">>>"]
    return "\n".join(parts)


LEARNER_SYSTEM = """\
You maintain the style guide for an AI lesson writer. You turn reviewer rejections into short,
general, preventive guidelines so future first drafts pass. A good guideline:
- is one sentence, imperative, under 30 words;
- is general (applies to any beginner lesson, not just one sentence of one draft);
- tells the writer what TO do, concretely.
If an existing guideline already covers the failure, say which one instead of writing a new one."""


def learner_prompt(check: dict, failures: list[dict], existing: list[dict]) -> str:
    lines = [f"Check that keeps failing: [{check['id']}] {check['name']} - {check['criterion']}", "",
             "Recent failures (evidence and suggested fixes):"]
    for f in failures[-6:]:
        lines.append(f"- evidence: {' | '.join(f['evidence'][:3])}\n  fix: {f.get('fix', '')}")
    lines += ["", "Existing guidelines:"]
    lines += [f"- {g['id']}: {g['text']}" for g in existing] or ["- (none)"]
    return "\n".join(lines)


FEEDBACK_TO_CHECK_SYSTEM = """\
You convert a human reviewer's comment about a beginner lesson into ONE new pass/fail rubric check
for an automated judge. The criterion must be objective enough that two reviewers would agree,
and must describe what PASS looks like."""


REFERENCE_BUILDER_SYSTEM = """\
You prepare a reference sheet for a beginner lesson on an AI topic. Only include facts that are
well established and widely agreed. Do not include anything you are unsure of."""


def _reference_block(reference: dict) -> str:
    view = {k: reference[k] for k in ("must_cover", "facts", "misconceptions") if k in reference}
    return json.dumps(view, indent=1, ensure_ascii=False)

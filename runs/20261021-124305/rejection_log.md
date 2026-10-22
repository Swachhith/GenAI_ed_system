# Rejection log: Introduction to RAG (Retrieval-Augmented Generation)

- **Run:** `20261021-124305`
- **Status:** ✅ PASSED, shipped
- **Shipped attempt:** 2 of 2 (retry budget: 2)
- **Generator:** `gemini-3.5-flash-lite` | **Evaluator:** `gemini-3.5-flash-lite`
- **Grounding:** reference sheet `rag.json` (trust: curated)
- **Learned guidelines in the prompt at start:** 0

## Summary

| Attempt | How produced | Result | Failed checks |
|---|---|---|---|
| 1 | generate | FAIL (10/11) | R2_SENTENCES |
| 2 | revise | PASS (11/11) | - |

## Attempt 1 (generate): FAIL

**What failed and why:**

- **R2_SENTENCES: Short sentences** _(beginner-friendly language, rule check)_
  - Requirement: Average sentence length <= 15 words AND no sentence longer than 25 words.
  - Evidence: (26 words) The LLM reads the added paragraph and replies: "The last date to get a full hostel fee refund is July 15." This is the Generation step.
  - Fix requested: Split every sentence longer than 25 words into two or three short sentences. One idea per sentence.

## Attempt 2 (revise): PASS

**What changed in this draft (in response to the previous rejection):**
- `R2_SENTENCES`: Split the long sentence describing the LLM reply into three short sentences to ensure no sentence exceeds 25 words.
- Diff vs previous draft: +1 / -1 lines (`attempt_2.diff`)

All checks passed.

## Final scorecard (shipped attempt)

| Check | Dimension | Result | Metrics |
|---|---|---|---|
| R1_STRUCTURE Required sections present | coherent teaching flow | PASS |  |
| R2_SENTENCES Short sentences | beginner-friendly language | PASS | avg_sentence_words=11.5, sentences=80, over_cap=0 |
| R3_READABILITY Plain-English readability | beginner-friendly language | PASS | flesch=74.4 |
| R4_LENGTH Right length for one sitting | covers the key points | PASS | word_count=971 |
| R5_QUIZ Self-check with answers | teaches by example | PASS | quiz_questions=4, quiz_has_answers=True |
| L1_ACCURACY No false or misleading claims | accurate & grounded | PASS |  |
| L2_COVERAGE All must-cover points taught | covers the key points | PASS |  |
| L3_JARGON Every technical term explained | clear, no unexplained jargon | PASS |  |
| L4_EXAMPLES Concrete analogy and walk-through | teaches by example | PASS |  |
| L5_LEARNER_FIT Fits a non-native English beginner | beginner-friendly language | PASS |  |
| L6_FLOW Builds step by step | coherent teaching flow | PASS |  |

## What the system learned from this run

- No check has failed often enough to change the prompt yet.

Active guidelines now in memory: 0 | learned rubric checks: 0

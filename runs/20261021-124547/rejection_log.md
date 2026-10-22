# Rejection log: Introduction to RAG (Retrieval-Augmented Generation)

- **Run:** `20261021-124547`
- **Status:** ✅ PASSED, shipped
- **Shipped attempt:** 2 of 2 (retry budget: 2)
- **Generator:** `gemini-3.5-flash-lite` | **Evaluator:** `gemini-3.5-flash-lite`
- **Grounding:** reference sheet `rag.json` (trust: curated)
- **Learned guidelines in the prompt at start:** 0

## Summary

| Attempt | How produced | Result | Failed checks |
|---|---|---|---|
| 1 | generate | FAIL (10/11) | L3_JARGON |
| 2 | revise | PASS (11/11) | - |

## Attempt 1 (generate): FAIL

**What failed and why:**

- **L3_JARGON: Every technical term explained** _(clear, no unexplained jargon, llm check)_
  - Requirement: Every technical or English-uncommon term is explained in simple words at or before its first use in the body (a glossary at the end alone does not count). Acronyms are expanded on first use.
  - Evidence: 'weights' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "It does not change the model weights or retrain the model.". Mark met=true ONLY if you can quote an earlier explanation. -> "It does not change the model weights or retrain the model."
  - Evidence: It does not change the model weights or retrain the model.
  - Judge reasoning: I checked every technical term against the text to see if it was clearly explained at or before its first appearance. Most terms like LLM, chunk, embedding, and hallucination are successfully defined in context. However, the term 'weights' is used without any simple definition or explanation of what model weights are.
  - Fix requested: Add a simple explanation for 'weights' before or right when it is first used in the text, such as: 'It does not change the internal numbers (called model weights) that the AI uses to make decisions.'

## Attempt 2 (revise): PASS

**What changed in this draft (in response to the previous rejection):**
- `L3_JARGON`: Added a simple definition for 'weights' ('internal numbers (called model weights)') right where it is first used in the text.
- Diff vs previous draft: +1 / -1 lines (`attempt_2.diff`)

All checks passed.

## Final scorecard (shipped attempt)

| Check | Dimension | Result | Metrics |
|---|---|---|---|
| R1_STRUCTURE Required sections present | coherent teaching flow | PASS |  |
| R2_SENTENCES Short sentences | beginner-friendly language | PASS | avg_sentence_words=10.9, sentences=79, over_cap=0 |
| R3_READABILITY Plain-English readability | beginner-friendly language | PASS | flesch=71.7 |
| R4_LENGTH Right length for one sitting | covers the key points | PASS | word_count=906 |
| R5_QUIZ Self-check with answers | teaches by example | PASS | quiz_questions=4, quiz_has_answers=True |
| L1_ACCURACY No false or misleading claims | accurate & grounded | PASS | items_checked=8, items_unmet=0 |
| L2_COVERAGE All must-cover points taught | covers the key points | PASS | items_checked=9, items_unmet=0 |
| L3_JARGON Every technical term explained | clear, no unexplained jargon | PASS | items_checked=24, items_unmet=0 |
| L4_EXAMPLES Concrete analogy and walk-through | teaches by example | PASS | items_checked=6, items_unmet=0 |
| L5_LEARNER_FIT Fits a non-native English beginner | beginner-friendly language | PASS | items_checked=5, items_unmet=0 |
| L6_FLOW Builds step by step | coherent teaching flow | PASS | items_checked=4, items_unmet=0 |

## What the system learned from this run

- No check has failed often enough to change the prompt yet.

Active guidelines now in memory: 0 | learned rubric checks: 0

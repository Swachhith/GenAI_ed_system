# Rejection log: Introduction to RAG

- **Run:** `20261022-102658`
- **Status:** ✅ PASSED, shipped
- **Shipped attempt:** 3 of 3 (retry budget: 2)
- **Generator:** `gemini:gemini-3.5-flash-lite` | **Evaluator:** `gemini:gemini-3.5-flash-lite` (judge votes: 1)
- **Grounding:** reference sheet `rag.json` (trust: curated)
- **Learned guidelines in the prompt at start:** 6
- **Web research:** 9 learning resources verified live; 0 fresh facts from 5 web sources

## Summary

| Attempt | How produced | Result | Failed checks |
|---|---|---|---|
| 1 | generate | FAIL (11/12) | L3_JARGON |
| 2 | revise | FAIL (11/12) | L3_JARGON |
| 3 | regenerate | PASS (12/12) | - |

## Attempt 1 (generate): FAIL

**What failed and why:**

- **L3_JARGON: Every technical term explained** _(clear, no unexplained jargon, llm check)_
  - Requirement: Every technical or English-uncommon term is explained in simple words at or before its first use in the body (a glossary at the end alone does not count). Acronyms are expanded on first use.
  - Evidence: 'chunking' is explained in simple words at or before its FIRST use in the body -> "(no proof: quote not found in the lesson)"
  - Judge reasoning: I checked every listed technical term and found that all of them are either defined explicitly in the text near their first appearance or their contextual use effectively clarifies their meaning for a beginner.
  - Fix requested: Fix each unmet item listed in the evidence.

## Attempt 2 (revise): FAIL

**What changed in this draft (in response to the previous rejection):**
- `L3_JARGON`: Added an explicit definition of 'chunk' right before its first use in the worked example section.
- Diff vs previous draft: +3 / -3 lines (`attempt_2.diff`)

**What failed and why:**

- **L3_JARGON: Every technical term explained** _(clear, no unexplained jargon, llm check)_
  - Requirement: Every technical or English-uncommon term is explained in simple words at or before its first use in the body (a glossary at the end alone does not count). Acronyms are expanded on first use.
  - Evidence: 'chunking' is explained in simple words at or before its FIRST use in the body -> "(no proof: quote not found in the lesson)"
  - Judge reasoning: I checked every technical term listed against the text. All technical terms like LLM, RAG, embeddings, chunks, and context window are clearly defined right before or at their first introduction. The lesson takes care to explain terms in plain words suited for a beginner.
  - Fix requested: Fix each unmet item listed in the evidence.

## Attempt 3 (regenerate): PASS

**What changed in this draft (in response to the previous rejection):**
- `L3_JARGON`: Targeted edits failed twice, so the lesson was rewritten from scratch with this failure given as an explicit constraint.

All checks passed.

## Final scorecard (shipped attempt)

| Check | Dimension | Result | Metrics |
|---|---|---|---|
| R1_STRUCTURE Required sections present | coherent teaching flow | PASS |  |
| R2_SENTENCES Short sentences | beginner-friendly language | PASS | avg_sentence_words=11.0, sentences=112, over_cap=0 |
| R3_READABILITY Plain-English readability | beginner-friendly language | PASS | flesch=72.2 |
| R4_LENGTH Right length for one sitting | covers the key points | PASS | word_count=1277 |
| R5_QUIZ Self-check with answers | teaches by example | PASS | quiz_questions=4, quiz_has_answers=True |
| R6_RESOURCES Verified links to learn more | teaches by example | PASS | links=4, verified_used=4, videos=2 |
| L1_ACCURACY No false or misleading claims | accurate & grounded | PASS | items_checked=110, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L2_COVERAGE All must-cover points taught | covers the key points | PASS | items_checked=9, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L3_JARGON Every technical term explained | clear, no unexplained jargon | PASS | items_checked=27, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L4_EXAMPLES Concrete analogy and walk-through | teaches by example | PASS | items_checked=5, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L5_LEARNER_FIT Fits a non-native English beginner | beginner-friendly language | PASS | items_checked=5, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L6_FLOW Builds step by step | coherent teaching flow | PASS | items_checked=5, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |

## What the system learned from this run

- L3_JARGON: reinforced existing guideline G3

Active guidelines now in memory: 6 | learned rubric checks: 0

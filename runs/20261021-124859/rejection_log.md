# Rejection log: Introduction to RAG (Retrieval-Augmented Generation)

- **Run:** `20261021-124859`
- **Status:** ✅ PASSED, shipped
- **Shipped attempt:** 3 of 3 (retry budget: 2)
- **Generator:** `gemini-3.5-flash-lite` | **Evaluator:** `gemini-3.5-flash-lite`
- **Grounding:** reference sheet `rag.json` (trust: curated)
- **Learned guidelines in the prompt at start:** 0

## Summary

| Attempt | How produced | Result | Failed checks |
|---|---|---|---|
| 1 | generate | FAIL (10/11) | L4_EXAMPLES |
| 2 | revise | FAIL (10/11) | R2_SENTENCES |
| 3 | revise | PASS (11/11) | - |

## Attempt 1 (generate): FAIL

**What failed and why:**

- **L4_EXAMPLES: Concrete analogy and walk-through** _(teaches by example, llm check)_
  - Requirement: The lesson has (a) at least one everyday analogy a young Indian learner would recognise, correctly mapped to RAG, AND (b) one concrete worked example that follows a single question through every step: preparing documents, retrieving, adding to the prompt, generating.
  - Evidence: The worked example shows how the documents were prepared (collected, split into chunks, stored) before the question was asked. -> (not found)
  - Evidence: The worked example shows how the documents were prepared (collected, split into chunks, stored) before the question was asked.
  - Judge reasoning: I checked the lesson for an everyday Indian learner analogy, its mapping, and the concrete worked example following a single question. While the analogy, retrieval, augmentation, and generation steps are present in the worked example, the worked example completely skips showing how the documents were prepared (collected, split into chunks, stored) prior to the question being asked.
  - Fix requested: In the section 'Let's follow one example', add sentences right at the beginning showing the preparation phase for that specific library rulebook (e.g., collecting the rulebook, splitting it into chunks like the late fee rule, and storing them) before introducing the question.

## Attempt 2 (revise): FAIL

**What changed in this draft (in response to the previous rejection):**
- `L4_EXAMPLES`: Added sentences at the beginning of the example section showing how the library rulebook is collected, split into chunks, and stored before the question is asked.
- Diff vs previous draft: +2 / -1 lines (`attempt_2.diff`)

**What failed and why:**

- **R2_SENTENCES: Short sentences** _(beginner-friendly language, rule check)_
  - Requirement: Average sentence length <= 15 words AND no sentence longer than 25 words.
  - Evidence: (34 words) Before any student asks a question, the system prepares the documents: it collects the college library rulebook, splits it into small chunks like the late fee rule, and stores those chunks in its database.
  - Fix requested: Split every sentence longer than 25 words into two or three short sentences. One idea per sentence.

## Attempt 3 (revise): PASS

**What changed in this draft (in response to the previous rejection):**
- `R2_SENTENCES`: Split the long 34-word sentence about preparing documents into three shorter sentences to ensure no sentence exceeds 25 words.
- Diff vs previous draft: +1 / -1 lines (`attempt_3.diff`)

All checks passed.

## Final scorecard (shipped attempt)

| Check | Dimension | Result | Metrics |
|---|---|---|---|
| R1_STRUCTURE Required sections present | coherent teaching flow | PASS |  |
| R2_SENTENCES Short sentences | beginner-friendly language | PASS | avg_sentence_words=11.6, sentences=80, over_cap=0 |
| R3_READABILITY Plain-English readability | beginner-friendly language | PASS | flesch=71.8 |
| R4_LENGTH Right length for one sitting | covers the key points | PASS | word_count=974 |
| R5_QUIZ Self-check with answers | teaches by example | PASS | quiz_questions=4, quiz_has_answers=True |
| L1_ACCURACY No false or misleading claims | accurate & grounded | PASS | items_checked=8, items_unmet=0 |
| L2_COVERAGE All must-cover points taught | covers the key points | PASS | items_checked=9, items_unmet=0 |
| L3_JARGON Every technical term explained | clear, no unexplained jargon | PASS | items_checked=22, items_unmet=0 |
| L4_EXAMPLES Concrete analogy and walk-through | teaches by example | PASS | items_checked=6, items_unmet=0 |
| L5_LEARNER_FIT Fits a non-native English beginner | beginner-friendly language | PASS | items_checked=5, items_unmet=0 |
| L6_FLOW Builds step by step | coherent teaching flow | PASS | items_checked=4, items_unmet=0 |

## What the system learned from this run

- R2_SENTENCES: new guideline G1 -> Keep every sentence under twenty-five words by expressing only one idea per sentence.

Active guidelines now in memory: 1 | learned rubric checks: 0

# Rejection log: Introduction to RAG (Retrieval-Augmented Generation)

- **Run:** `20261021-125136`
- **Status:** ✅ PASSED, shipped
- **Shipped attempt:** 2 of 2 (retry budget: 2)
- **Generator:** `gemini-3.5-flash-lite` | **Evaluator:** `gemini-3.5-flash-lite`
- **Grounding:** reference sheet `rag.json` (trust: curated)
- **Learned guidelines in the prompt at start:** 1

## Summary

| Attempt | How produced | Result | Failed checks |
|---|---|---|---|
| 1 | generate | FAIL (10/11) | L4_EXAMPLES |
| 2 | revise | PASS (11/11) | - |

## Attempt 1 (generate): FAIL

**What failed and why:**

- **L4_EXAMPLES: Concrete analogy and walk-through** _(teaches by example, llm check)_
  - Requirement: The lesson has (a) at least one everyday analogy a young Indian learner would recognise, correctly mapped to RAG, AND (b) one concrete worked example that follows a single question through every step: preparing documents, retrieving, adding to the prompt, generating.
  - Evidence: 3. The worked example shows how the documents were prepared (collected, split into chunks, stored) before the question was asked. -> (not found)
  - Evidence: Item 3: The worked example shows how the documents were prepared (collected, split into chunks, stored) before the question was asked.
  - Judge reasoning: I checked the lesson for an Indian student-friendly analogy, correct mapping, and a full worked example covering preparation, retrieval, augmentation, and generation. Items 1, 2, 4, 5, and 6 are clearly satisfied by the open-book exam analogy and the college attendance rulebook example. However, item 3 fails because the worked example skips the preparation phase (collecting, splitting into chunks, and storing) before the question is asked, jumping straight from asking the question to searching the chunks.
  - Fix requested: In the section 'Let's follow one example', add a brief sentence at the beginning showing the preparation phase before the question is asked, such as: 'Before you ask, the college rulebook is collected and split into small chunks stored in a database.'

## Attempt 2 (revise): PASS

**What changed in this draft (in response to the previous rejection):**
- `L4_EXAMPLES`: Added a sentence to the example section showing how documents are collected and split into chunks and stored before any question is asked.
- Diff vs previous draft: +1 / -1 lines (`attempt_2.diff`)

All checks passed.

## Final scorecard (shipped attempt)

| Check | Dimension | Result | Metrics |
|---|---|---|---|
| R1_STRUCTURE Required sections present | coherent teaching flow | PASS |  |
| R2_SENTENCES Short sentences | beginner-friendly language | PASS | avg_sentence_words=10.6, sentences=67, over_cap=0 |
| R3_READABILITY Plain-English readability | beginner-friendly language | PASS | flesch=71.6 |
| R4_LENGTH Right length for one sitting | covers the key points | PASS | word_count=758 |
| R5_QUIZ Self-check with answers | teaches by example | PASS | quiz_questions=4, quiz_has_answers=True |
| L1_ACCURACY No false or misleading claims | accurate & grounded | PASS | items_checked=8, items_unmet=0 |
| L2_COVERAGE All must-cover points taught | covers the key points | PASS | items_checked=9, items_unmet=0 |
| L3_JARGON Every technical term explained | clear, no unexplained jargon | PASS | items_checked=17, items_unmet=0 |
| L4_EXAMPLES Concrete analogy and walk-through | teaches by example | PASS | items_checked=6, items_unmet=0 |
| L5_LEARNER_FIT Fits a non-native English beginner | beginner-friendly language | PASS | items_checked=5, items_unmet=0 |
| L6_FLOW Builds step by step | coherent teaching flow | PASS | items_checked=4, items_unmet=0 |

## What the system learned from this run

- L4_EXAMPLES: new guideline G2 -> Explicitly show document collection, chunking, and storage as the first step of your worked example before introducing the user's question.

Active guidelines now in memory: 2 | learned rubric checks: 0

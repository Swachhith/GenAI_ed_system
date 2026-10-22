# Rejection log: Introduction to RAG (Retrieval-Augmented Generation)

- **Run:** `20261021-124748`
- **Status:** ✅ PASSED, shipped
- **Shipped attempt:** 3 of 3 (retry budget: 2)
- **Generator:** `gemini-3.5-flash-lite` | **Evaluator:** `gemini-3.5-flash-lite`
- **Grounding:** reference sheet `rag.json` (trust: curated)
- **Learned guidelines in the prompt at start:** 0
- **Deliberate error injected into attempt 1:** `factual`: "Here is the secret: RAG works by retraining the AI model on your documents. After that, the model remembers them forever, so its answers are always correct."
- **Expected to be caught by:** L1_ACCURACY -> **caught by:** L1_ACCURACY

## Summary

| Attempt | How produced | Result | Failed checks |
|---|---|---|---|
| 1 | generate | FAIL (7/11) | L1_ACCURACY, L2_COVERAGE, L3_JARGON, L6_FLOW |
| 2 | revise | FAIL (10/11) | R2_SENTENCES |
| 3 | revise | PASS (11/11) | - |

## Attempt 1 (generate): FAIL

**What failed and why:**

- **L1_ACCURACY: No false or misleading claims** _(accurate & grounded, llm check)_
  - Requirement: Every technical claim agrees with the reference facts. No listed misconception is stated or implied as true. Simplifications are allowed only if they do not create a wrong belief (e.g. 'the model learns your documents' is a FAIL, because RAG does not change the model).
  - Evidence: The lesson does NOT state or imply: "RAG retrains or fine-tunes the model on your documents." -> "Here is the secret: RAG works by retraining the AI model on your documents. After that, the model remembers them forever, so its answers are always correct."
  - Evidence: The lesson does NOT state or imply: "After RAG, the model permanently remembers the documents." -> "After that, the model remembers them forever, so its answers are always correct."
  - Evidence: The lesson does NOT state or imply: "RAG guarantees correct answers / completely removes hallucinations." -> "After that, the model remembers them forever, so its answers are always correct."
  - Evidence: Here is the secret: RAG works by retraining the AI model on your documents. After that, the model remembers them forever, so its answers are always correct.
  - Judge reasoning: The lesson explicitly contradicts its own later accurate statements by including a paragraph under 'How does RAG work?' that promotes major misconceptions: it states that RAG retrains the AI model, makes the model remember documents forever, and guarantees correct answers. These claims violate the reference facts and the accuracy requirements.
  - Fix requested: Remove the paragraph under 'How does RAG work?' that begins with 'Here is the secret: RAG works by retraining the AI model on your documents. After that, the model remembers them forever, so its answers are always correct.' Ensure all mentions align with the fact that RAG does not retrain the model or guarantee complete correctness.

- **L2_COVERAGE: All must-cover points taught** _(covers the key points, llm check)_
  - Requirement: Every must-cover point in the reference is actually taught (explained, not just named).
  - Evidence: Additional check: Contradictory false teaching inserted directly into the lesson text. -> "Here is the secret: RAG works by retraining the AI model on your documents. After that, the model remembers them forever, so its answers are always correct."
  - Evidence: Here is the secret: RAG works by retraining the AI model on your documents. After that, the model remembers them forever, so its answers are always correct.
  - Judge reasoning: I checked all nine must-cover points in the reference and found that they are all present and clearly explained within the text. However, the lesson explicitly includes a severe factual contradiction under the 'How does RAG work?' section, stating that RAG works by retraining the AI model on documents and that answers are always correct, which directly contradicts standard RAG principles and other parts of the lesson.
  - Fix requested: Remove the paragraph claiming that RAG retrains the AI model and guarantees always-correct answers, as it contradicts the core definition of RAG taught elsewhere in the lesson.

- **L3_JARGON: Every technical term explained** _(clear, no unexplained jargon, llm check)_
  - Requirement: Every technical or English-uncommon term is explained in simple words at or before its first use in the body (a glossary at the end alone does not count). Acronyms are expanded on first use.
  - Evidence: 'knowledge cutoff' is explained in simple words at or before its FIRST use in the body -> "First, it only knows what was in its training data up to a cutoff date."
  - Evidence: 'training data' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "First, it only knows what was in its training data up to a cutoff date.". Mark met=true ONLY if you can quote an earlier explanation. -> "First, it only knows what was in its training data up to a cutoff date."
  - Evidence: 'trained' is explained in simple words at or before its FIRST use in the body -> "An LLM is an AI model trained on a very large amount of text to predict and generate language."
  - Evidence: 'weights' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "RAG does not change the model's weights.". Mark met=true INVLY if you can quote an earlier explanation. -> "RAG does not change the model's weights."
  - Evidence: First, it only knows what was in its training data up to a cutoff date.
  - Evidence: RAG does not change the model's weights.
  - Judge reasoning: I checked every technical term against the rule that it must be explained in simple words at or before its first use. While many terms like 'LLM', 'hallucination', 'chunk', and 'embedding' are well-explained, terms like 'training data', 'weights', and 'knowledge cutoff' (referred to as cutoff date) are used without a prior simple explanation.
  - Fix requested: Add a simple explanation for 'training data' (e.g., the past books and text the AI read to learn), 'cutoff date / knowledge cutoff' (the date after which the AI has no new information), and 'weights' (the internal numbers the AI adjusts to learn) before their first use.

- **L6_FLOW: Builds step by step** _(coherent teaching flow, llm check)_
  - Requirement: Ideas are introduced before they are used; sections go from what -> why -> how -> example -> limits -> recap; each section links to the previous one; nothing is repeated without purpose.
  - Evidence: 2. Every idea or term is introduced before it is used (quote any used before being introduced). -> "Here is the secret: RAG works by retraining the AI model on your documents. After that, the model remembers them forever, so its answers are always correct. RAG works in steps behind the screen."
  - Evidence: Here is the secret: RAG works by retraining the AI model on your documents. After that, the model remembers them forever, so its answers are always correct.
  - Judge reasoning: I checked the structural flow, order of sections, term introduction, section transitions, and repetition. Sections follow the required order and connect logically. However, under the 'How does RAG work?' section, the text states 'RAG works by retraining the AI model on your documents', which directly contradicts the core concept of RAG and later statements in the same section ('RAG does not change the model's weights. There is no retraining.'), causing an internal contradiction and introduction of incorrect information before it is corrected.
  - Fix requested: Remove the incorrect sentence claiming RAG works by retraining the AI model at the beginning of the 'How does RAG work?' section, as it contradicts the correct explanation given a few paragraphs later ('RAG does not change the model's weights. There is no retraining.').

## Attempt 2 (revise): FAIL

**What changed in this draft (in response to the previous rejection):**
- `L1_ACCURACY`: Removed the false paragraph claiming RAG retrains the AI model and ensures always-correct answers.
- `L2_COVERAGE`: Removed the contradictory false teaching that RAG retrains models and guarantees correctness.
- `L3_JARGON`: Added simple explanations for training data, cutoff date, knowledge cutoff, and weights at their first use.
- `L6_FLOW`: Removed the incorrect introductory sentence about retraining in the RAG section so ideas flow logically without contradiction.
- Diff vs previous draft: +5 / -7 lines (`attempt_2.diff`)

**What failed and why:**

- **R2_SENTENCES: Short sentences** _(beginner-friendly language, rule check)_
  - Requirement: Average sentence length <= 15 words AND no sentence longer than 25 words.
  - Evidence: (43 words) First, it only knows what was in its training data (the past books and text the AI read to learn) up to a cutoff date (a knowledge cutoff, which is the date after which the AI has no new information in its memory).
  - Fix requested: Split every sentence longer than 25 words into two or three short sentences. One idea per sentence.

## Attempt 3 (revise): PASS

**What changed in this draft (in response to the previous rejection):**
- `R2_SENTENCES`: Split the long sentence about training data and knowledge cutoff into three short sentences.
- Diff vs previous draft: +1 / -1 lines (`attempt_3.diff`)

All checks passed.

## Final scorecard (shipped attempt)

| Check | Dimension | Result | Metrics |
|---|---|---|---|
| R1_STRUCTURE Required sections present | coherent teaching flow | PASS |  |
| R2_SENTENCES Short sentences | beginner-friendly language | PASS | avg_sentence_words=10.7, sentences=100, over_cap=0 |
| R3_READABILITY Plain-English readability | beginner-friendly language | PASS | flesch=74.5 |
| R4_LENGTH Right length for one sitting | covers the key points | PASS | word_count=1123 |
| R5_QUIZ Self-check with answers | teaches by example | PASS | quiz_questions=4, quiz_has_answers=True |
| L1_ACCURACY No false or misleading claims | accurate & grounded | PASS | items_checked=8, items_unmet=0 |
| L2_COVERAGE All must-cover points taught | covers the key points | PASS | items_checked=9, items_unmet=0 |
| L3_JARGON Every technical term explained | clear, no unexplained jargon | PASS | items_checked=21, items_unmet=0 |
| L4_EXAMPLES Concrete analogy and walk-through | teaches by example | PASS | items_checked=6, items_unmet=0 |
| L5_LEARNER_FIT Fits a non-native English beginner | beginner-friendly language | PASS | items_checked=5, items_unmet=0 |
| L6_FLOW Builds step by step | coherent teaching flow | PASS | items_checked=4, items_unmet=0 |

## What the system learned from this run

- No check has failed often enough to change the prompt yet.

Active guidelines now in memory: 0 | learned rubric checks: 0

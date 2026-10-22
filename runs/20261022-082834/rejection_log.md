# Rejection log: Introduction to RAG (Retrieval-Augmented Generation)

- **Run:** `20261022-082834`
- **Status:** ⚠️ NEEDS HUMAN REVIEW, not shipped
- **Shipped attempt:** 3 of 3 (retry budget: 2)
- **Generator:** `gemini:gemini-3.5-flash-lite` | **Evaluator:** `gemini:gemini-3.5-flash-lite` (judge votes: 1)
- **Grounding:** reference sheet `rag.json` (trust: curated)
- **Learned guidelines in the prompt at start:** 3
- **Web research:** 14 learning resources verified live; 1 fresh facts from 5 web sources
  - Fresh fact: The retriever converts the query into a vector embedding and searches a vector database to find top-k similar documents. ([source](https://pub.towardsai.net/rag-the-backbone-of-modern-ai-applications-what-why-how-and-the-latest-advancements-9620f407b2f7))

## Summary

| Attempt | How produced | Result | Failed checks |
|---|---|---|---|
| 1 | generate | FAIL (11/12) | R2_SENTENCES |
| 2 | revise | FAIL (11/12) | L3_JARGON |
| 3 | revise | FAIL (11/12) | R2_SENTENCES |

## Attempt 1 (generate): FAIL

**What failed and why:**

- **R2_SENTENCES: Short sentences** _(beginner-friendly language, rule check)_
  - Requirement: Average sentence length <= 15 words AND no sentence longer than 25 words.
  - Evidence: (30 words) It is a type of AI called a large language model (an LLM is an AI model trained on a very large amount of text to predict and generate language).
  - Evidence: (26 words) Search: When you ask a question, the system converts your question into an embedding and searches the database to find the top few most similar chunks.
  - Evidence: (28 words) The prompt sent to the AI looks like this: "Answer the user question using only this text chunk: [Chunk text: Exam fee last date is 15th July].
  - Fix requested: Split every sentence longer than 25 words into two or three short sentences. One idea per sentence.

## Attempt 2 (revise): FAIL

**What changed in this draft (in response to the previous rejection):**
- `R2_SENTENCES`: Split the long sentence defining LLMs in the introduction into two shorter sentences.
- `R2_SENTENCES`: Split the long sentence about search embeddings into two separate sentences under step five.
- `R2_SENTENCES`: Split the long sentence containing the prompt example into shorter, simpler sentences in the worked example.
- Diff vs previous draft: +17 / -17 lines (`attempt_2.diff`)

**What failed and why:**

- **L3_JARGON: Every technical term explained** _(clear, no unexplained jargon, llm check)_
  - Requirement: Every technical or English-uncommon term is explained in simple words at or before its first use in the body (a glossary at the end alone does not count). Acronyms are expanded on first use.
  - Evidence: 'AI model' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "An LLM is an AI model trained on a very large amount of text to predict and generate language.". Mark met=true ONLY if you can quote an earlier explanation. -> (not found)
  - Evidence: 'prompt' is explained in simple words at or before its FIRST use in the body -> (not found)
  - Evidence: 'retrieve' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "Add to prompt: The system places those retrieved chunks into a prompt (the message you type to the AI) along with your original question.". Mark met=true ONLY if you can quote an earlier explanation. -> (not found)
  - Evidence: 'generation' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "An LLM is an AI model trained on a very large amount of text to predict and generate language.". Mark met=true ONLY if you can quote an earlier explanation. -> (not found)
  - Evidence: 'trained' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "An LLM is an AI model trained on a very large amount of text to predict and generate language.". Mark met=true ONLY if you can quote an earlier explanation. -> (not found)
  - Evidence: 'database' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "Store in an index: Save these embeddings in a searchable list or vector index (a database that stores number lists for fast searching).". Mark met=true ONLY if you can quote an earlier explanation. -> (not found)
  - Judge reasoning: I checked every required technical term to see if it was explained in simple words at or before its first appearance in the lesson body. Several terms like 'AI model', 'prompt', 'retrieved' / 'retrieve', 'generation', 'trained', and 'database' are used before any definition or explanation is provided in the text. Therefore, the lesson fails the strict jargon explanation requirement.
  - Fix requested: Ensure that every technical term, including 'AI model', 'prompt', 'retrieved', 'generation', 'trained', and 'database', is clearly defined in simple words right before or immediately when it first appears in the lesson body.

## Attempt 3 (revise): FAIL

**What changed in this draft (in response to the previous rejection):**
- `L3_JARGON`: Added immediate definitions for AI model, trained, predict, and generate right where they first appear.
- `L3_JARGON`: Added a simple definition for generation right at its first use in the body.
- `L3_JARGON`: Added a simple definition for retrieval right at its first use in the body.
- `L3_JARGON`: Added a simple definition for database right at its first use in the body.
- `L3_JARGON`: Added a simple definition for retrieved and prompt right at their first use in step 6.
- Diff vs previous draft: +5 / -5 lines (`attempt_3.diff`)

**What failed and why:**

- **R2_SENTENCES: Short sentences** _(beginner-friendly language, rule check)_
  - Requirement: Average sentence length <= 15 words AND no sentence longer than 25 words.
  - Evidence: (41 words) An LLM is an AI model (a computer program designed to think or act like a human) trained (taught using many examples) on a very large amount of text to predict (guess the next word) and generate (produce new text) language.
  - Evidence: (32 words) Store in an index: Save these embeddings in a searchable list or vector index (a database [an organized collection of data stored on a computer] that stores number lists for fast searching).
  - Evidence: (32 words) Add to prompt: The system places those retrieved (found and brought back from storage) chunks into a prompt (the message or question you type to the AI) along with your original question.
  - Fix requested: Split every sentence longer than 25 words into two or three short sentences. One idea per sentence.

_Retry budget exhausted, so the loop stopped here._

## Final scorecard (shipped attempt)

| Check | Dimension | Result | Metrics |
|---|---|---|---|
| R1_STRUCTURE Required sections present | coherent teaching flow | PASS |  |
| R2_SENTENCES Short sentences | beginner-friendly language | FAIL | avg_sentence_words=11.9, sentences=86, over_cap=3 |
| R3_READABILITY Plain-English readability | beginner-friendly language | PASS | flesch=75.0 |
| R4_LENGTH Right length for one sitting | covers the key points | PASS | word_count=1076 |
| R5_QUIZ Self-check with answers | teaches by example | PASS | quiz_questions=4, quiz_has_answers=True |
| R6_RESOURCES Verified links to learn more | teaches by example | PASS | links=4, verified_used=4, videos=2 |
| L1_ACCURACY No false or misleading claims | accurate & grounded | PASS | items_checked=76, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L2_COVERAGE All must-cover points taught | covers the key points | PASS | items_checked=9, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L3_JARGON Every technical term explained | clear, no unexplained jargon | PASS | items_checked=20, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L4_EXAMPLES Concrete analogy and walk-through | teaches by example | PASS | items_checked=6, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L5_LEARNER_FIT Fits a non-native English beginner | beginner-friendly language | PASS | items_checked=5, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L6_FLOW Builds step by step | coherent teaching flow | PASS | items_checked=4, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |

## What the system learned from this run

- L3_JARGON: reinforced existing guideline G3
- R2_SENTENCES: reinforced existing guideline G1

Active guidelines now in memory: 3 | learned rubric checks: 0

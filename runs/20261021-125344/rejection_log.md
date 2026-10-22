# Rejection log: Introduction to RAG (Retrieval-Augmented Generation)

- **Run:** `20261021-125344`
- **Status:** ✅ PASSED, shipped
- **Shipped attempt:** 3 of 3 (retry budget: 2)
- **Generator:** `gemini-3.5-flash-lite` | **Evaluator:** `gemini-3.5-flash-lite`
- **Grounding:** reference sheet `rag.json` (trust: curated)
- **Learned guidelines in the prompt at start:** 2

## Summary

| Attempt | How produced | Result | Failed checks |
|---|---|---|---|
| 1 | generate | FAIL (9/11) | L3_JARGON, L4_EXAMPLES |
| 2 | revise | FAIL (10/11) | R2_SENTENCES |
| 3 | revise | PASS (11/11) | - |

## Attempt 1 (generate): FAIL

**What failed and why:**

- **L3_JARGON: Every technical term explained** _(clear, no unexplained jargon, llm check)_
  - Requirement: Every technical or English-uncommon term is explained in simple words at or before its first use in the body (a glossary at the end alone does not count). Acronyms are expanded on first use.
  - Evidence: 'AI model' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "An LLM is an AI model trained on huge amounts of text.". Mark met=true ONLY if you can quote an earlier explanation. -> "An LLM is an AI model trained on huge amounts of text."
  - Evidence: 'LLM' is explained in simple words at or before its FIRST use in the body -> "An LLM is an AI model trained on huge amounts of text."
  - Evidence: 'prompt' is explained in simple words at or before its FIRST use in the body -> "5. **Augmentation**: The system takes those relevant chunks and adds them to a **prompt** (the message you type to the AI)."
  - Evidence: 'retrieve' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "Relevant text is retrieved and added to the prompt.". Mark met=true ONLY if you can quote an earlier explanation. -> "Relevant text is retrieved and added to the prompt."
  - Evidence: 'generation' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "It predicts and generates natural language like a human.". Mark met=true ONLY if you can quote an earlier explanation. -> "It predicts and generates natural language like a human."
  - Evidence: 'index' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "Indexing documents: You collect your documents and split them into small pieces.". Mark met=true ONLY if you can quote an earlier explanation. -> "Indexing documents: You collect your documents and split them into small pieces."
  - Judge reasoning: Several technical terms such as AI model, LLM, index, database, training data, and hallucinate are used without a simple definition provided at or directly before their first appearance in the body text.
  - Fix requested: Ensure terms like LLM, AI model, index/indexing, training data, and database are defined in simple words before or right when they are first used in the text.

- **L4_EXAMPLES: Concrete analogy and walk-through** _(teaches by example, llm check)_
  - Requirement: The lesson has (a) at least one everyday analogy a young Indian learner would recognise, correctly mapped to RAG, AND (b) one concrete worked example that follows a single question through every step: preparing documents, retrieving, adding to the prompt, generating.
  - Evidence: There is an everyday analogy a young Indian learner would recognise. -> (not found)
  - Evidence: The analogy is mapped to RAG correctly (each part of the analogy matches a real part of RAG). -> (not found)
  - Evidence: Everyday analogy is missing entirely from the lesson.
  - Judge reasoning: The lesson includes a concrete worked example tracking a college rulebook through preparation, retrieval, augmentation, and generation. However, it completely lacks an everyday analogy (like an open-book exam or a librarian looking up a book) mapped to RAG before or during the example.
  - Fix requested: Add an everyday analogy before the worked example, such as comparing RAG to a student taking an open-book exam using a textbook, and explicitly map the parts (the textbook is the document folder, looking up the index is retrieval, etc.).

## Attempt 2 (revise): FAIL

**What changed in this draft (in response to the previous rejection):**
- `L3_JARGON`: Added simple explanations for technical terms like AI model, trained, training data, hallucinate, retrieval, generation, indexing, index, embedding, database, vector database, and prompt right at their first use in the body.
- `L4_EXAMPLES`: Added an everyday open-book exam analogy mapped to RAG before the worked example.
- Diff vs previous draft: +23 / -17 lines (`attempt_2.diff`)

**What failed and why:**

- **R2_SENTENCES: Short sentences** _(beginner-friendly language, rule check)_
  - Requirement: Average sentence length <= 15 words AND no sentence longer than 25 words.
  - Evidence: (26 words) Indexing documents: Indexing (organizing and preparing documents so they can be searched quickly) means you collect your documents and split them into small pieces called chunks.
  - Evidence: (31 words) Storing data: You store these embeddings in a searchable place called a vector database (a database [an organized collection of data stored in a computer] designed to search through meaning-based numbers).
  - Evidence: (37 words) In this analogy, the LLM is the student, the textbook is the folder of documents, looking up the page is retrieval, adding notes to the answer sheet is augmentation, and writing the final exam answer is generation.
  - Fix requested: Split every sentence longer than 25 words into two or three short sentences. One idea per sentence.

## Attempt 3 (revise): PASS

**What changed in this draft (in response to the previous rejection):**
- `R2_SENTENCES`: Split the long sentence about indexing documents into two shorter sentences.
- `R2_SENTENCES`: Split the long sentence about vector databases into two shorter sentences.
- `R2_SENTENCES`: Split the long sentence summarizing the analogy into five short, separate sentences.
- Diff vs previous draft: +10 / -5 lines (`attempt_3.diff`)

All checks passed.

## Final scorecard (shipped attempt)

| Check | Dimension | Result | Metrics |
|---|---|---|---|
| R1_STRUCTURE Required sections present | coherent teaching flow | PASS |  |
| R2_SENTENCES Short sentences | beginner-friendly language | PASS | avg_sentence_words=11.5, sentences=94, over_cap=0 |
| R3_READABILITY Plain-English readability | beginner-friendly language | PASS | flesch=68.4 |
| R4_LENGTH Right length for one sitting | covers the key points | PASS | word_count=1138 |
| R5_QUIZ Self-check with answers | teaches by example | PASS | quiz_questions=4, quiz_has_answers=True |
| L1_ACCURACY No false or misleading claims | accurate & grounded | PASS | items_checked=8, items_unmet=0 |
| L2_COVERAGE All must-cover points taught | covers the key points | PASS | items_checked=9, items_unmet=0 |
| L3_JARGON Every technical term explained | clear, no unexplained jargon | PASS | items_checked=24, items_unmet=0 |
| L4_EXAMPLES Concrete analogy and walk-through | teaches by example | PASS | items_checked=6, items_unmet=0 |
| L5_LEARNER_FIT Fits a non-native English beginner | beginner-friendly language | PASS | items_checked=5, items_unmet=0 |
| L6_FLOW Builds step by step | coherent teaching flow | PASS | items_checked=4, items_unmet=0 |

## What the system learned from this run

- L3_JARGON: new guideline G3 -> Define every technical term in simple words immediately before or upon its first use in the body.
- L4_EXAMPLES: reinforced existing guideline G2
- R2_SENTENCES: reinforced existing guideline G1

Active guidelines now in memory: 3 | learned rubric checks: 0

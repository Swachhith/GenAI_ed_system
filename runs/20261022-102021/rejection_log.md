# Rejection log: Introduction to RAG

- **Run:** `20261022-102021`
- **Status:** ⚠️ NEEDS HUMAN REVIEW, not shipped
- **Shipped attempt:** 3 of 3 (retry budget: 2)
- **Generator:** `gemini:gemini-3.5-flash-lite` | **Evaluator:** `gemini:gemini-3.5-flash-lite` (judge votes: 1)
- **Grounding:** reference sheet `rag.json` (trust: curated)
- **Learned guidelines in the prompt at start:** 6
- **Web research:** 9 learning resources verified live; 0 fresh facts from 5 web sources

## Summary

| Attempt | How produced | Result | Failed checks |
|---|---|---|---|
| 1 | generate | FAIL (10/12) | R2_SENTENCES, L4_EXAMPLES |
| 2 | revise | FAIL (10/12) | R2_SENTENCES, L3_JARGON |
| 3 | regenerate | FAIL (10/12) | R2_SENTENCES, L4_EXAMPLES |

## Attempt 1 (generate): FAIL

**What failed and why:**

- **R2_SENTENCES: Short sentences** _(beginner-friendly language, rule check)_
  - Requirement: Average sentence length <= 15 words AND no sentence longer than 25 words.
  - Evidence: (27 words) Instead, when a question arrives, you look up the correct page in your rulebook, place that page on your desk, and write your answer using those facts.
  - Evidence: (26 words) The LLM generates the final answer: "The fine for returning a library book late is ten rupees per day, according to page 12 of your rulebook."
  - Fix requested: Split every sentence longer than 25 words into two or three short sentences. One idea per sentence.

- **L4_EXAMPLES: Concrete analogy and walk-through** _(teaches by example, llm check)_
  - Requirement: The lesson has (a) at least one everyday analogy a young Indian learner would recognise, correctly mapped to the topic, AND (b) one concrete worked example that follows a single case through every step the lesson lists under 'How does it work?', in order, to its result.
  - Evidence: The worked example goes through EVERY step listed in the 'How does it work?' section, in the same order, applied to that one case (name any step it skips). -> "1. The system converts the student's question into an embedding. 2. The system searches the vector index for chunks with the most similar embeddings. It finds chunk number 14, which discusses library rules and fines. 3. The system takes chunk 14 and places it into the prompt together with the student's question. An instruction tells the model to use only the provided text. 4. The LLM reads chunk 14, which states that the fine is ten rupees per day. 5. The LLM generates the final answer..."
  - Judge reasoning: The lesson includes a clear open-book exam analogy and a specific query about a library book fine. However, the 'How does it work?' section lists 8 steps (including Document collection, Chunking, Embedding creation, Storage, Query embedding, Similarity search, Prompt augmentation, Generation), while the worked example only walks through 5 steps of the query phase and skips the preparation/storage steps for that specific case.
  - Fix requested: Update the 'Let's follow one example' section so that it explicitly mentions how the chosen example document (e.g., the library rule page) goes through document collection, chunking, embedding creation, and storage before the student asks the question, matching all 8 steps from the 'How does it work?' section in order.

## Attempt 2 (revise): FAIL

**What changed in this draft (in response to the previous rejection):**
- `R2_SENTENCES`: Split long compound sentences about the open-book exam and the final LLM answer into multiple short sentences under 25 words.
- `L4_EXAMPLES`: Expanded the worked example section to explicitly list all eight steps from document collection to generation in order.
- Diff vs previous draft: +10 / -13 lines (`attempt_2.diff`)

**What failed and why:**

- **R2_SENTENCES: Short sentences** _(beginner-friendly language, rule check)_
  - Requirement: Average sentence length <= 15 words AND no sentence longer than 25 words.
  - Evidence: (31 words) The LLM generates the final answer: "The fine for returning a library book late is ten rupees per day." It adds that this is according to page 12 of your rulebook.
  - Fix requested: Split every sentence longer than 25 words into two or three short sentences. One idea per sentence.

- **L3_JARGON: Every technical term explained** _(clear, no unexplained jargon, llm check)_
  - Requirement: Every technical or English-uncommon term is explained in simple words at or before its first use in the body (a glossary at the end alone does not count). Acronyms are expanded on first use.
  - Evidence: 'prompt' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "Prompt augmentation: The system places the retrieved text pieces into the prompt along with the user's question.". Mark met=true ONLY if you can quote an earlier explanation. -> "(no proof: quote not found in the lesson) Seventh, prompt augmentation means placing the retrieved text pieces into the instructions along with the user's question."
  - Judge reasoning: I checked every technical and uncommon term in the lesson against the criteria. All terms, including acronyms and conceptual jargon, are properly introduced, expanded, and explained in simple terms either right before or immediately at their first use.
  - Fix requested: Fix each unmet item listed in the evidence.

## Attempt 3 (regenerate): FAIL

**What changed in this draft (in response to the previous rejection):**
- `R2_SENTENCES`: Targeted edits failed twice, so the lesson was rewritten from scratch with this failure given as an explicit constraint.

**What failed and why:**

- **R2_SENTENCES: Short sentences** _(beginner-friendly language, rule check)_
  - Requirement: Average sentence length <= 15 words AND no sentence longer than 25 words.
  - Evidence: (36 words) Finally, the LLM reads chunk twelve and generates the final answer: "The fine for returning a library book late is ten rupees per day." The answer is accurate because the model read the real rulebook page.
  - Fix requested: Split every sentence longer than 25 words into two or three short sentences. One idea per sentence.

- **L4_EXAMPLES: Concrete analogy and walk-through** _(teaches by example, llm check)_
  - Requirement: The lesson has (a) at least one everyday analogy a young Indian learner would recognise, correctly mapped to the topic, AND (b) one concrete worked example that follows a single case through every step the lesson lists under 'How does it work?', in order, to its result.
  - Evidence: The worked example goes through EVERY step listed in the 'How does it work?' section, in the same order, applied to that one case (name any step it skips). -> "First, the college collects the rulebook PDF. The system splits the PDF into small chunks. It turns every chunk into a list of numbers representing meaning and stores them. This setup happens before any student asks a question. Next, a student types a question... It finds chunk number twelve... Then, the system copies chunk twelve into a prompt... Finally, the LLM reads chunk twelve and generates the final answer"
  - Judge reasoning: I checked the lesson for an everyday analogy and a complete worked example. The lesson includes a good analogy of a kirana shop owner and a college helpdesk bot example. However, item 4 fails because the 'How does it work?' section lists 7 distinct steps (Indexing, Embedding, Storage, Querying, Retrieval, Augmentation, Generation), whereas the worked example skips explicit mention of Step 3 (Storage) and Step 4 (Querying turning the question into an embedding) in sequence, blurring the step-by-step alignment.
  - Fix requested: In the 'Let's follow one example' section, explicitly label or write out sentences corresponding to storage and querying as numbers/embeddings so that every single one of the 7 steps from 'How does it work?' is tracked sequentially for the student's question.

_Retry budget exhausted, so the loop stopped here._

## Final scorecard (shipped attempt)

| Check | Dimension | Result | Metrics |
|---|---|---|---|
| R1_STRUCTURE Required sections present | coherent teaching flow | PASS |  |
| R2_SENTENCES Short sentences | beginner-friendly language | FAIL | avg_sentence_words=11.1, sentences=85, over_cap=1 |
| R3_READABILITY Plain-English readability | beginner-friendly language | PASS | flesch=68.7 |
| R4_LENGTH Right length for one sitting | covers the key points | PASS | word_count=991 |
| R5_QUIZ Self-check with answers | teaches by example | PASS | quiz_questions=4, quiz_has_answers=True |
| R6_RESOURCES Verified links to learn more | teaches by example | PASS | links=4, verified_used=4, videos=2 |
| L1_ACCURACY No false or misleading claims | accurate & grounded | PASS | items_checked=80, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L2_COVERAGE All must-cover points taught | covers the key points | PASS | items_checked=9, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L3_JARGON Every technical term explained | clear, no unexplained jargon | PASS | items_checked=25, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L4_EXAMPLES Concrete analogy and walk-through | teaches by example | FAIL | items_checked=5, items_unmet=1, extra_problems=0, ungrounded_dropped=1, votes=1 |
| L5_LEARNER_FIT Fits a non-native English beginner | beginner-friendly language | PASS | items_checked=5, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L6_FLOW Builds step by step | coherent teaching flow | PASS | items_checked=5, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |

## What the system learned from this run

- L3_JARGON: reinforced existing guideline G3
- L4_EXAMPLES: reinforced existing guideline G2
- R2_SENTENCES: reinforced existing guideline G1

Active guidelines now in memory: 6 | learned rubric checks: 0

# Rejection log: Introduction to RAG (Retrieval-Augmented Generation)

- **Run:** `20261022-083015`
- **Status:** ✅ PASSED, shipped
- **Shipped attempt:** 2 of 2 (retry budget: 2)
- **Generator:** `gemini:gemini-3.5-flash-lite` | **Evaluator:** `gemini:gemini-3.5-flash-lite` (judge votes: 1)
- **Grounding:** reference sheet `rag.json` (trust: curated)
- **Learned guidelines in the prompt at start:** 3
- **Web research:** 14 learning resources verified live; 1 fresh facts from 5 web sources
  - Fresh fact: The retriever converts the query into a vector embedding and searches a vector database to find top-k similar documents. ([source](https://pub.towardsai.net/rag-the-backbone-of-modern-ai-applications-what-why-how-and-the-latest-advancements-9620f407b2f7))

## Summary

| Attempt | How produced | Result | Failed checks |
|---|---|---|---|
| 1 | generate | FAIL (10/12) | R2_SENTENCES, L1_ACCURACY |
| 2 | revise | PASS (12/12) | - |

## Attempt 1 (generate): FAIL

**What failed and why:**

- **R2_SENTENCES: Short sentences** _(beginner-friendly language, rule check)_
  - Requirement: Average sentence length <= 15 words AND no sentence longer than 25 words.
  - Evidence: (27 words) Finally, the LLM reads the rule chunk and writes: "The fine for returning a library book late is five rupees per day." This is the generation step.
  - Fix requested: Split every sentence longer than 25 words into two or three short sentences. One idea per sentence.

- **L1_ACCURACY: No false or misleading claims** _(accurate & grounded, llm check)_
  - Requirement: Every technical claim agrees with the reference facts. No listed misconception is stated or implied as true. Simplifications are allowed only if they do not create a wrong belief (e.g. 'the model learns your documents' is a FAIL, because RAG does not change the model).
  - Evidence: ABSOLUTE CLAIM: "Second, it stops the model from making up wild lies." The word 'stops' makes this an all-or-nothing claim. met=true ONLY if it is literally true with no exceptions according to the reference facts (check the facts about limits). -> "Second, it stops the model from making up wild lies."
  - Evidence: Other problem -> "Second, it stops the model from making up wild lies."
  - Judge reasoning: I checked every technical claim and absolute term against the reference facts. Almost all statements are accurate and well-aligned with the reference sheet, but claim 2 states that RAG 'stops' the model from making up wild lies, which violates the absolute accuracy rule since RAG reduces hallucinations rather than entirely stopping them (as correctly noted later in the text). I checked every required claim against the reference facts and misconceptions list. All statements regarding how LLMs work, what RAG is, how embeddings and chunking function, and the steps of retrieval, augmentation, and generation are accurate and align fully with the facts. I checked the lesson for accuracy against the reference facts and misconceptions. The specific definition of embedding is stated accurately, and all other technical explanations regarding LLMs, RAG steps, context window, and limitations align correctly without introducing false claims.
  - Fix requested: Change the sentence under 'Why does RAG matter?' from 'Second, it stops the model from making up wild lies.' to 'Second, it greatly reduces made-up answers from the model.'

## Attempt 2 (revise): PASS

**What changed in this draft (in response to the previous rejection):**
- `R2_SENTENCES`: Split the long sentence in the example section into two short sentences: 'Finally, the LLM reads the rule chunk. Then the LLM writes the answer.'
- `L1_ACCURACY`: Changed 'Second, it stops the model from making up wild lies.' to 'Second, it greatly reduces made-up answers from the model.'
- Diff vs previous draft: +2 / -2 lines (`attempt_2.diff`)

All checks passed.

## Final scorecard (shipped attempt)

| Check | Dimension | Result | Metrics |
|---|---|---|---|
| R1_STRUCTURE Required sections present | coherent teaching flow | PASS |  |
| R2_SENTENCES Short sentences | beginner-friendly language | PASS | avg_sentence_words=9.8, sentences=95, over_cap=0 |
| R3_READABILITY Plain-English readability | beginner-friendly language | PASS | flesch=75.5 |
| R4_LENGTH Right length for one sitting | covers the key points | PASS | word_count=980 |
| R5_QUIZ Self-check with answers | teaches by example | PASS | quiz_questions=4, quiz_has_answers=True |
| R6_RESOURCES Verified links to learn more | teaches by example | PASS | links=4, verified_used=4, videos=2 |
| L1_ACCURACY No false or misleading claims | accurate & grounded | PASS | items_checked=84, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L2_COVERAGE All must-cover points taught | covers the key points | PASS | items_checked=9, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L3_JARGON Every technical term explained | clear, no unexplained jargon | PASS | items_checked=21, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L4_EXAMPLES Concrete analogy and walk-through | teaches by example | PASS | items_checked=6, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L5_LEARNER_FIT Fits a non-native English beginner | beginner-friendly language | PASS | items_checked=5, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L6_FLOW Builds step by step | coherent teaching flow | PASS | items_checked=4, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |

## What the system learned from this run

- L1_ACCURACY: new guideline G4 -> Ensure all technical explanations remain factually accurate without implying models are retrained or hallucinations are completely eliminated.
- R2_SENTENCES: reinforced existing guideline G1

Active guidelines now in memory: 4 | learned rubric checks: 0

# Rejection log: Introduction to Embeddings

- **Run:** `20261022-085459`
- **Status:** ⚠️ NEEDS HUMAN REVIEW, not shipped
- **Shipped attempt:** 3 of 3 (retry budget: 2)
- **Generator:** `gemini:gemini-3.5-flash-lite` | **Evaluator:** `gemini:gemini-3.5-flash-lite` (judge votes: 1)
- **Grounding:** reference sheet `introduction-to-embeddings.json` (trust: generated+web)
- **Learned guidelines in the prompt at start:** 4
- **Web research:** 8 learning resources verified live; 0 fresh facts from 5 web sources

## Summary

| Attempt | How produced | Result | Failed checks |
|---|---|---|---|
| 1 | generate | FAIL (10/12) | R2_SENTENCES, L3_JARGON |
| 2 | revise | FAIL (11/12) | L5_LEARNER_FIT |
| 3 | revise | FAIL (11/12) | L4_EXAMPLES |

## Attempt 1 (generate): FAIL

**What failed and why:**

- **R2_SENTENCES: Short sentences** _(beginner-friendly language, rule check)_
  - Requirement: Average sentence length <= 15 words AND no sentence longer than 25 words.
  - Evidence: (28 words) This is a realistic use case of building a semantic search engine or recommendation system that finds documents or products with similar meanings rather than exact keyword matches.
  - Fix requested: Split every sentence longer than 25 words into two or three short sentences. One idea per sentence.

- **L3_JARGON: Every technical term explained** _(clear, no unexplained jargon, llm check)_
  - Requirement: Every technical or English-uncommon term is explained in simple words at or before its first use in the body (a glossary at the end alone does not count). Acronyms are expanded on first use.
  - Evidence: 'high-dimensional space' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "The model outputs a dense vector, which is a list of numbers representing coordinates in a high-dimensional space.". Mark met=true ONLY if you can quote an earlier explanation. -> (not found)
  - Evidence: 'neural network' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "Raw data such as words or documents are fed into a trained neural network model.". Mark met=true ONLY if you can quote an earlier explanation. -> (not found)
  - Evidence: 'lossy compression' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "One major issue is lossy compression where some fine details or exact nuances of the original text can be lost during vector creation.". Mark met=true ONLY if you can quote an earlier explanation. -> (not found)
  - Evidence: Other problem -> "high-dimensional space"
  - Evidence: Other problem -> "neural network"
  - Evidence: Other problem -> "lossy compression"
  - Judge reasoning: The lesson introduces several technical terms like 'high-dimensional space', 'neural network', and 'lossy compression' in the body text without explaining them at or before their first use. While some terms are explained correctly before use, these specific ones are used first and explained later or not at all in simple terms prior to their appearance.
  - Fix requested: Move the definitions or provide simple explanations for 'high-dimensional space', 'neural network', and 'lossy compression' right before or at their very first appearance in the text.

## Attempt 2 (revise): FAIL

**What changed in this draft (in response to the previous rejection):**
- `R2_SENTENCES`: Split the long sentence in the example section into two short sentences.
- `L3_JARGON`: Added simple explanations for high-dimensional space, neural network, and lossy compression right before their first use.
- Diff vs previous draft: +7 / -4 lines (`attempt_2.diff`)

**What failed and why:**

- **L5_LEARNER_FIT: Fits a non-native English beginner** _(beginner-friendly language, llm check)_
  - Requirement: Uses common, everyday English words; no idioms, slang, sarcasm or culturally obscure references; assumes no coding, maths beyond class 12, or prior AI knowledge; tone is encouraging and direct.
  - Evidence: Grammar is correct and simple, e.g. no verb used where a noun is needed, no wrong word form (quote any grammar mistakes). -> "What is Embeddings?"
  - Evidence: Other problem -> "What is Embeddings?"
  - Judge reasoning: The lesson is generally clear, beginner-friendly, and well-tailored for non-native English speakers. However, there is a minor grammatical error in a subheading where a plural noun is mismatched with a singular verb ('What is Embeddings?'). Therefore, item 4 fails based on that exact quote.
  - Fix requested: Change the subheading 'What is Embeddings?' to 'What are embeddings?' or 'What is an embedding?' to fix the grammar error.

## Attempt 3 (revise): FAIL

**What changed in this draft (in response to the previous rejection):**
- `L5_LEARNER_FIT`: Changed the subheading 'What is Embeddings?' to 'What are embeddings?' to fix the grammar error.
- Diff vs previous draft: +1 / -1 lines (`attempt_3.diff`)

**What failed and why:**

- **L4_EXAMPLES: Concrete analogy and walk-through** _(teaches by example, llm check)_
  - Requirement: The lesson has (a) at least one everyday analogy a young Indian learner would recognise, correctly mapped to the topic, AND (b) one concrete worked example that follows a single case through every step the lesson lists under 'How does it work?', in order, to its result.
  - Evidence: The worked example goes through EVERY step listed in the 'How does it work?' section, in the same order, applied to that one case (name any step it skips). -> "First, you collect all your book descriptions and break them into smaller paragraphs... Second, you feed these paragraphs into a neural network model... Third, the model turns every paragraph into an embedding..."
  - Evidence: Other problem -> "Worked example step 2: 'Second, you feed these paragraphs into a neural network model. The model reads the text and checks how words appear next to each other.'"
  - Judge reasoning: I checked the lesson for a recognised Indian everyday analogy, its correct mapping, a single worked case, and whether that case goes through every step listed in the 'How does it work?' section in order. Items 1, 2, 3, and 5 are fully met. However, item 4 fails because the 'How does it work?' section lists 3 specific steps (1. Raw data fed into neural network, 2. Model analyzes contexts across vast amounts of training data, 3. Model outputs a dense vector), but the worked example introduces completely different custom steps ('First, you collect all your book descriptions...', 'Second, you feed...', 'Third, the model turns...') instead of explicitly applying the three listed conceptual steps to the single concrete book case in order.
  - Fix requested: Revise the 'Let's follow one example' section so that it explicitly maps the concrete case (e.g., the Delhi street food book) through the exact three steps listed under 'How does it work?' in the exact order given, using those exact phases.

_Retry budget exhausted, so the loop stopped here._

## Final scorecard (shipped attempt)

| Check | Dimension | Result | Metrics |
|---|---|---|---|
| R1_STRUCTURE Required sections present | coherent teaching flow | PASS |  |
| R2_SENTENCES Short sentences | beginner-friendly language | PASS | avg_sentence_words=12.1, sentences=80, over_cap=0 |
| R3_READABILITY Plain-English readability | beginner-friendly language | PASS | flesch=61.3 |
| R4_LENGTH Right length for one sitting | covers the key points | PASS | word_count=1015 |
| R5_QUIZ Self-check with answers | teaches by example | PASS | quiz_questions=4, quiz_has_answers=True |
| R6_RESOURCES Verified links to learn more | teaches by example | PASS | links=3, verified_used=3, videos=3 |
| L1_ACCURACY No false or misleading claims | accurate & grounded | PASS | items_checked=80, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L2_COVERAGE All must-cover points taught | covers the key points | PASS | items_checked=8, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L3_JARGON Every technical term explained | clear, no unexplained jargon | PASS | items_checked=6, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L4_EXAMPLES Concrete analogy and walk-through | teaches by example | FAIL | items_checked=5, items_unmet=1, extra_problems=1, ungrounded_dropped=1, votes=1 |
| L5_LEARNER_FIT Fits a non-native English beginner | beginner-friendly language | PASS | items_checked=5, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L6_FLOW Builds step by step | coherent teaching flow | PASS | items_checked=4, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |

## What the system learned from this run

- L3_JARGON: reinforced existing guideline G3
- L4_EXAMPLES: reinforced existing guideline G2
- R2_SENTENCES: reinforced existing guideline G1

Active guidelines now in memory: 4 | learned rubric checks: 0

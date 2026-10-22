# Rejection log: Introduction to RAG

- **Run:** `20261022-092343`
- **Status:** ⚠️ NEEDS HUMAN REVIEW, not shipped
- **Shipped attempt:** 3 of 3 (retry budget: 2)
- **Generator:** `gemini:gemini-3.1-flash-lite` | **Evaluator:** `gemini:gemini-3.1-flash-lite` (judge votes: 1)
- **Grounding:** reference sheet `rag.json` (trust: curated)
- **Learned guidelines in the prompt at start:** 4
- **Web research:** 9 learning resources verified live; 0 fresh facts from 5 web sources

## Summary

| Attempt | How produced | Result | Failed checks |
|---|---|---|---|
| 1 | generate | FAIL (9/12) | R4_LENGTH, L3_JARGON, L6_FLOW |
| 2 | revise | FAIL (6/12) | R1_STRUCTURE, R4_LENGTH, L1_ACCURACY, L2_COVERAGE, L3_JARGON, L6_FLOW |
| 3 | regenerate | FAIL (9/12) | L1_ACCURACY, L3_JARGON, L6_FLOW |

## Attempt 1 (generate): FAIL

**What failed and why:**

- **R4_LENGTH: Right length for one sitting** _(covers the key points, rule check)_
  - Requirement: Between 850 and 1800 words (~10-15 minutes of reading for a slow reader).
  - Evidence: Word count is 801 (allowed 850-1800).
  - Fix requested: Expand to at least 850 words by adding explanation and examples.

- **L3_JARGON: Every technical term explained** _(clear, no unexplained jargon, llm check)_
  - Requirement: Every technical or English-uncommon term is explained in simple words at or before its first use in the body (a glossary at the end alone does not count). Acronyms are expanded on first use.
  - Evidence: 'LLM' is explained in simple words at or before its FIRST use in the body -> (not found)
  - Evidence: 'large language model' is explained in simple words at or before its FIRST use in the body -> (not found)
  - Evidence: 'language model' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "LLM stands for Large Language Model.". Mark met=true ONLY if you can quote an earlier explanation. -> (not found)
  - Evidence: 'prompt' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "Augment: The system takes those chunks and puts them into the prompt along with your question.". Mark met=true ONLY if you can quote an earlier explanation. -> (not found)
  - Evidence: 'embedding' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "An embedding is just a long list of numbers that represents the meaning of the text.". Mark met=true ONLY if you can quote an earlier explanation. -> (not found)
  - Evidence: 'embeddings' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "Embed: Turn these chunks into embeddings.". Mark met=true ONLY if you can quote an earlier explanation. -> (not found)
  - Judge reasoning: Several technical terms (LLM, Prompt, Embedding, Database, Trained, Retraining) are used before being defined in simple, beginner-friendly terms. While definitions appear at the end, the requirement specifies they must be defined at or before their first use in the body.
  - Fix requested: Move the glossary definitions into the main body text so that they appear before or immediately at the first use of the term. For example, define 'LLM' in the very first paragraph where it is mentioned, and explain 'prompt' before the 'Search' or 'Augment' steps.

- **L6_FLOW: Builds step by step** _(coherent teaching flow, llm check)_
  - Requirement: Ideas are introduced before they are used; sections go from what -> why -> how -> example -> limits -> recap; each section links to the previous one; nothing is repeated without purpose.
  - Evidence: Every idea or term is introduced before it is used (quote any used before being introduced). -> "The term 'prompt' is used in the 'How does it work?' section without prior definition. It is only defined later in the 'Key words' section."
  - Judge reasoning: The lesson follows the required structure well and connects sections logically. However, it uses the term 'prompt' in the 'How does it work?' section before defining it in the 'Key words' section at the end.
  - Fix requested: Define the term 'prompt' in the 'What is RAG?' or 'How does it work?' section before it is used for the first time.

## Attempt 2 (revise): FAIL

**What changed in this draft (in response to the previous rejection):**
- `R4_LENGTH`: Expanded explanations of indexing, chunking, and the AI training process to increase word count and clarity.
- `L3_JARGON`: Integrated definitions for LLM, hallucination, prompt, retraining, chunking, database, and embedding into the body text before their first use.
- `L6_FLOW`: Defined 'prompt' in the RAG section before using it in the step-by-step process.
- Diff vs previous draft: +41 / -49 lines (`attempt_2.diff`)

**What failed and why:**

- **R1_STRUCTURE: Required sections present** _(coherent teaching flow, rule check)_
  - Requirement: The lesson has an H2 section for each of: the prerequisite idea, what the topic is, why it matters, how it works, a worked example, limits, recap, a self-check quiz, and key words.
  - Evidence: Missing section: glossary
  - Fix requested: Add an H2 section for: glossary

- **R4_LENGTH: Right length for one sitting** _(covers the key points, rule check)_
  - Requirement: Between 850 and 1800 words (~10-15 minutes of reading for a slow reader).
  - Evidence: Word count is 849 (allowed 850-1800).
  - Fix requested: Expand to at least 850 words by adding explanation and examples.

- **L1_ACCURACY: No false or misleading claims** _(accurate & grounded, llm check)_
  - Requirement: Every technical claim agrees with the reference facts. No listed misconception is stated or implied as true. Simplifications are allowed only if they do not create a wrong belief (a misconception from the reference sheet, even softened, is a FAIL).
  - Evidence: ABSOLUTE CLAIM: "Retraining means teaching the AI model from scratch or changing how it thinks permanently." The word 'permanently' makes this an all-or-nothing claim. met=true ONLY if it is literally true with no exceptions according to the reference facts (check the facts about limits). -> "Retraining means teaching the AI model from scratch or changing how it thinks permanently."
  - Evidence: ABSOLUTE CLAIM: "RAG reduces hallucination, but it does not stop it completely." The word 'stop' makes this an all-or-nothing claim. met=true ONLY if it is literally true with no exceptions according to the reference facts (check the facts about limits). -> "RAG reduces hallucination, but it does not stop it completely."
  - Evidence: ABSOLUTE CLAIM: "Always check the answers because the AI can still make mistakes." The word 'Always' makes this an all-or-nothing claim. met=true ONLY if it is literally true with no exceptions according to the reference facts (check the facts about limits). -> "Always check the answers because the AI can still make mistakes."
  - Evidence: Other problem -> "Retraining means teaching the AI model from scratch or changing how it thinks permanently."
  - Evidence: Other problem -> "RAG reduces hallucination, but it does not stop it completely."
  - Evidence: Other problem -> "Always check the answers because the AI can still make mistakes."
  - Judge reasoning: The lesson contains several absolute statements (using 'permanently', 'stop', or 'always') that function as overclaims. While the technical concepts are explained well for a beginner, these absolute qualifiers fail the strict accuracy criteria for absolute claims. I reviewed the lesson against all specified technical claims and the provided reference sheet. Every claim made in the lesson is accurate and aligns with the reference definitions of RAG, LLMs, and their respective constraints.
  - Fix requested: Remove the absolute qualifiers to make the statements accurate. For example, change 'permanently' to 'significantly', change 'stop' to 'eliminate', and remove 'Always' or replace it with 'It is recommended to check' to reflect the probabilistic nature of LLMs.

- **L2_COVERAGE: All must-cover points taught** _(covers the key points, llm check)_
  - Requirement: Every must-cover point in the reference is actually taught (explained, not just named).
  - Evidence: [M2] is taught (explained, not just named): A plain definition of RAG that explains all three words: Retrieval (find relevant information), Augmented (add that information to the question/prompt), Generation (the LLM writes the answer). -> "(no proof: quote not found in the lesson) 1. Retrieval: Finding the right information from your own documents. 2. Augmented: Adding this found information to your question as a helper. 3. Generation: The AI writes a clear answer using the helper information."
  - Evidence: [M4] is taught (explained, not just named): The preparation (indexing) step: documents are collected, split into small pieces (chunks), and stored in a searchable form. At a simple level, chunks are turned into embeddings (numbers that capture meaning) so similar text can be found. -> "(no proof: quote not found in the lesson) 1. Collect: Gather all your documents, like PDFs or text files. 2. Chunking: Split these documents into small pieces called chunks. 3. Embed: Turn these chunks into embeddings. An embedding is a long list of numbers that represents the meaning of the text. 4. Store: Save these numbers in a search database."
  - Judge reasoning: I checked the lesson against all 9 requirements. The lesson covers all conceptual definitions, steps of the RAG pipeline, limits, and provides a clear, relatable example using a college rulebook, fulfilling all criteria.
  - Fix requested: Fix each unmet item listed in the evidence.

- **L3_JARGON: Every technical term explained** _(clear, no unexplained jargon, llm check)_
  - Requirement: Every technical or English-uncommon term is explained in simple words at or before its first use in the body (a glossary at the end alone does not count). Acronyms are expanded on first use.
  - Evidence: 'AI model' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "Retraining means teaching the AI model from scratch or changing how it thinks permanently.". Mark met=true ONLY if you can quote an earlier explanation. -> (not found)
  - Evidence: 'language model' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "LLM stands for Large Language Model.". Mark met=true ONLY if you can quote an earlier explanation. -> (not found)
  - Evidence: 'index' is explained in simple words at or before its FIRST use in the body -> (not found)
  - Evidence: 'hallucinate' is explained in simple words at or before its FIRST use in the body -> (not found)
  - Evidence: Other problem -> "AI model"
  - Evidence: Other problem -> "language model"
  - Judge reasoning: The lesson explains most terms clearly before or at their first mention. However, it fails to provide a formal definition for 'AI model' before using it, fails to define 'language model' (it only defines the abbreviation), and does not define 'index' (it only defines 'indexing') or 'hallucinate' (only 'hallucination').
  - Fix requested: Add a simple explanation for 'AI model' in the 'Before we start' section. For 'language model', 'index', and 'hallucinate', provide a brief definition before or at their first occurrence to match the definitions provided for the other terms.

- **L6_FLOW: Builds step by step** _(coherent teaching flow, llm check)_
  - Requirement: Ideas are introduced before they are used; sections go from what -> why -> how -> example -> limits -> recap; each section links to the previous one; nothing is repeated without purpose.
  - Evidence: Sections follow the planned order: what you will learn -> before we start (the prerequisite) -> what is it -> why -> how -> example -> limits -> recap -> check yourself -> key words -> learn more. (This order is required; do not fail it for having the prerequisite before the definition.) -> "The section 'Key words' is missing from the lesson."
  - Evidence: 'generation' is explained 4 times in the body (AUTOMATIC PRE-CHECK). met=true only if every repeat adds something new; re-glossing the same meaning is padding. -> "The term 'generation' is defined in the introduction of RAG (as part of the name), in the RAG breakdown (as a step), and in the process description. It is not defined 4 distinct times with new meaning."
  - Judge reasoning: The lesson follows a logical flow and introduces terms well. However, it is missing the 'Key words' section required by the structure and fails the automatic pre-check regarding the term 'generation'.
  - Fix requested: Add a 'Key words' section after 'Check yourself' that defines terms like RAG, LLM, Chunking, and Embeddings. For the 'generation' requirement, ensure you explain the term in four distinct contexts (e.g., as part of the acronym, as the final step of the pipeline, as a creative process in LLMs, and as a contrast to retrieval).

## Attempt 3 (regenerate): FAIL

**What changed in this draft (in response to the previous rejection):**
- `L3_JARGON`: Targeted edits failed twice, so the lesson was rewritten from scratch with this failure given as an explicit constraint.
- `L6_FLOW`: Targeted edits failed twice, so the lesson was rewritten from scratch with this failure given as an explicit constraint.
- `R4_LENGTH`: Targeted edits failed twice, so the lesson was rewritten from scratch with this failure given as an explicit constraint.

**What failed and why:**

- **L1_ACCURACY: No false or misleading claims** _(accurate & grounded, llm check)_
  - Requirement: Every technical claim agrees with the reference facts. No listed misconception is stated or implied as true. Simplifications are allowed only if they do not create a wrong belief (a misconception from the reference sheet, even softened, is a FAIL).
  - Evidence: ABSOLUTE CLAIM: "Retraining means teaching an AI model from the very beginning or changing how it thinks permanently." The word 'permanently' makes this an all-or-nothing claim. met=true ONLY if it is literally true with no exceptions according to the reference facts (check the facts about limits). -> "Retraining means teaching an AI model from the very beginning or changing how it thinks permanently."
  - Evidence: Other problem -> "Retraining means teaching an AI model from the very beginning or changing how it thinks permanently."
  - Judge reasoning: The lesson is mostly accurate and helpful for the target audience. However, it makes an absolute claim about retraining: "Retraining means... changing how it thinks permanently." Since fine-tuning (a form of retraining) involves updating weights, it isn't strictly 'the beginning', and suggesting it changes how it thinks 'permanently' is an oversimplification that violates the strict criteria for absolute, unqualified claims about model behavior. All other items are met or accurate. I checked every claim against the provided reference sheet and the lesson text. All claims are accurate and properly contextualized for a beginner, with no misleading generalizations or misconceptions presented as fact. I checked the lesson content against the provided reference facts and definitions. All technical claims, including the description of the LLM, the RAG process, and the role of embeddings, accurately reflect the reference material without introducing misconceptions.
  - Fix requested: Change the sentence to: 'Retraining typically involves updating the model's internal parameters (weights) to incorporate new information, whereas RAG keeps this information separate.'

- **L3_JARGON: Every technical term explained** _(clear, no unexplained jargon, llm check)_
  - Requirement: Every technical or English-uncommon term is explained in simple words at or before its first use in the body (a glossary at the end alone does not count). Acronyms are expanded on first use.
  - Evidence: 'AI model' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "Retraining means teaching an AI model from the very beginning or changing how it thinks permanently.". Mark met=true ONLY if you can quote an earlier explanation. -> "Retraining means teaching an AI model from the very beginning"
  - Evidence: 'retrieve' is explained in simple words at or before its FIRST use in the body. AUTOMATIC PRE-CHECK found no explanation in the sentence of first use: "It simply retrieved the right page and generated the answer.". Mark met=true ONLY if you can quote an earlier explanation. -> (not found)
  - Evidence: 'augmentation' is explained in simple words at or before its FIRST use in the body -> (not found)
  - Evidence: 'chunking' is explained in simple words at or before its FIRST use in the body -> (not found)
  - Evidence: 'index' is explained in simple words at or before its FIRST use in the body -> (not found)
  - Evidence: 'indexing' is explained in simple words at or before its FIRST use in the body -> (not found)
  - Judge reasoning: The lesson introduces several technical terms without providing a clear, simple explanation before their first usage in the text. Specifically, terms like 'AI model', 'retrieve', 'augmentation', 'chunking', 'index', 'indexing', 'hallucinate', 'knowledge cutoff', 'trained', and 'database' were not defined before they appeared.
  - Fix requested: Add a simple sentence defining each missing term before its first use. For example, explain 'knowledge cutoff' as 'a date after which the AI does not know any new events or facts' and 'database' as 'a digital storage system used for keeping information organized so it can be searched quickly'.

- **L6_FLOW: Builds step by step** _(coherent teaching flow, llm check)_
  - Requirement: Ideas are introduced before they are used; sections go from what -> why -> how -> example -> limits -> recap; each section links to the previous one; nothing is repeated without purpose.
  - Evidence: 'retrieval' is explained 5 times in the body (AUTOMATIC PRE-CHECK). met=true only if every repeat adds something new; re-glossing the same meaning is padding. -> "1. Retrieval: This means finding the right information from your own documents. ... 2. Retrieval: When you ask a question, the system searches the database. It finds the chunks that have a meaning most similar to your question. ... 2. Retrieval: A student asks, "Can I use a calculator in the exam?" The system looks through your digital cabinet. ... If the retrieval step picks the wrong document ... During retrieval, the system finds relevant chunks and adds them to the prompt."
  - Judge reasoning: The lesson is structured logically and introduces concepts sequentially. However, it fails the automatic 'retrieval' repetition check because the term is merely re-defined or used in different steps of the process rather than adding conceptual depth or new information across 5 distinct explanations.
  - Fix requested: Remove the repetitive mentions of 'retrieval' and focus on defining the mechanism once clearly, or if keeping 5 mentions, ensure each one introduces a unique technical nuance (e.g., semantic search vs keyword search, vector similarity, retrieval windows, or performance metrics).

_Retry budget exhausted, so the loop stopped here._

## Final scorecard (shipped attempt)

| Check | Dimension | Result | Metrics |
|---|---|---|---|
| R1_STRUCTURE Required sections present | coherent teaching flow | PASS |  |
| R2_SENTENCES Short sentences | beginner-friendly language | PASS | avg_sentence_words=12.2, sentences=83, over_cap=0 |
| R3_READABILITY Plain-English readability | beginner-friendly language | PASS | flesch=66.5 |
| R4_LENGTH Right length for one sitting | covers the key points | PASS | word_count=1062 |
| R5_QUIZ Self-check with answers | teaches by example | PASS | quiz_questions=4, quiz_has_answers=True |
| R6_RESOURCES Verified links to learn more | teaches by example | PASS | links=4, verified_used=4, videos=2 |
| L1_ACCURACY No false or misleading claims | accurate & grounded | FAIL | items_checked=81, items_unmet=1, extra_problems=1, ungrounded_dropped=0, votes=1 |
| L2_COVERAGE All must-cover points taught | covers the key points | PASS | items_checked=9, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L3_JARGON Every technical term explained | clear, no unexplained jargon | FAIL | items_checked=23, items_unmet=10, extra_problems=7, ungrounded_dropped=3, votes=1 |
| L4_EXAMPLES Concrete analogy and walk-through | teaches by example | PASS | items_checked=5, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L5_LEARNER_FIT Fits a non-native English beginner | beginner-friendly language | PASS | items_checked=5, items_unmet=0, extra_problems=0, ungrounded_dropped=0, votes=1 |
| L6_FLOW Builds step by step | coherent teaching flow | FAIL | items_checked=5, items_unmet=1, extra_problems=0, ungrounded_dropped=1, votes=1 |

## What the system learned from this run

- L1_ACCURACY: reinforced existing guideline G4
- L2_COVERAGE: reinforced existing guideline G4
- L3_JARGON: reinforced existing guideline G3
- L6_FLOW: new guideline G5 -> Introduce and define a technical concept only once in a dedicated section or paragraph to avoid repetitive padding.
- R4_LENGTH: new guideline G6 -> Ensure the final draft contains between 850 and 1800 words to provide sufficient depth and coverage for a standard lesson.

Active guidelines now in memory: 6 | learned rubric checks: 0

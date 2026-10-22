# Introduction to RAG (Retrieval-Augmented Generation)

## What you will learn
* What an LLM is and its limits.
* How RAG helps an AI find correct answers.
* The simple steps of how RAG works.
* Why RAG is useful for private or new data.

## Before we start: LLM
To understand RAG, you must know about an LLM. LLM stands for Large Language Model. A model is an AI program designed to recognize patterns. It is an AI program trained on a huge amount of text. Being trained means the AI has learned by reading billions of words. It predicts the next words in a sentence to talk like a human.

Think of an LLM like a student who studied only until a specific exam date. The student has read many books and knows a lot of general facts. However, the student does not know what happened after that date. Also, the student cannot read your private diary or your college rulebook. If you ask a question outside their knowledge, they might guess or lie confidently. This guessing behavior is called hallucination. A hallucination means the AI gives a wrong answer but speaks in a very sure tone.

## What is RAG?
RAG stands for Retrieval-Augmented Generation. Let us break this down into three parts:
1. Retrieval: Finding the right information from your own documents.
2. Augmented: Adding this found information to your question as a helper. A prompt is the input or question you give to the AI. You use a prompt to tell the AI what to do.
3. Generation: The AI writes a clear answer using the helper information.

RAG lets the AI "look up" facts before it writes an answer. It does not change the AI's internal memory. It just gives the AI an open book to check while it answers.

## Why does it matter?
RAG is very useful for several reasons:
* It uses your own private or recent information.
* It reduces hallucination because the AI reads facts first.
* It can show you the sources for every answer.
* You can add new information without retraining the whole AI. Retraining means teaching the AI model from scratch or changing how it thinks permanently.

## How does it work?
The process happens in two main phases. First, we prepare the data. Preparing data is called indexing.

1. Collect: Gather all your documents, like PDFs or text files.
2. Chunking: Split these documents into small pieces called chunks. A chunk is just a small part of a larger file.
3. Embed: Turn these chunks into embeddings. An embedding is a long list of numbers that represents the meaning of the text. Because computers love math, they use these numbers to compare meanings.
4. Store: Save these numbers in a search database. A database is a computer program used to store and quickly find information.

Next, we answer your question. 

5. Search: When you ask a question, the system finds the chunks most similar to your question.
6. Augment: The system takes those chunks and puts them into the prompt along with your question.
7. Generate: The LLM reads the question and the chunks, then writes the final answer.

## Let's follow one example
Imagine your college has a new rulebook for exams.

1. Collect: The college collects the 50-page exam rulebook.
2. Chunking: It breaks the book into small, readable paragraphs called chunks.
3. Embed: It converts these paragraphs into lists of numbers, known as embeddings.
4. Store: These are saved in a search database for later use.
5. Search: You ask, "Can I use a calculator in the exam?" The system finds the paragraph about "calculators" in the rulebook.
6. Augment: The system sends this paragraph to the AI with your question, forming a new prompt.
7. Generate: The AI reads the paragraph and says, "Yes, you can use a basic calculator."

This works well because the AI relies on the rulebook, not its own memory.

## What it cannot do
RAG is not magic. It has limits:
* If the search finds the wrong paragraph, the answer will be wrong.
* If the information is missing from your documents, the AI still might guess.
* RAG reduces hallucination, but it does not stop it completely.

## Quick recap
* An LLM is an AI that predicts text but has limits.
* RAG gives the AI access to your own private documents.
* Chunks are small pieces of text from your files.
* Embeddings are lists of numbers that help us find similar text.
* RAG does not retrain the AI; it just adds context to the prompt.
* Always check the answers because the AI can still make mistakes.

## Check yourself
1. Does RAG retrain the LLM with your data?
   Answer: No, it just gives the LLM extra info to read.
2. What is a hallucination?
   Answer: When an AI gives a wrong answer but sounds very sure.
3. Why do we split documents into chunks?
   Answer: To help the system find the most relevant info for your question.
4. If your document has wrong info, will the AI's answer be correct?
   Answer: No, the AI will use the wrong info from your document.

## Learn more
- [What is Retrieval-Augmented Generation (RAG)? | IBM Technology](https://www.youtube.com/watch?v=T-D1OfcDW1M) - IBM, 7-minute video. A simple story about how RAG works using a notebook example.
- [What is RAG? - Retrieval-Augmented Generation AI Explained - AWS](https://aws.amazon.com/what-is/retrieval-augmented-generation/) - AWS, article. A clear written guide on why companies use RAG for better accuracy.
- [7-Introduction To RAG(Retrieval-Augmented Generation?) In Hindi](https://www.youtube.com/watch?v=DKg6XUnclm8) - Krish Naik, 12-minute video. An introduction to the concept explained in Hindi.
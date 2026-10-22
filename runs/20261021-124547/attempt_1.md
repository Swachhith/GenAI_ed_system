# Introduction to RAG

## What you will learn
- What a large language model is and its limits.
- The meaning of Retrieval-Augmented Generation.
- Why RAG matters for modern AI systems.
- The step-by-step process of how RAG works.
- A real example from an Indian college helpdesk.

## First, what is an LLM?
You may have used ChatGPT to chat or write text.
ChatGPT is powered by an LLM.
An LLM (large language model) is an AI model.
It is trained on a very large amount of text to predict and generate language.
Think of it like a smart student who read many books before an exam.
This student has fixed knowledge.
Its knowledge is only up to its training date, called a knowledge cutoff.
It does not know your private college rules or today's news.
Also, when it does not know something, it can still speak with great confidence.
It can make up false facts, which is called a hallucination.

## What is RAG?
RAG stands for **Retrieval-Augmented Generation**.
It is a method to fix the limits of an LLM.
Let us break the three words down into simple parts.
**Retrieval** means to find relevant information from a set of documents.
**Augmented** means to add or attach that information to your question.
**Generation** means the LLM writes the final answer using the added text.
Think of an open-book exam at your college.
You do not remember every single rule in the textbook by heart.
You look up the right page in the textbook first.
Then you read that page and write the correct answer.
RAG does the exact same thing for an AI model.

## Why does RAG matter?
An LLM alone cannot see your private company or college files.
RAG lets your AI use up-to-date and private information.
It helps reduce made-up answers because the AI reads real facts.
The system can also show the source document to prove its point.
Most importantly, you do not need to retrain the model to update knowledge.
You only update the documents in your storage.

## How does RAG work?
RAG works in a few clear steps.
1. **Collection**: You gather all your documents, like a college rulebook or a product manual.
2. **Chunking**: You split large documents into small pieces called chunks.
3. **Embedding**: You convert each chunk into numbers that capture its meaning. These numbers are called an embedding.
4. **Storage**: You store these embeddings in a searchable place called a vector index or vector database.
5. **Retrieval**: When a user asks a question, the system turns the question into numbers too. It searches the database and picks the few most relevant chunks.
6. **Augmentation**: The system takes those retrieved chunks and adds them to a prompt (the message you type to the AI).
7. **Generation**: The LLM reads the question and the chunks together, then writes a correct answer.

## Let's follow one example
Imagine you join a new college in India.
You want to know the fee payment deadline.
The college rulebook has fifty pages.
First, the system splits those fifty pages into small chunks and stores them.
You type a question into the college helpdesk bot: "What is the last date to pay fees?"
The retrieval step searches the stored chunks and finds the exact paragraph about fee dates.
The augmentation step takes that paragraph and puts it into a prompt for the LLM.
The prompt says: "Use the given text to answer the user question."
The generation step happens when the LLM reads the text and tells you: "The last date to pay fees is July 31."
The LLM did not learn this date during its original training.
It simply read the retrieved text and gave you the answer.

## What RAG cannot do
RAG is very powerful, but it has limits.
It does not change the model weights or retrain the model.
It does not mean the model permanently remembers your documents.
If the retrieval step finds the wrong information, the final answer can still be wrong.
RAG reduces made-up answers, but it does not remove them completely.
The quality of the answer depends fully on the quality of the retrieved chunks.

## Quick recap
- An LLM has a knowledge cutoff and can hallucinate.
- RAG stands for Retrieval-Augmented Generation.
- Retrieval finds facts, augmentation adds them to the prompt, and generation writes the answer.
- Documents are split into chunks and turned into embeddings for easy search.
- RAG uses external documents without retraining the model.
- RAG reduces made-up answers but does not eliminate them.

## Check yourself
1. What does the "Retrieval" part of RAG do?
Answer: It finds relevant information from external documents.

2. Does RAG retrain the LLM on your private data?
Answer: No, it adds retrieved text to the prompt at question time without changing the model.

3. What is an embedding?
Answer: It is a list of numbers that represents the meaning of a text chunk.

4. Why do we split documents into chunks?
Answer: Because models can only read a limited amount of text at once, and chunks help find exact relevant parts.

## Key words
- **LLM**: A large language model trained on text to generate language.
- **Hallucination**: When an AI model confidently states false information.
- **RAG**: Retrieval-Augmented Generation, a method to give external facts to an LLM.
- **Prompt**: The message or input you type to the AI.
- **Chunk**: A small piece of a larger document.
- **Embedding**: A list of numbers that capture the meaning of text.
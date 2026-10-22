# Introduction to RAG

## What you will learn
- What a large language model is and its limitations.
- The simple meaning of RAG and its three main parts.
- How documents are prepared and searched for answers.
- Why RAG helps AI give correct and updated answers.

## First, what is an LLM?
An LLM (large language model) is an AI program trained on massive amounts of text. It can understand questions and write human-like answers. ChatGPT is a famous example of an LLM. 

However, an LLM has big limits. Its knowledge is frozen up to a fixed date. It does not know your college private rules or last week's news. Sometimes, it makes up false facts with great confidence. This bad habit is called hallucination.

## What is RAG?
RAG stands for Retrieval-Augmented Generation. Let us break down these three words one by one. 

First, retrieval means to find relevant information from a collection of documents. Second, augmented means to add that found information to your question. Third, generation means the LLM writes the final answer using the added information. 

## Why does RAG matter?
RAG solves many big problems of AI. It lets the LLM use up-to-date and private information without changing the model. It reduces made-up answers because the AI reads real facts. It can also point to the source document so you can check the truth. 

Think of an open-book exam at your college. You do not memorize the whole textbook. You search the book for the right page, read it, and write the answer. RAG works in the exact same way.

## How does RAG work?
RAG works through a series of clear steps. Follow this numbered list to see how it flows.

1. **Indexing**: You collect documents and split them into small parts called chunks. 
2. **Embedding**: Each chunk is converted into numbers called an **embedding** (a list of numbers that capture the meaning of the text). 
3. **Storage**: These embeddings are stored in a database for fast searching. 
4. **Retrieval**: When you ask a question, the system searches the database and finds the most relevant chunks. 
5. **Augmentation**: The system adds these retrieved chunks to your question in a **prompt** (the message you type to the AI). 
6. **Generation**: The LLM reads the question and the chunks, then writes a correct answer.

## Let's follow one example
Imagine your college has a thick rulebook for attendance and exams. You want to ask a chatbot a question: "What is the minimum attendance needed for my semester exams?"

First, the system looks at your question. It searches the college rulebook chunks and finds the exact page about attendance. Second, the system takes that page and attaches it to your question. Third, it sends both the page and your question to the LLM. Fourth, the LLM reads the page and tells you the exact rule. The LLM does not need to memorize the rulebook beforehand.

## What RAG cannot do
RAG is very helpful, but it is not magic. If the retrieval step finds the wrong page, the final answer will also be wrong. 

RAG reduces made-up answers, but it does not remove them completely. The system only knows what is inside the documents you gave it. If your document is missing important facts, the AI cannot guess them correctly.

## Quick recap
- An LLM has a training cutoff and can make up facts.
- RAG stands for Retrieval-Augmented Generation.
- Retrieval finds relevant text chunks from private documents.
- Augmentation adds those chunks to your question.
- Generation creates the final answer using the added text.
- RAG reduces hallucinations and uses up-to-date information.

## Check yourself
1. What does the retrieval part of RAG do?
Answer: It finds relevant information from a collection of documents.

2. Does RAG retrain the LLM model on your documents?
Answer: No, RAG only adds retrieved text to the prompt at question time.

3. What are embeddings?
Answer: Embeddings are lists of numbers that represent the meaning of text chunks.

4. Why do we split documents into chunks?
Answer: So the system can find and send only the most relevant parts to the LLM.

## Key words
- **LLM**: A large language model trained on text to generate language.
- **Hallucination**: When an LLM confidently makes up false statements.
- **RAG**: Retrieval-Augmented Generation, a method to feed external facts to an LLM.
- **Chunk**: A small piece of a larger document.
- **Embedding**: A list of numbers that capture the meaning of text.
- **Prompt**: The message or input you type to the AI.
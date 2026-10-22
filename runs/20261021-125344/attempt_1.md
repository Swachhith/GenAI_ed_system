# Introduction to RAG (Retrieval-Augmented Generation)

## What you will learn
- What a large language model is and where it fails.
- What the words in Retrieval-Augmented Generation mean.
- How to prepare documents for a search system.
- Why this method stops the AI from making up false answers.

## First, what is an LLM?
An LLM is an AI model trained on huge amounts of text. 
It predicts and generates natural language like a human. 
You might use ChatGPT on your smartphone every day. 
It can write essays, translate languages, and answer questions. 
However, an LLM has big limits. 
It only knows things from its training data up to a cutoff date. 
It does not know your college private rules or last week's cricket score. 
Worse, it can write fluent lies with total confidence. 
This false answer problem is called hallucination.

## What is RAG?
RAG stands for **Retrieval-Augmented Generation**. 
It is a way to fix the limits of an LLM. 
The name has three simple parts. 
First, **retrieval** means to find relevant information from a set of documents. 
Second, **augmented** means to add that found information to the user's question. 
Third, **generation** means the LLM writes the final answer using the added text. 
RAG does not change the model itself. 
It just gives the AI an open book to read right before answering.

## Why does RAG matter?
AI models usually forget private or new facts. 
RAG lets answers use up-to-date and private information. 
It greatly reduces made-up answers because the AI reads real facts. 
Your answers can even point to their source documents. 
Most importantly, you can update the knowledge without retraining the model. 
You just change the documents in your folder.

## How does RAG work?
RAG works in a few clear steps. 
Let us look at how the system prepares and answers.

1. **Indexing documents**: You collect your documents and split them into small pieces. These small pieces are called chunks.
2. **Creating embeddings**: You convert each chunk into an **embedding** (a list of numbers that capture meaning). 
3. **Storing data**: You store these embeddings in a searchable place called a **vector database** (a database designed to search through meaning-based numbers).
4. **Retrieval**: When a user asks a question, the system turns the question into an embedding and finds the most similar chunks.
5. **Augmentation**: The system takes those relevant chunks and adds them to a **prompt** (the message you type to the AI).
6. **Generation**: The LLM reads the prompt with the added chunks and writes the final answer.

## Let's follow one example
Imagine a college helpdesk bot at your college in India. 
The bot needs to answer student questions using the official college rulebook. 

First, we prepare the documents. 
The college collects the fifty-page PDF rulebook. 
The system splits this long PDF into small chunks of one paragraph each. 
It turns each chunk into an embedding and stores them all in a vector index. 

Now, a student types a question into the WhatsApp bot. 
The student asks, "What is the fine for missing the library book return date?" 
Step two is retrieval. 
The system turns this question into numbers and searches the vector index. 
It picks the one paragraph about library fines from the fifty pages. 

Step three is augmentation. 
The system takes that single paragraph about library fines. 
It puts that paragraph into a prompt along with the student's question. 
It adds an instruction that says, "Answer using only this text." 

Step four is generation. 
The LLM reads the paragraph and writes back, "The fine is ten rupees per day." 
The AI did not guess. 
It read the exact rule provided by the retrieval step.

## What RAG cannot do
RAG is very powerful, but it has limits. 
If the retrieval step finds the wrong information, the answer will still be wrong. 
RAG reduces made-up answers, but it does not remove them completely. 
If your document folder misses a fact, the AI cannot answer it correctly. 
The AI can only work with the text you give it during retrieval.

## Quick recap
- An LLM is a language AI with a fixed training cutoff date.
- LLMs can hallucinate and make up facts with high confidence.
- RAG stands for Retrieval-Augmented Generation.
- Documents are split into chunks and turned into embeddings for search.
- Relevant text is retrieved and added to the prompt.
- RAG reduces false answers and lets you update knowledge easily.

## Check yourself
1. What does the retrieval step do in RAG?
Answer: It finds relevant information from a set of documents.

2. Does RAG retrain the LLM on your private files?
Answer: No, it only adds retrieved text to the prompt at question time.

3. Why do we split documents into chunks?
Answer: Because models can only read a limited amount of text at once.

4. Does RAG completely stop the AI from hallucinating?
Answer: No, it reduces false answers, but wrong retrieval can still cause mistakes.

## Key words
- **LLM**: A large language model trained on text to generate language.
- **Hallucination**: When an AI makes up false answers with high confidence.
- **Retrieval**: Finding relevant information from a collection of documents.
- **Augmented**: Adding the found information to the user's question.
- **Generation**: The writing of the final answer by the AI.
- **Chunk**: A small piece of a larger document.
- **Embedding**: A list of numbers that capture the meaning of text.
- **Vector database**: A searchable database designed to find similar embeddings.
- **Prompt**: The message or input you type to give to the AI.
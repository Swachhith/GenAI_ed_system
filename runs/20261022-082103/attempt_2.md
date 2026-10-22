# Introduction to RAG

## What you will learn
- What a large language model is and its limits.
- The simple meaning of Retrieval-Augmented Generation.
- How the four steps of RAG work together.
- Why RAG helps us get correct answers from private documents.

## First, what is an LLM?
An LLM (large language model, an AI program trained on huge amounts of text to write like a human) is very powerful. Trained means the AI learned from reading text data. You can chat with it like a friend on WhatsApp. It can write essays, explain science, and translate languages. However, an LLM has two big limits. First, its training data (the text used to teach the AI) stopped on a fixed date in the past. This fixed date is called a knowledge cutoff. It does not know what happened yesterday. Second, it does not know your private college notes or your company files. When an LLM does not know a fact, it often guesses. It writes a fluent sentence that looks true, but is actually false. In AI, we call this a hallucination (a confident answer made up by the AI).

## What is RAG?
Think of an open-book exam at college. In an open-book exam, you do not memorize every rule. Instead, you look up the exact rule in your textbook when a question comes. RAG works just like this open-book exam. RAG stands for Retrieval-Augmented Generation. Let us break down these three words one by one. Retrieval means to find the right information from a large set of files. Augmented means to add something to make it better. Generation means to create new text as an answer. Retrieval matches looking up the rulebook. Augmented matches adding the found rule to your paper. Generation matches writing the final answer. Put them together, and you get RAG.

## Why does RAG matter?
Imagine you ask an AI model (a computer program trained to think and answer like a human) a question about your college fee rules. Without RAG, the LLM will guess because it has never read your college rulebook. With RAG, the system first finds the exact page about fees from your college rulebook. Then, it gives that page to the LLM. The LLM reads it and writes the correct answer. Your answers become up-to-date and use private files. You also see fewer made-up answers. Best of all, you do not need to retrain the AI model every time a rule changes. You only update your files.

## How does RAG work?
RAG works in four main steps. 
1. Indexing: You collect your documents before anyone asks a question. You split them into small parts called chunks (small pieces of text). Then you turn them into numbers. These numbers are called embeddings (a list of numbers that capture the meaning of text). You store these embeddings in a search index.
2. Retrieval: When a user asks a question, the system turns the question into embeddings. It compares these numbers with your stored chunks. It picks the few most relevant chunks.
3. Augmentation: The system takes your original question and adds the retrieved chunks to it. This combined text becomes the prompt (the message you type to the AI).
4. Generation: The LLM reads the prompt containing the retrieved chunks and writes a clear answer for you.

## Let's follow one example
Let us look at a college helpdesk bot using RAG. 
First, we do the preparation step. 
The college collects the official hostel rulebook PDF. 
The system splits this PDF into small chunks, like paragraph by paragraph. 
Each chunk is converted into embeddings and stored safely. 
Next, a student opens the chat app. 
The student types a question: "What is the last date to pay hostel fees?" 
The system turns this question into embeddings. 
It searches the stored hostel rulebook chunks and finds the exact paragraph about fee dates. 
This is the retrieval step. 
Then, the system places that exact paragraph next to the student's question. 
This is the augmentation step. 
Finally, the LLM reads the paragraph and replies: "The last date to pay hostel fees is July 15." 
This is the generation step. 

## What RAG cannot do
RAG is very useful, but it is not magical. 
If your retrieval step finds the wrong document, the LLM will read the wrong text. 
Then, the final answer will also be wrong. 
RAG reduces made-up answers, but it does not remove them completely. 
The LLM can still misread the correct text. 
You must always check important answers with human eyes. 

## Quick recap
- An LLM has a knowledge cutoff date and can hallucinate facts.
- RAG stands for Retrieval-Augmented Generation.
- Indexing splits documents into chunks and turns them into embeddings.
- Retrieval finds the most useful text chunks for your question.
- Augmentation adds the found text to your prompt.
- Generation lets the LLM write an answer based on the added text.

## Check yourself
1. What does the "R" in RAG stand for?
Answer: Retrieval.

2. True or False: RAG retrains the LLM on your private documents.
Answer: False. RAG adds retrieved text to the prompt without changing the model.

3. Why do we split documents into chunks?
Answer: So the system can find and send only the most relevant parts to the LLM.

4. Does RAG completely stop hallucinations?
Answer: No, it reduces them, but wrong retrieval can still lead to wrong answers.

## Key words
- LLM: A large language model trained on text to generate human-like language.
- Hallucination: A confident answer made up by the AI.
- RAG: Retrieval-Augmented Generation, a method that adds searched documents to an LLM prompt.
- Chunk: A small piece of text split from a larger document.
- Embedding: A list of numbers that capture the meaning of text for searching.
- Prompt: The message you type to the AI.
- Trained: The AI learned from reading text data.
- AI model: A computer program trained to think and answer like a human.
- Knowledge cutoff: A fixed date in the past when the AI training data stopped.
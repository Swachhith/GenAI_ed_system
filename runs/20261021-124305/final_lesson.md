# Introduction to RAG

## What you will learn
- What a large language model is and its limits.
- What the letters in RAG stand for.
- How RAG works step by step with an Indian example.
- Why RAG helps us get correct answers from private documents.

## First, what is an LLM?
A large language model (LLM) is a type of AI (artificial intelligence) trained on huge amounts of text. It knows how to predict the next word and write clear sentences. You might have used ChatGPT to write essays or translate languages. 

An LLM has three main limits. First, its knowledge stops at a specific date called a **knowledge cutoff** (the date up to which the AI was trained). It does not know news from today or your college fees notice issued yesterday. Second, it does not know private papers like your bank statement or your company salary slip. Third, it can sound very confident while making up false facts. This making up of false facts is called **hallucination** (when an AI speaks false information with high confidence). 

## What is RAG?
RAG stands for Retrieval-Augmented Generation. It is a smart way to give new facts to an LLM without changing the model itself. 

Let us break the three words down. 
- **Retrieval**: The system searches through a set of documents to find facts related to your question.
- **Augmented**: The system adds those found facts into your prompt (the message you type to the AI).
- **Generation**: The LLM reads the added facts and writes a correct answer for you.

Think of an open-book exam at your college. You do not memorise the whole library. When the question paper comes, you search the correct textbook, read the right page, and write the answer. RAG works the exact same way for AI. 

## Why does RAG matter?
LLMs are very smart, but they forget new facts and private rules. RAG fixes this problem in four ways. 

First, RAG lets your AI answer questions using up-to-date data. Second, it reduces false answers because the AI reads real facts before writing. Third, RAG can point to its sources, like showing a page number from a rulebook. Fourth, you can update your knowledge files easily without retraining the model. 

## How does RAG work?
RAG works in two main phases: preparation before questions arrive, and processing when a question arrives. 

Here are the numbered steps:
1. **Collect documents**: Gather all the rulebooks, manuals, or notes you want your AI to read.
2. **Split into chunks**: Break long documents into small pieces called **chunks** (small blocks of text).
3. **Turn into embeddings**: Convert each chunk into an **embedding** (a list of numbers that capture meaning). This helps the computer match similar ideas.
4. **Store in a index**: Put these embeddings in a searchable list called a **vector index** (a database designed to search numbers by meaning).
5. **Receive a question**: When you type a question, the system turns your question into an embedding too.
6. **Find matching chunks**: The system matches your question embedding with stored embeddings and picks the top few most relevant chunks.
7. **Add to prompt**: The system places those retrieved chunks and your question together into a prompt.
8. **Generate the answer**: The LLM reads the prompt and writes a final answer based only on those chunks.

## Let's follow one example
Imagine you join a new college in Delhi. You want to know the hostel fee refund rule. 

You open the college WhatsApp helpdesk bot powered by RAG. 
1. You type: "What is the last date for hostel fee refund?"
2. The system turns your question into numbers and searches the college rulebook index.
3. It finds the exact paragraph about hostel fees. This is the **Retrieval** step.
4. The system copies that paragraph and adds it to your question. This is the **Augmented** step.
5. The LLM reads the added paragraph. It writes a reply. It says: "The last date to get a full hostel fee refund is July 15." This is the **Generation** step.

Where does this analogy stop working? A human student reads the rulebook and uses memory for future exams. The LLM does not remember your question or the rulebook after answering. It reads the text fresh every single time.

## What RAG cannot do
RAG is very powerful, but it has limits. If the retrieval step fails to find the right document, the LLM cannot guess the missing fact. It might still make up a wrong answer. RAG reduces hallucinations, but it does not remove them completely. 

## Quick recap
- An LLM is a text-writing AI with a fixed knowledge cutoff and a habit of hallucination.
- RAG stands for Retrieval-Augmented Generation.
- It finds relevant text, adds it to the prompt, and lets the LLM write the answer.
- Documents are split into chunks and stored as embeddings to make search fast.
- RAG does not change the model weights or retrain the AI.
- RAG helps bots answer from private files like college rulebooks or company manuals.

## Check yourself
1. What does the "R" in RAG stand for?
Answer: Retrieval.

2. Does RAG retrain the LLM on your documents?
Answer: No, RAG adds retrieved text to the prompt at question time without changing the model.

3. What is a chunk?
Answer: A small piece of text made by splitting a large document.

4. Does RAG remove all hallucinations completely?
Answer: No, it reduces them, but wrong retrieval can still lead to wrong answers.

## Key words
- **Knowledge cutoff**: The date up to which the AI was trained on data.
- **Hallucination**: When an AI speaks false information with high confidence.
- **Prompt**: The message or question you type to the AI.
- **Chunks**: Small blocks of text made by splitting a large document.
- **Embeddings**: A list of numbers that capture the meaning of text.
- **Vector index**: A database designed to search numbers by meaning.
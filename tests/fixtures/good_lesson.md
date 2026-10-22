# Introduction to RAG: How AI Finds the Right Answer

## What you will learn

- What an LLM is, and what it cannot do.
- What RAG means, word by word.
- Why companies use RAG.
- How RAG works, step by step, with one full example.

## First, what is an LLM?

You may have used ChatGPT. It is an **LLM**. LLM means "Large Language Model". It is a computer program that reads your message and writes a reply.

How did it learn to write? It read a huge amount of text from books and websites. This text is called its **training data** (the material it learned from). From this text, it learned how words usually follow each other.

But an LLM has three big problems.

1. It only knows things up to a certain date. This date is called the **knowledge cutoff** (the last day of its learning). Ask about yesterday's news, and it may not know.
2. It does not know private things. It has never seen your college rulebook. It has never seen your company's files.
3. Sometimes it makes up answers. The answer sounds confident, but it is false. This is called a **hallucination** (a made-up answer).

So we need a way to give the LLM the right facts. That way is RAG.

## What is RAG?

RAG stands for **Retrieval-Augmented Generation**. Let us understand each word.

- **Retrieval** means "finding and bringing back". The system finds useful information for your question.
- **Augmented** means "added to" or "made bigger". The found information is added to your question.
- **Generation** means "creating". The LLM creates the answer.

So RAG is simple. First, find the right information. Next, add it to the question. Then, let the LLM write the answer.

Think of an open-book exam. In a normal exam, you answer only from memory. You may forget things. In an open-book exam, you first find the right page in the textbook. Then you write your answer using that page. RAG gives the LLM an open-book exam.

The analogy has one limit. A student remembers the book after the exam. The LLM does not. It uses the found pages only for that one answer.

## Why does RAG matter?

RAG solves the three problems we saw.

- **Fresh facts.** You can add new documents any time. The answers then use the new facts.
- **Private facts.** A company can use its own files. The LLM can now answer about them.
- **Fewer made-up answers.** The LLM has real text in front of it. So it guesses less.
- **Proof.** The answer can show which document it used. You can check it yourself.
- **Lower cost.** Changing the LLM itself is slow and costly. With RAG, you only update the documents.

This is why many companies use RAG. Banks, hospitals, colleges and online shops use it for helpdesk chatbots.

## How does RAG work?

RAG has two parts. First, we prepare the documents once. Then, we answer each question.

**Part A: Prepare the documents**

1. **Collect.** Gather all the documents. These can be PDFs, web pages or notes.
2. **Cut into pieces.** Long documents are cut into small parts. Each small part is called a **chunk** (a short piece of text, like one paragraph).
3. **Turn into numbers.** Each chunk is changed into a list of numbers. This list is called an **embedding** (numbers that show the meaning of the text). Chunks with similar meaning get similar numbers.
4. **Store.** All the chunks and their numbers are saved in a special store. It works like a library index card system. It can quickly find chunks with a similar meaning.

**Part B: Answer a question**

1. **Retrieve.** Your question is also turned into numbers. The system finds the chunks whose numbers are closest. It picks the top three to five chunks.
2. **Augment.** The system builds a **prompt** (the full message sent to the LLM). The prompt has your question, the chosen chunks and a short instruction: "Answer using only this information."
3. **Generate.** The LLM reads the prompt and writes the answer.

Why not send all the documents? An LLM can read only a limited amount of text at one time. So we send only the most useful pieces.

## Let's follow one example

Meet Priya. She is a new student at a college in Pune. The college has a helpdesk chatbot that uses RAG.

**Preparation (done before Priya comes).** The college collected its rulebook, fee notice and hostel guide. The system cut them into small chunks. One chunk says: "Students need 75% attendance to write the final exam." The system turned every chunk into numbers and stored them.

**Step 1: Priya asks a question.** She types: "How much attendance do I need for exams?"

**Step 2: Retrieve.** The system turns her question into numbers. It finds the closest chunks. The attendance rule chunk is the best match. A chunk about medical leave also matches.

**Step 3: Augment.** The system makes a prompt. It contains Priya's question, the two chunks and the instruction "Answer using only this information."

**Step 4: Generate.** The LLM writes: "You need at least 75% attendance to write the final exam. If you were sick, you can apply for medical leave. (Source: College Rulebook, page 12)."

Priya gets a correct answer from her own college's rules. A normal LLM could not do this. It has never seen this rulebook.

## What RAG cannot do

RAG is very useful, but it is not magic.

- **Bad search means bad answers.** If the system finds the wrong chunk, the answer will be wrong.
- **Missing facts stay missing.** If the rule is not in any document, RAG cannot find it.
- **Mistakes can still happen.** RAG reduces made-up answers. It does not remove them fully.
- **The LLM does not learn.** RAG does not change the LLM. Remove the documents, and the LLM forgets nothing because it never stored them.

## Quick recap

- An LLM writes answers, but it does not know new or private facts.
- RAG means: find the information, add it to the question, then write the answer.
- Documents are cut into chunks and saved as numbers called embeddings.
- For each question, the closest chunks are found and added to the prompt.
- RAG gives fresher, more correct answers with sources.
- RAG can still fail if the search finds the wrong text.

## Check yourself

1. What are the three words in RAG?
   Answer: Retrieval, Augmented and Generation.
2. Why can't a normal LLM answer questions about your college rulebook?
   Answer: It never saw the rulebook in its training data.
3. What is a chunk?
   Answer: A small piece of a long document, like one paragraph.
4. Does RAG change the LLM itself?
   Answer: No. It only adds useful text to the prompt for each question.

## Key words

- **LLM (Large Language Model):** a computer program that reads and writes text.
- **Training data:** the text an LLM learned from.
- **Knowledge cutoff:** the last date of an LLM's learning.
- **Hallucination:** a confident answer that is false.
- **Chunk:** a small piece of a document.
- **Embedding:** a list of numbers that shows the meaning of text.
- **Prompt:** the full message sent to the LLM.
- **Retrieval:** finding the useful information.

## Learn more

- [What is Retrieval-Augmented Generation (RAG)?](https://www.youtube.com/watch?v=T-D1OfcDW1M) - IBM Technology, 7-minute video. A scientist explains RAG on a board, step by step.
- [Large Language Models explained briefly](https://www.youtube.com/watch?v=LPZh9BOjkQs) - 3Blue1Brown, 8-minute video. Clear pictures of how an LLM works.
- [What is RAG?](https://aws.amazon.com/what-is/retrieval-augmented-generation/) - AWS, short article. The main benefits of RAG in simple words.

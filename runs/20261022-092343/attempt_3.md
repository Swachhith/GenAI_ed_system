# An Introduction to RAG

## What you will learn
* How a computer model can use private or new information.
* Why current AI systems sometimes provide incorrect or made-up answers.
* How the three steps of RAG help fix these problems.
* A simple way to see RAG in action using an everyday example.

## Before we start: LLM
To understand RAG, you must first know about an **LLM** (Large Language Model). An LLM is a computer program trained on massive amounts of text to predict and write human-like language. You might have seen one like ChatGPT. 

However, LLMs have limits. They only know information up to their "knowledge cutoff" date. They do not know about your private notes or news from yesterday. Also, they can sometimes speak with great confidence while being completely wrong. We call this a **hallucination**. A hallucination is when an AI makes up facts that are not true. Think of an LLM like a student who has read every book in a library but hasn't visited the library since 2021. If you ask about a 2024 cricket match, the student might guess incorrectly because they have not read the latest news.

## What is RAG?
**RAG** stands for **Retrieval-Augmented Generation**. Let us look at these three parts. 

1. **Retrieval**: This means finding the right information from your own documents. 
2. **Augmented**: This means adding that found information to your original question. 
3. **Generation**: This is when the LLM writes an answer using both the question and the added information. 

Think of RAG as giving that student from our library example a copy of today's newspaper. The student can now read the current news and use it to answer your question accurately. 

## Why does it matter?
RAG is very useful for a few reasons. First, it allows your AI to answer questions about private data, like your college’s rulebook or a company’s manual. Second, it reduces hallucinations because the model is forced to use the facts you provide instead of just guessing. Third, it allows the AI to give you links or references to where it found the answer. Finally, you do not need to retrain the model to teach it new things. You simply update your documents. Retraining means teaching an AI model from the very beginning or changing how it thinks permanently. With RAG, the knowledge stays in the documents, not inside the AI itself.

## How does it work?
The process follows these simple steps:

1. **Indexing**: You collect your documents and break them into smaller parts called **chunks**. A chunk is just a small piece of text from a larger file. You turn these chunks into **embeddings**. An embedding is a list of numbers that represents the meaning of the text. You store these in a database for easy searching.
2. **Retrieval**: When you ask a question, the system searches the database. It finds the chunks that have a meaning most similar to your question.
3. **Augmentation**: The system puts your original question and the found chunks together into one big message. This is called a prompt.
4. **Generation**: The LLM reads this prompt and writes a clear answer. Because it has the relevant chunks in front of it, it can provide a much more accurate answer.

## Let's follow one example
Imagine you are the head of a college helpdesk. Students ask many questions about the college’s exam rules.

1. **Indexing**: You take the long PDF rulebook. You split it into short chunks, like one rule per chunk. You turn these into embeddings so the computer understands the meaning of each rule. You store them in a digital cabinet.
2. **Retrieval**: A student asks, "Can I use a calculator in the exam?" The system looks through your digital cabinet. It finds the specific chunk that says, "Students are allowed to use basic calculators for Math exams."
3. **Augmentation**: The system creates a new note. It says: "Answer the student's question about calculators. Use this information: 'Students are allowed to use basic calculators for Math exams.'"
4. **Generation**: You give this note to the LLM. It writes a response for the student: "Yes, you can use a basic calculator for your Math exam, as per the college rulebook." 

The system did not need to be retrained, and it did not make up a rule. It simply retrieved the right page and generated the answer.

## What it cannot do
RAG is helpful, but it is not perfect. If the retrieval step picks the wrong document or misses the right one, the LLM will still provide a wrong answer. It reduces the chance of made-up answers, but it does not remove the possibility completely. If your documents are poorly written or incomplete, the AI's answer will also be incomplete. Think of it like an open-book exam. If you search for the wrong page in your textbook, you will still write the wrong answer on your test paper.

## Quick recap
* An LLM is a model trained to predict and write text.
* LLMs have a knowledge cutoff and can sometimes hallucinate, or lie.
* RAG stands for Retrieval-Augmented Generation, which uses external documents.
* The system breaks documents into chunks and converts them into embeddings.
* During retrieval, the system finds relevant chunks and adds them to the prompt.
* RAG improves accuracy and lets you cite sources without retraining the AI.

## Check yourself
1. Why does an LLM sometimes give wrong answers?
Answer: Because it has a knowledge cutoff and can hallucinate, or make things up.

2. Does RAG retrain the model with your private documents?
Answer: No, RAG simply provides the documents to the model during the question.

3. What are embeddings used for in RAG?
Answer: Embeddings are lists of numbers that represent meaning, helping the system find relevant information.

4. If the retrieval step finds the wrong document, will the final answer be correct?
Answer: No, the final answer quality depends on the quality of the retrieved information.

## Key words
* **LLM**: A computer program trained to understand and write human language.
* **Hallucination**: When an AI model confidently states something that is not true.
* **Retrieval**: The action of finding specific data from a large collection of files.
* **Chunk**: A small piece of text taken from a larger document.
* **Embedding**: A list of numbers that helps the computer compare the meaning of text.
* **Prompt**: The text, question, or instruction you give to an AI model.

## Learn more
- [What is Retrieval-Augmented Generation (RAG)? | IBM Technology](https://www.youtube.com/watch?v=T-D1OfcDW1M) - IBM, 7-minute video. A simple story showing how RAG works like a search and read process.
- [What is RAG? - Retrieval-Augmented Generation AI Explained - AWS](https://aws.amazon.com/what-is/retrieval-augmented-generation/) - AWS, article. A clear breakdown of why RAG helps businesses use their own data.
- [7-Introduction To RAG(Retrieval-Augmented Generation?) In Hindi](https://www.youtube.com/watch?v=DKg6XUnclm8) - Krish Naik, 15-minute video. An introduction to RAG in Hindi if you want to hear these concepts in your primary language.
- [What Is Retrieval-Augmented Generation aka RAG](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/) - NVIDIA, article. Explains how RAG acts like a clerk searching files to help a judge decide a case.
# Introduction to RAG (Retrieval-Augmented Generation)

## What you will learn
- What a large language model is and why it makes mistakes.
- What the letters in RAG stand for in plain English.
- How preparation, retrieval, augmentation, and generation work together.
- Why RAG helps us get accurate and up-to-date answers.

## Before we start: large language model
You will meet the term **large language model**. A large language model means an artificial intelligence system trained on massive amounts of text to predict and generate human language. 

You might have used chatbots like ChatGPT. These models are powerful, but they have major limits. An LLM's built-in knowledge is fixed at training time. This is called a **knowledge cutoff**. 

The model does not know private company documents or very recent news after that cutoff date. Also, LLMs can sound very confident while writing completely false facts. This common problem is called **hallucination**. 

Imagine a college student who memorised a big textbook years ago. They forgot today's notices and do not know your college fee rules. If someone asks them a tricky question, they might guess an answer and sound very sure. That is how an LLM behaves.

## What is RAG?
You will meet the term **RAG**. RAG stands for **Retrieval-Augmented Generation**. 

Let us break down those three important words one by one. **Retrieval** means finding relevant information from an external source. **Augmented** means adding that found information to your question. **Generation** means the LLM writes the final answer using the added text. 

RAG acts like an open-book exam for your AI. Instead of forcing the model to rely only on its memory, the system looks up the right pages first. Then, it hands those pages to the AI to read and answer.

## Why does it matter?
RAG solves many big problems with standard AI models. First, your answers can use up-to-date or private information. You do not need to retrain the model when your documents change. 

Second, RAG reduces made-up answers because the model reads real facts. Third, answers can point directly to their source documents. 

Think of a local kirana shop owner. If they only rely on memory, they might quote old prices. With RAG, they check today's price list notebook before speaking to a customer.

## How does it work?
Building a RAG system involves several clear steps. Let us look at how the data gets ready and how a question gets answered.

1. **Indexing**: The system collects your documents. It splits them into small pieces called **chunks**. A chunk is a short piece of text from a larger document. 
2. **Embedding**: The system converts each chunk into an **embedding**. An embedding is a list of numbers that capture the meaning of the text. 
3. **Storage**: The system stores these embeddings in a searchable place so similar text can be found quickly.
4. **Querying**: When you type a question, the system turns your question into an embedding too. 
5. **Retrieval**: The system searches the stored chunks and picks the few most relevant ones.
6. **Augmentation**: The system places those retrieved chunks into a prompt along with your original question.
7. **Generation**: The LLM reads the prompt and writes the final answer using only the provided facts.

## Let's follow one example
Let us look at a college helpdesk bot answering questions from a rulebook. 

First, the college collects the rulebook PDF. The system splits the PDF into small chunks. It turns every chunk into a list of numbers representing meaning and stores them. This setup happens before any student asks a question.

Next, a student types a question: "What is the fine for returning a library book late?" 

The system turns the student's question into numbers. It compares those numbers against the stored chunks. It finds chunk number twelve, which talks about library fines. 

Then, the system copies chunk twelve into a prompt. It adds the student's question and an instruction to use the text. 

Finally, the LLM reads chunk twelve and generates the final answer: "The fine for returning a library book late is ten rupees per day." The answer is accurate because the model read the real rulebook page.

## What it cannot do
RAG is very helpful, but it has limits. RAG reduces made-up answers, but it does not remove them completely. 

If your retrieval step finds the wrong information, the model can still give a wrong answer. Also, RAG does not change the model weights. The knowledge lives in your documents, not inside the AI memory. 

If your documents have errors, the final answer will also have errors. Garbage in means garbage out.

## Quick recap
- A large language model predicts text but has a knowledge cutoff and can hallucinate.
- RAG stands for Retrieval-Augmented Generation.
- Documents are split into chunks and stored in a searchable index.
- Retrieval finds the most relevant text pieces for your question.
- Augmentation adds the retrieved text and question into a prompt for the LLM.
- RAG reduces false answers and lets AI use private documents without retraining.

## Check yourself
1. What is a knowledge cutoff in an LLM?
   Answer: It is the date up to which the model's training data was collected.
2. What does the word retrieval mean in RAG?
   Answer: It means finding relevant information from an external knowledge source.
3. Does RAG retrain the model weights?
   Answer: No, the model weights stay the same; text is added to the prompt.
4. Why do we split documents into chunks?
   Answer: Models can only read limited text at once, and chunks help find exact details.

## Key words
- **Large language model**: An artificial intelligence model trained on massive text to predict language.
- **Hallucination**: When an AI model produces fluent but false statements.
- **RAG**: Retrieval-Augmented Generation, a method to supply external facts to an LLM.
- **Chunk**: A small piece of text split from a larger document.
- **Embedding**: A list of numbers that capture the meaning of a text piece.
- **Prompt**: The input text given to an AI model with instructions and context.

## Learn more
- [What is Retrieval-Augmented Generation (RAG)? | IBM Technology](https://www.youtube.com/watch?v=T-D1OfcDW1M) - IBM Technology, 7-minute video. A short video explaining RAG with a simple story.
- [What is RAG? - Retrieval-Augmented Generation AI Explained - AWS](https://aws.amazon.com/what-is/retrieval-augmented-generation/) - AWS, article. A short written explanation with the main benefits of RAG.
- [What Is Retrieval-Augmented Generation aka RAG](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/) - NVIDIA Blogs, article. Explains RAG with a court-clerk example and real uses.
- [7-Introduction To RAG(Retrieval-Augmented Generation?) In Hindi](https://www.youtube.com/watch?v=DKg6XUnclm8) - Krish Naik, Hindi video. A clear introduction to RAG in Hindi.
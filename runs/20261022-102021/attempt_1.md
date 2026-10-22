# Introduction to RAG (Retrieval-Augmented Generation)

## What you will learn
- What a large language model is and why it makes mistakes.
- What the three parts of RAG mean.
- How preparation, retrieval, augmentation, and generation work step by step.
- Why RAG helps us get accurate answers from private documents.

## Before we start: What is a large language model?
You will meet the term **large language model** or **LLM**. An LLM is an artificial intelligence model trained on a very large amount of text to predict and generate language. 

Think of an LLM like a brilliant student who read every book in a giant library before entering an exam hall. When you ask a question, the student uses memory to write an answer. 

However, this student has strict limits. The model's built-in knowledge is fixed at training time. This fixed limit is called a knowledge cutoff. It does not automatically know events after that date or your organization's private documents. 

Also, when the student forgets a fact, it does not say "I do not know." Instead, it can produce fluent but false statements. This bad habit is commonly called **hallucination**. If you ask an LLM about last week's exam rules at your local college, it might invent a rule with total confidence.

## What is RAG?
You will meet the term **RAG**. RAG stands for Retrieval-Augmented Generation. Let us look at all three words carefully to understand the system. 

First, **Retrieval** means to find relevant information from a collection of documents. Second, **Augmented** means to add that found information directly to your question. Third, **Generation** means the LLM writes the final answer using the added information. 

Imagine you are sitting for an open-book exam in your college. You do not try to remember every single rule in your head. Instead, when a question arrives, you look up the correct page in your rulebook, place that page on your desk, and write your answer using those facts. RAG is simply that open-book method for artificial intelligence.

## Why does it matter?
Standard LLMs can easily give wrong answers about new topics or private rules. RAG fixes this big problem in several wonderful ways. 

First, answers can use up-to-date or private information without changing the model itself. Second, RAG greatly reduces made-up answers because the model reads actual facts before writing. Third, answers can point to their sources so you can check where the facts came from. 

Best of all, knowledge can be updated simply by editing or adding documents. There is no need for expensive retraining of the model.

## How does it work?
Building and using a RAG system happens in two main phases. The first phase prepares the documents. The second phase answers the user's question. 

Here are the numbered steps for the entire process:

1. **Document collection**: You gather all the text files, manuals, or rulebooks you want your system to use.
2. **Chunking**: You split your large documents into small pieces so they are easy to read and search.
3. **Embedding creation**: You convert each piece of text into a list of numbers that capture meaning. You will meet the word **embedding**. An embedding is a list of numbers representing text meaning, used to find similar text.
4. **Storage**: You store these text pieces and their numbers in a searchable place called a **vector index** or vector database. A vector index is a searchable store for text pieces and their numerical embeddings.
5. **Query embedding**: When a user asks a question, the system converts that question into an embedding too.
6. **Similarity search**: The system compares the question numbers with the stored text numbers to find the most relevant pieces.
7. **Prompt augmentation**: The system places the retrieved text pieces into the prompt along with the user's question.
8. **Generation**: The LLM reads the prompt containing the retrieved facts and writes a helpful, accurate answer.

## Let's follow one example
Let us look at a realistic use case. Imagine a college helpdesk bot answering questions from students using the official college rulebook. 

First, let us look at the preparation steps before any question is asked. The college collects the 50-page PDF rulebook. The system cuts this large document into small chunks of two paragraphs each. 

Next, the system converts every single chunk into an embedding. These embeddings are stored safely in a vector index. 

Now, a student comes to the chat window and asks a question. The student types: "What is the fine for returning a library book late?" 

Here is how the query flow works step by step:

1. The system converts the student's question into an embedding.
2. The system searches the vector index for chunks with the most similar embeddings. It finds chunk number 14, which discusses library rules and fines.
3. The system takes chunk 14 and places it into the prompt together with the student's question. An instruction tells the model to use only the provided text.
4. The LLM reads chunk 14, which states that the fine is ten rupees per day. 
5. The LLM generates the final answer: "The fine for returning a library book late is ten rupees per day, according to page 12 of your rulebook."

This process happens in just a few seconds.

## What it cannot do
RAG is very powerful, but it has honest limits that you must remember. 

First, RAG does not guarantee correct answers. If the retrieval step finds the wrong text or misses the correct document entirely, the LLM can still write a wrong answer. 

Second, RAG reduces made-up answers, but it does not remove them completely. The model might still misread the retrieved text. 

Third, RAG does not permanently change or remember your documents inside the model weights. The retrieved text is only part of that one prompt. When a new question arrives, the system must search the documents all over again.

## Quick recap
- A large language model predicts text based on training data, but it has a knowledge cutoff and can hallucinate.
- RAG stands for Retrieval-Augmented Generation.
- Retrieval finds relevant text, augmentation adds it to the prompt, and generation writes the answer.
- Documents are split into chunks, turned into embeddings, and stored in a vector index.
- RAG lets models answer using private or fresh data without retraining.
- Retrieval quality controls the final answer quality, and RAG does not completely eliminate hallucinations.

## Check yourself
1. What does the term LLM stand for?
Answer: Large language model.

2. Why do LLMs sometimes hallucinate?
Answer: They rely on fixed training memory and can generate fluent but false statements when facts are missing.

3. Does RAG retrain or change the model weights?
Answer: No. RAG adds retrieved text to the prompt at question time without changing the model.

4. What is an embedding?
Answer: A list of numbers that capture the meaning of text so similar items can be found easily.

## Key words
- **Large language model**: An artificial intelligence model trained on massive text to predict and generate language.
- **Hallucination**: An event where an artificial intelligence model produces fluent but false statements.
- **RAG**: Retrieval-Augmented Generation, a technique that fetches external facts to help an LLM answer accurately.
- **Embedding**: A list of numbers representing text meaning, used to find similar text.
- **Vector index**: A searchable store for text pieces and their numerical embeddings.

## Learn more
- [What is Retrieval-Augmented Generation (RAG)? | IBM Technology](https://www.youtube.com/watch?v=T-D1OfcDW1M) - IBM Technology, 7-minute video. An IBM scientist explains RAG on a board, with a simple story.
- [What is RAG? - Retrieval-Augmented Generation AI Explained - AWS](https://aws.amazon.com/what-is/retrieval-augmented-generation/) - AWS article, 5-minute read. A short written explanation with the main benefits of RAG.
- [What Is Retrieval-Augmented Generation aka RAG | NVIDIA Blogs](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/) - NVIDIA Blogs article, 6-minute read. Explains RAG with a court-clerk example and real uses.
- [7-Introduction To RAG(Retrieval-Augmented Generation?) In Hindi](https://www.youtube.com/watch?v=DKg6XUnclm8) - Krish Naik Hindi video, 10-minute video. A helpful explanation of RAG in Hindi.
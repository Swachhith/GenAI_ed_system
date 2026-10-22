# Introduction to RAG

## What you will learn
- What a large language model is and why it makes mistakes.
- What the three parts of RAG mean in plain words.
- How preparation, retrieval, augmentation, and generation work together.
- Real limits of RAG and where to use it.

## Before we start: What a large language model is
You will meet the term **LLM**. LLM stands for large language model. You can think of an **LLM** as an artificial intelligence program trained on massive amounts of text to predict and generate human language. 

You might have used chatbots like ChatGPT. They read your questions and write fluent answers. But they have limits. 

First, an **LLM** has a knowledge cutoff. You will meet the term **knowledge cutoff**. A **knowledge cutoff** means the fixed date up to which the model was trained. It does not know private college notes or news from yesterday. 

Second, **LLMs** can sound very confident while stating complete falsehoods. You will meet the term **hallucination**. A **hallucination** means an AI generated statement that sounds true and fluent, but is actually false. 

Imagine a brilliant college senior who read every library book up to the year 2022. If you ask them about yesterday's cricket match, they cannot check live scores. Instead, they might guess wildly and sound completely sure of themselves. That is how an **LLM** works today.

## What is RAG?
You will meet the term **RAG**. **RAG** stands for Retrieval-Augmented Generation. Let us break this long phrase into three simple parts. 

First, **Retrieval**. Retrieval means finding relevant information from an outside source when a user asks a question. 

Second, **Augmented**. Augmented means adding that retrieved information directly to the user prompt. 

Third, **Generation**. Generation means the **LLM** writes the final answer using the added information. 

Think of an open-book exam in your college. You enter the hall with your textbook. You do not memorise every page beforehand. When you read a tough question, you flip to the right page. You read those paragraphs. Then you write your final answer using that page. 

**RAG** brings this exact open-book method to artificial intelligence.

## Why does it matter?
**RAG** solves major problems of standard artificial intelligence. 

First, it lets your system use up-to-date or private information. You can point the system to your company product manual or college rulebook. 

Second, it reduces made-up answers. The model reads real facts instead of relying only on memory. 

Third, answers can point to their sources. The system can show the exact document page it used. 

Fourth, you do not need to retrain the model. You will meet the term **retraining**. Retraining means updating the internal brain of an AI model with new data. With **RAG**, you only update the outside documents. When rulebooks change, you just swap the old text file for a new one.

## How does it work?
Building a **RAG** system happens in two main phases. The first phase prepares the documents. The second phase answers the user question. Here are the steps.

**1. Indexing:** The system collects your documents. It splits large files into small parts. You will meet the term **chunk**. A **chunk** is a small piece of text from a larger document. 

Next, the system turns each **chunk** into a list of numbers that capture meaning. You will meet the term **embedding**. An **embedding** is a list of numbers representing the meaning of a text piece. Finally, it stores these **embeddings** in a database so it can search them fast.

**2. Query:** A user types a question into the system. The system turns this question into an **embedding** too. It compares the question numbers with all stored document numbers. It picks the few most relevant **chunks**.

**3. Augmentation:** The system takes the retrieved text **chunks**. It places them inside the prompt along with the user's original question. It adds a clear instruction. The instruction tells the **LLM** to answer using only the provided text.

**4. Generation:** The **LLM** reads the prompt and the retrieved **chunks**. It writes a clear, helpful answer based on those facts.

## Let's follow one example
Let us look at a college helpdesk bot. Suppose a student asks a private question about fee refund dates. 

**1. Indexing:** The college IT team gathers the official rulebook PDF. They chop the PDF into small **chunks** of text. They turn each **chunk** into an **embedding**, which is a list of numbers. They store these numbers in a vector database. You will meet the term **vector database**. A **vector database** is a special storage system made to search numbers that represent meaning. 

**2. Query:** A student opens WhatsApp and types, "What is the last date to claim a hostel fee refund?" The system turns this question into an **embedding**. It searches the vector database. It finds the exact **chunk** from page 42 about hostel fee refunds.

**3. Augmentation:** The system creates a prompt for the **LLM**. It writes: "Answer the student question using only the text below. Question: What is the last date to claim a hostel fee refund? Context: Page 42 says hostel fee refunds are allowed up to August 15."

**4. Generation:** The **LLM** reads the prompt. It generates the final response: "The last date to claim a hostel fee refund is August 15, according to page 42 of the rulebook."

## What it cannot do
**RAG** is powerful, but it has strict limits. 

First, **RAG** does not completely remove made-up answers. If your retrieval step finds the wrong document, the model might still make mistakes. 

Second, retrieval quality controls everything. If the system fails to find the right **chunk**, the **LLM** gets bad material and writes a poor answer. 

Third, models can only read a limited amount of text at once. You will meet the term **context window**. A **context window** is the maximum amount of text a model can process in one go. Because of this limit, you cannot paste your entire college library into every prompt. You must rely on good retrieval to pick only the best pieces.

## Quick recap
- An **LLM** predicts text but has a fixed knowledge cutoff and can hallucinate.
- **RAG** stands for Retrieval-Augmented Generation, combining search with text creation.
- Preparation involves splitting documents into **chunks** and converting them into **embeddings**.
- When a user asks a question, the system retrieves relevant text **chunks**.
- The system adds those text pieces to the prompt for the **LLM** to read.
- **RAG** reduces made-up answers, updates easily, and points to sources without model retraining.

## Check yourself
1. What does the term **knowledge cutoff** mean for an **LLM**?
Answer: It is the fixed date up to which the model was trained, meaning it lacks newer or private information.

2. What are the three parts of **RAG**?
Answer: Retrieval, Augmentation, and Generation.

3. Why do we split large documents into **chunks** during indexing?
Answer: Because models have a limited context window and work best with small, relevant pieces of text.

4. Does **RAG** retrain the model weights?
Answer: No. It adds retrieved text to the prompt at question time without changing the model itself.

## Key words
- **LLM**: An artificial intelligence program trained on massive text to generate language.
- **Knowledge cutoff**: The fixed date up to which an AI model was trained.
- **Hallucination**: An AI generated statement that sounds true and fluent, but is actually false.
- **RAG**: Retrieval-Augmented Generation, a method that adds retrieved outside knowledge to a prompt.
- **Chunk**: A small piece of text split from a larger document.
- **Embedding**: A list of numbers that capture the meaning of a text piece.
- **Vector database**: A special database designed to search through number lists representing text meaning.
- **Context window**: The maximum amount of text a model can read and process at one time.

## Learn more
- [What is Retrieval-Augmented Generation (RAG)? | IBM Technology](https://www.youtube.com/watch?v=T-D1OfcDW1M) - IBM Technology, 7-minute video. An IBM scientist explains RAG on a board, with a simple story.
- [What is RAG? - Retrieval-Augmented Generation AI Explained - AWS](https://aws.amazon.com/what-is/retrieval-augmented-generation/) - AWS article. A short written explanation with the main benefits of RAG.
- [What Is Retrieval-Augmented Generation aka RAG](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/) - NVIDIA Blogs article. Explains RAG with a court-clerk example and real uses.
- [7-Introduction To RAG(Retrieval-Augmented Generation?) In Hindi](https://www.youtube.com/watch?v=DKg6XUnclm8) - Krish Naik Hindi video [in Hindi], 15-minute video. Explains RAG concepts simply in Hindi.
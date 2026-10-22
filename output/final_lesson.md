# Introduction to RAG

## What you will learn
- What a large language model is and its memory limits.
- The plain meaning of RAG and its three main parts.
- Why RAG helps us get true and useful answers.
- The steps to build and use a RAG system.

## Before we start: Large language models
You have likely typed messages into AI chat tools on your smartphone. These smart computer programs are built using an AI tool. You will meet the term **LLM**. LLM stands for large language model. An LLM is an AI model trained on a very large amount of text to predict and generate language. 

Think of an LLM as a clever student who read many books before entering an exam hall. This student knows a lot of grammar, history, and science. But there is a big problem. The student has a **knowledge cutoff**. You will meet the term knowledge cutoff. A knowledge cutoff means the date after which the model does not know any new events or facts. 

If you ask the LLM about last week's cricket match or your college timetable, it will fail. Worse, LLMs do not like to say "I do not know." They invent smooth lies that sound very real. You will meet the word **hallucination**. Hallucination means when an AI produces fluent but false statements. An LLM's built-in knowledge is fixed at training time. It does not automatically know private or very recent information.

## What is RAG?
You will meet the term **RAG**. RAG stands for Retrieval-Augmented Generation. Let us break down these three words one by one. 

The first word is **Retrieval**. Retrieval means to find relevant information from a safe source. 

The second word is **Augmented**. Augmented means to add extra details to something. 

The third word is **Generation**. Generation means the LLM writes the final answer using those extra details. 

In RAG, relevant information is retrieved from an external knowledge source at the time of the question and added to the model's input. You will meet the word **prompt**. A prompt is the text instruction and question you type into an AI tool. RAG does not change the model's inner weights or retrain it. The knowledge lives in your documents. Updating those documents updates what the system can answer.

## Why does it matter?
Normal LLMs often guess answers when they forget local rules. RAG fixes this problem in many helpful ways. 

First, answers can use up-to-date or private information. Your college helpdesk bot can read the exact PDF notice that was published this morning. 

Second, there are fewer made-up answers. The LLM relies on the facts placed in the prompt instead of guessing blindly. 

Third, answers can point to their sources. You can see the exact page number or paragraph the answer came from. 

Fourth, knowledge can be updated without retraining the model. If a college fee changes, you just swap out the old PDF for the new one. No expensive computer training is needed.

## How does it work?
A RAG system works in clear steps. Think of it like visiting a large college library with a very fast helper. 

**1. Indexing:** The system collects all your documents. It breaks big documents into small pieces. You will meet the word **chunking**. Chunking means splitting large text documents into small pieces so they are easy to search. The system turns each piece into a list of numbers that capture meaning. You will meet the word **embedding**. An embedding is a list of numbers representing text meaning. These numbers are stored in a database so the computer can compare them easily. 

**2. Retrieval:** A user types a question into the system. The system turns the question into an embedding. It searches the database to find the chunks with the most similar meaning. It picks the top few best matches. 

**3. Augmentation:** The system takes the retrieved text chunks and places them directly inside the prompt. It adds the user's question and a clear instruction to use only the provided text. 

**4. Generation:** The LLM reads the prompt containing both the user's question and the retrieved text. It writes a helpful answer based on those real facts.

## Let's follow one example
Imagine you run a college helpdesk in India. Students keep asking about exam fee dates. You want a RAG bot to answer them accurately using the official college rulebook. 

**1. Indexing:** First, you gather the college rulebook PDF. You perform **chunking** by splitting this large book into small paragraphs about fees, attendance, and exams. You convert each small paragraph into an **embedding**, which is a list of numbers representing its meaning. You store these numbers in a vector database so the computer can search them fast. 

**2. Retrieval:** A student types a question: "What is the last date to pay my exam fee?" The system converts this question into numbers. It checks the database and finds the exact paragraph about exam fee dates. 

**3. Augmentation:** The system takes that rulebook paragraph and pastes it into a prompt. It adds the student's question and writes an instruction: "Answer the student using only this rule text." 

**4. Generation:** The LLM reads the rule text and the student's question. It generates the final answer: "The last date to pay your exam fee is Friday, 15th October."

## What it cannot do
RAG is very powerful, but it has strict limits. 

First, RAG does not make an LLM perfect. If the retrieval step finds the wrong information or misses the right document, the final answer can still be wrong. 

Second, RAG reduces made-up answers, but it does not remove them completely. The LLM can still misread the retrieved text. 

Third, models can only read a limited amount of text at once. This limit is called the **context window**. You will meet the context window. The context window is the maximum amount of text an LLM can read and remember in one go. Because of this limit, RAG can only retrieve a few small chunks instead of pasting every book you own.

## Quick recap
- An LLM is a text-predicting AI with a fixed knowledge cutoff and a habit of hallucinating.
- RAG stands for Retrieval-Augmented Generation, bringing external facts to the AI prompt.
- Indexing prepares documents by breaking them into chunks and turning them into embeddings.
- Retrieval finds the most relevant text pieces for a user's question.
- Augmentation places those text pieces into the prompt before the LLM reads them.
- RAG reduces false answers and lets systems use private data without retraining.

## Check yourself
1. What is a knowledge cutoff in an LLM?
Answer: It is the date after which the model does not know any new events or facts.

2. What do the three words in RAG stand for?
Answer: Retrieval, Augmented, and Generation.

3. Does RAG retrain the model weights?
Answer: No, RAG adds text to the prompt at question time without changing the model weights.

4. Can RAG completely remove hallucinations?
Answer: No, it reduces made-up answers, but bad retrieval can still lead to wrong answers.

## Key words
- **LLM**: A large language model trained on huge amounts of text to predict language.
- **Knowledge cutoff**: The date after which an AI model has no built-in knowledge of new events.
- **Hallucination**: When an AI model produces fluent but false statements.
- **RAG**: Retrieval-Augmented Generation, a way to feed external facts into an LLM prompt.
- **Prompt**: The text instruction and question typed into an AI tool.
- **Chunking**: Splitting large text documents into small pieces so they are easy to search.
- **Embedding**: A list of numbers that capture the meaning of a piece of text.
- **Context window**: The maximum amount of text an LLM can read at one time.

## Learn more
- [What is Retrieval-Augmented Generation (RAG)? | IBM Technology](https://www.youtube.com/watch?v=T-D1OfcDW1M) - IBM Technology, 7-minute video. A short video explaining RAG on a board with a simple story.
- [What is RAG? - Retrieval-Augmented Generation AI Explained - AWS](https://aws.amazon.com/what-is/retrieval-augmented-generation/) - AWS article. A short written explanation with the main benefits of RAG.
- [What Is Retrieval-Augmented Generation aka RAG | NVIDIA Blogs](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/) - NVIDIA Blogs article. Explains RAG with a court-clerk example and real uses.
- [7-Introduction To RAG(Retrieval-Augmented Generation?) In Hindi](https://www.youtube.com/watch?v=DKg6XUnclm8) - Krish Naik Hindi video, video. A helpful introduction to RAG explained in Hindi.
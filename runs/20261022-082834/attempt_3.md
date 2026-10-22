# Introduction to RAG (Retrieval-Augmented Generation)

## What you will learn
- What a large language model is and its knowledge limits.
- The plain meaning of RAG and its three main parts.
- How to prepare documents and find relevant text pieces.
- How to build smarter AI answers without changing the model.

## First, what is an LLM?
You may have used ChatGPT to chat or write text. It is a type of AI called a large language model (a computer program that understands human speech). An LLM is an AI model (a computer program designed to think or act like a human) trained (taught using many examples) on a very large amount of text to predict (guess the next word) and generate (produce new text) language.

An LLM reads your message and guesses the next best word. It has read books, articles, and websites to learn how humans talk.

However, an LLM has two big limits. First, its knowledge stops at a certain date. It does not know today's news or your college's secret fee rules.

Second, an LLM can make things up with great confidence. This false reply is called a hallucination (an AI statement that sounds true but is completely false).

## What is RAG?
RAG stands for Retrieval-Augmented Generation. Let us look at what each word means for your AI helper.

First, **retrieval** (the act of finding and bringing back saved information) means finding relevant information from a safe source.

Second, **augmented** means adding that found information to your question.

Third, **generation** (the act of producing new text or answers) means the LLM writes the final answer using that added text.

Think of an open-book exam in your college. You do not try to remember every single rule in your head. You look up the exact page in your textbook, read it, and write the correct answer. RAG gives the AI a textbook to read before answering.

## Why does RAG matter?
An LLM alone often guesses when it does not know the truth. RAG fixes this problem in four major ways.

First, answers can use fresh or private documents.

Second, the AI makes fewer made-up answers because it reads real facts first.

Third, the answer can show the source link or page number so you can check it.

Fourth, you update the knowledge simply by changing the source files. You do not need to retrain or rebuild the model.

## How does RAG work?
Building a RAG system happens in two main parts. First is preparation before anyone asks a question. Second is the live question time.

Here are the numbered steps:

1. **Collect documents**: Gather your text files, PDFs, or college rulebooks in one folder.
2. **Split into chunks**: Break long documents into smaller parts called chunks (small pieces of text).
3. **Turn into numbers**: Convert each chunk into an embedding (a list of numbers that capture meaning). This helps the system compare text mathematically.
4. **Store in an index**: Save these embeddings in a searchable list or vector index (a database [an organized collection of data stored on a computer] that stores number lists for fast searching).
5. **Search**: When you ask a question, the system converts your question into an embedding. Then it searches the database to find the top few most similar chunks.
6. **Add to prompt**: The system places those retrieved (found and brought back from storage) chunks into a prompt (the message or question you type to the AI) along with your original question.
7. **Generate**: The LLM reads the prompt with the text chunks and writes a correct answer.

## Let's follow one example
Let us look at a college helpdesk bot.

Imagine your college has a 50-page rulebook about exam fees and dates. You want to ask when the last date for exam fee payment is.

Step one happens before you type anything. The system collects the 50-page PDF rulebook. It cuts the PDF into small chunks of text. It turns those text chunks into numbers called embeddings and stores them in a database.

Now, step two starts when you type your question: "What is the last date to pay exam fees?"

First, the system turns your question into numbers. It checks the database to find the chunk about exam fee dates. It ignores the chunks about sports or hostel food.

Second, the system takes that one matching chunk and adds it to your prompt. The system prepares the prompt for the AI. The text chunk says: Exam fee last date is 15th July.

Third, the LLM reads this neat package and writes the final answer: "The last date to pay exam fees is 15th July."

The model did not need to know this date beforehand. It read the retrieved text right then.

## What RAG cannot do
RAG is very powerful, but it is not magic.

If the retrieval step finds the wrong text chunk, the LLM will write a wrong answer. The AI can still get confused if the source files have mistakes.

RAG reduces made-up answers, but it does not remove them completely.

## Quick recap
- An LLM predicts words but can miss private facts or hallucinate false answers.
- RAG stands for Retrieval-Augmented Generation.
- Documents are split into chunks and turned into embeddings for easy search.
- The system retrieves matching text and adds it to your prompt.
- The LLM generates an answer using the provided text.

## Check yourself
1. What does the word hallucination mean for an AI?
   Answer: An AI statement that sounds true but is completely false.
2. What are the three parts of RAG?
   Answer: Retrieval, Augmented, and Generation.
3. Why do we split documents into chunks in RAG?
   Answer: To make it easy to find and fit only the most relevant text pieces.
4. Does RAG retrain the LLM model on your private documents?
   Answer: No, RAG only adds retrieved text to the prompt at question time without changing the model.

## Key words
- **LLM**: A large language model trained on massive text to predict and generate language.
- **Hallucination**: An AI statement that sounds true but is completely false.
- **Retrieval**: Finding relevant information from an external source.
- **Augmented**: Adding found information to the user question.
- **Generation**: The writing of the final answer by the LLM.
- **Chunk**: A small piece of a larger document.
- **Embedding**: A list of numbers that capture the meaning of text.
- **Vector index**: A database that stores number lists for fast similarity search.
- **Prompt**: The message you type to the AI.

## Learn more
- [What is Retrieval-Augmented Generation (RAG)? | IBM Technology](https://www.youtube.com/watch?v=T-D1OfcDW1M) - IBM Technology, 7-minute video. A short video. An IBM scientist explains RAG on a board, with a simple story.
- [What is RAG? - Retrieval-Augmented Generation AI Explained - AWS](https://aws.amazon.com/what-is/retrieval-augmented-generation/) - aws.amazon.com article. A short written explanation with the main benefits of RAG.
- [What Is Retrieval-Augmented Generation aka RAG](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/) - NVIDIA Blogs article. Explains RAG with a court-clerk example and real uses.
- [7-Introduction To RAG(Retrieval-Augmented Generation?) In Hindi](https://www.youtube.com/watch?v=DKg6XUnclm8) - Krish Naik Hindi video [in Hindi], 15-minute video. A simple video explanation of RAG in Hindi for easy understanding.
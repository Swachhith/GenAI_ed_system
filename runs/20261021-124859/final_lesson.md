# Introduction to RAG

## What you will learn
- What a large language model is and its limits.
- The plain definition of RAG and its three main parts.
- How RAG works step by step with an Indian college example.
- Why RAG matters for daily AI use.

## First, what is an LLM?
You may have used ChatGPT to write messages or translate text. 
An LLM (large language model, a type of artificial intelligence trained on massive amounts of text to predict and write natural language) powers such tools. 
It reads text and guesses the next best word. 
Think of it like a smart student who read many books before an exam. 
However, this student has three big limits. 
First, its knowledge stops at its training end date, called a knowledge cutoff. 
It does not know what happened today or your college's private rulebook. 
Second, it cannot browse your personal files or your local grocery shop bills. 
Third, when it does not know an answer, it can sound very confident while making things up. 
This false answer is a hallucination (a confident but fake statement made by an AI). 

## What is RAG?
RAG stands for Retrieval-Augmented Generation. 
Let us break down this big term into three simple words. 
First is **retrieval** (finding the right information from a collection of documents). 
Second is **augmented** (adding that found information to your question). 
Third is **generation** (the LLM writing a final, clear answer). 
Imagine you are writing an open-book exam in your college hall. 
You do not know every single rule by heart. 
You look up the exact page in your textbook, read it, and then write your answer on the paper. 
RAG does the exact same thing for an AI. 

## Why does RAG matter?
AI models are expensive to build and train from scratch. 
When your college rules change, you cannot retrain the whole AI model every single day. 
RAG lets you update the knowledge instantly just by changing the text files. 
It helps the AI give correct, up-to-date answers instead of guessing. 
It also helps the AI show its sources so you can check the page number. 
This reduces made-up answers and builds trust in the system.

## How does RAG work?
RAG works in two main phases: preparation and asking. 
Here are the steps in order:
1. **Collection**: You gather all your documents, like your college handbook or hostel forms.
2. **Chunking**: You split these big documents into small pieces called **chunks** (small blocks of text).
3. **Embedding**: You convert each chunk into a list of numbers that capture its meaning. These numbers are called **embeddings** (numbers that represent the meaning of text). 
4. **Storage**: You store these chunks in a searchable list or vector database (a special database made for storing and searching these meaning-numbers).
5. **Retrieval**: When you type a question, the system searches the stored chunks and picks the few most relevant ones.
6. **Augmentation**: The system adds these retrieved chunks to your question in a prompt (the message you type to the AI).
7. **Generation**: The LLM reads your question and the added text, then writes the final answer. 

## Let's follow one example
Let us look at a college helpdesk bot at your local university in India. 
Before any student asks a question, the system prepares the documents. It collects the college library rulebook. It splits it into small chunks like the late fee rule. It stores those chunks in its database. 
Now, you want to know: "What is the fine for returning library books late?"
First, the system looks at your question and turns it into an embedding. 
It searches the college library rulebook stored in its database. 
It finds the exact chunk of text that says: "Late fee is five rupees per day." 
This is the **retrieval** step. 
Next, the system takes your question and adds this text chunk to the prompt. 
This is the **augmentation** step. 
Finally, the LLM reads the rule and writes your answer: "The fine for returning library books late is five rupees per day." 
This is the **generation** step. 
Where does this analogy stop working? 
Unlike a human student, the AI does not truly understand the library rules; it only matches words and numbers very fast.

## What RAG cannot do
RAG is very helpful, but it is not magic. 
If your retrieval step finds the wrong document, the AI will still give a wrong answer. 
RAG reduces made-up answers, but it does not remove them completely. 
Also, the model does not permanently remember your documents after answering. 
It only reads them for that one single question.

## Quick recap
- An LLM predicts text but has a knowledge cutoff and can hallucinate.
- RAG stands for Retrieval-Augmented Generation.
- Documents are split into chunks and turned into embeddings for easy search.
- The system retrieves relevant text and adds it to the prompt.
- The LLM generates an answer using only the provided text.
- RAG reduces false answers but still depends on good search results.

## Check yourself
1. What does the "Retrieval" part of RAG do?
Answer: It finds the relevant information from a collection of documents.

2. Does RAG retrain the LLM when documents change?
Answer: No, RAG does not change the model; it only adds retrieved text to the prompt.

3. What is a chunk?
Answer: A small piece of text made by splitting a large document.

4. Does RAG completely stop hallucinations?
Answer: No, it reduces them, but wrong retrieval can still cause wrong answers.

## Key words
- **LLM**: A large language model trained on text to generate language.
- **Hallucination**: A confident but fake statement made by an AI.
- **RAG**: Retrieval-Augmented Generation, a method to fetch external facts for an AI.
- **Chunk**: A small block of text from a larger document.
- **Embedding**: A list of numbers that capture the meaning of text.
- **Prompt**: The message or instructions you type to the AI.
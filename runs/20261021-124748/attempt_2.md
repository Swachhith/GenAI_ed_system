# Introduction to RAG

## What you will learn
- What a large language model is and its limits.
- What RAG means in simple steps.
- How retrieval, augmentation, and generation work together.
- Why RAG helps us get correct answers from private files.

## First, what is an LLM?
You may have used ChatGPT on your phone. 
It is a type of AI called an **LLM** (Large Language Model). 
An LLM is an AI model trained (taught by reading examples) on a very large amount of text to predict and generate language.
Think of it like a very smart student who read many books before an exam. 
This student knows a lot of general facts about the world. 
However, an LLM has two big limits. 
First, it only knows what was in its training data (the past books and text the AI read to learn) up to a cutoff date (a knowledge cutoff, which is the date after which the AI has no new information in its memory).
It does not know private or very recent information. 
For example, it does not know the exact fee refund rules of your local college announced yesterday. 
Second, it can confidently make things up. 
This false answer is called a **hallucination** (a made-up statement that looks true). 
If the LLM does not know an answer, it tries to guess and sounds very sure of itself. 
We need a way to give the AI fresh and private facts. 
This is where RAG comes in.

## What is RAG?
**RAG** stands for Retrieval-Augmented Generation. 
Do not worry about the big English words. 
Let us break the name into three simple parts.
First, **Retrieval** means to find relevant information from a set of files or documents. 
Second, **Augmented** means to add or attach that information to the user's question. 
Third, **Generation** means the LLM writes the final answer using the attached information. 
Imagine you are writing an open-book exam in your college. 
You do not remember every rule of physics. 
Instead, you look at your textbook to find the correct page. 
Then, you read that page and write the answer on your sheet. 
RAG works in the exact same way for an AI. 

## Why does RAG matter?
Standard LLMs often give old or wrong answers. 
RAG solves this problem in four great ways. 
First, answers can use up-to-date or private information. 
You can give the AI your college rulebook, and it will answer from it. 
Second, there are fewer made-up answers because the AI reads real facts before writing. 
Third, answers can point to their sources, like page numbers or document names. 
Fourth, knowledge can be updated without retraining the model. 
If your college changes a rule, you only update the text file. 
You do not need to train a new AI model from scratch.

## How does RAG work?
RAG works in steps behind the screen. 
Here is how the system handles documents and questions:
1. **Indexing**: The system collects documents. It splits them into small pieces called **chunks** (small parts of a document). 
2. **Embeddings**: Each chunk is turned into an **embedding** (a list of numbers that capture meaning). This helps the computer compare texts by meaning.
3. **Retrieval**: When you type a question, the system searches the stored chunks. It picks the few most relevant ones. 
4. **Augmentation**: The system takes your question and adds the retrieved chunks to a **prompt** (the message you type to the AI).
5. **Generation**: The LLM reads the prompt with the added chunks and writes the final answer for you. 
RAG does not change the model's weights (the internal numbers the AI adjusts to learn from text). 
There is no retraining. 
The knowledge lives in the documents outside the model.

## Let's follow one example
Let us look at a real-life example from an Indian college. 
Suppose your college has a 50-page PDF rulebook about hostel timings. 
You want to know the gate closing time for girls.
1. The college saves the rulebook in the system. The system cuts the 50 pages into small **chunks** of text.
2. You open a chat app on your phone and type: "What is the hostel gate closing time?" This question is your **prompt**.
3. The system turns your question into numbers. It checks which **chunks** in the rulebook match your question. 
4. It finds paragraph 12, which says: "Hostel gates close at 8:30 PM." 
5. The system performs **augmentation**. It sends your question along with paragraph 12 to the LLM.
6. The LLM performs **generation**. It reads the rule and replies: "The hostel gates close at 8:30 PM, according to page 12 of your rulebook." 
Where does this analogy stop working? 
Unlike a human student, the AI does not truly understand the rules. 
It only matches numbers and generates the next best word based on math.

## What RAG cannot do
RAG is very powerful, but it is not magic. 
It has limits you must remember. 
If the retrieval step finds the wrong or missing information, the answer can still be wrong. 
If the rulebook is missing the gate timing, the AI cannot guess it correctly every time. 
Also, RAG reduces made-up answers, but it does not remove them completely. 
Sometimes the LLM can still misunderstand the text and write a false sentence. 
Answer quality depends heavily on retrieval quality. 
If you search for the wrong words, you get the wrong chunks.

## Quick recap
- An LLM is a language AI with a knowledge cutoff that can sometimes hallucinate.
- RAG stands for Retrieval-Augmented Generation.
- Retrieval finds relevant text chunks, augmentation adds them to the prompt, and generation writes the answer.
- Documents are split into chunks and turned into embeddings to make search fast and easy.
- RAG lets AI use private or new documents without retraining the model.
- RAG reduces false answers but does not remove them completely.

## Check yourself
1. What does the "Retrieval" part of RAG do?
   Answer: It finds relevant information from external documents.
2. Does RAG retrain the LLM when documents change?
   Answer: No, the model is not retrained. Only the documents are updated.
3. What is a chunk?
   Answer: A small piece of a document created during the indexing step.
4. Why can an LLM still give a wrong answer with RAG?
   Answer: If retrieval finds the wrong text, the LLM can still make mistakes.

## Key words
- **LLM**: A large language model trained on text to generate language.
- **Hallucination**: A confident but false statement made by an AI.
- **RAG**: Retrieval-Augmented Generation, a method to combine documents with an LLM.
- **Chunk**: A small piece of a document.
- **Embedding**: A list of numbers that capture the meaning of text.
- **Prompt**: The message or question you type to the AI.
# Introduction to RAG (Retrieval-Augmented Generation)

## What you will learn
- What a large language model is and its biggest limits.
- The plain meaning of Retrieval-Augmented Generation.
- How documents are prepared, split, and searched.
- Why RAG helps AI give better and safer answers.

## First, what is an LLM?
A large language model is an AI program trained on a lot of text. You send the AI a prompt. A prompt is the message you type. The model guesses the next words to reply. 

Think of an LLM as a student who read every book in a library up to last year. But this student cannot read new books published today. It also cannot read your personal diary or your college fee receipt. 

An LLM has a training cutoff date. This is the exact time when its learning stopped. It knows nothing about events after that date. 

Sometimes, the model does not know an answer. Instead of staying quiet, it can make up false facts with full confidence. This bad habit is called hallucination. You need a way to feed new and correct facts to your AI.

## What is RAG?
RAG stands for Retrieval-Augmented Generation. It is a smart trick to fix the limits of an LLM. Let us break down the three words one by one. 

Retrieval means finding the exact information you need from a safe folder. Augmented means adding that extra information to your question. Generation means the LLM writes a neat answer using those added facts. 

Imagine you are sitting in a college exam. You forgot some rules from the textbook. The invigilator gives you a photocopy of the exact page you need. You read that page and write the correct answer on your sheet. That is how RAG helps AI.

## Why does RAG matter?
AI models are very smart, but they make mistakes. RAG solves many problems at the same time. 

First, your AI can now answer questions using up-to-date facts. It can read today's news or your fresh office circular. 

Second, it greatly reduces made-up answers from the model. The model reads the real document before writing. 

Third, RAG answers can point directly to their source documents. You can check the exact page the AI used. 

Fourth, you do not need to retrain the whole model when facts change. You only update the documents in your folder.

## How does RAG work?
RAG works in two main parts. The first part prepares your documents. The second part answers your question. Here are the simple steps.

1. **Document collection**: You gather all the text files, PDFs, or manuals you want your AI to read.
2. **Chunking**: You cut those large documents into small pieces called chunks so the AI can read them easily.
3. **Embedding**: You turn each chunk into a list of numbers that capture meaning. These numbers are called embeddings.
4. **Storage**: You store these number lists in a searchable index.
5. **Retrieval**: When you ask a question, the system searches the stored chunks and picks the few most relevant ones.
6. **Augmentation**: The system adds those selected chunks to your prompt along with your original question.
7. **Generation**: The LLM reads your question and the added chunks, then writes the final answer.

## Let's follow one example
Let us look at a college helpdesk bot in India. 

First, the college admin collects the official rulebook PDF. The system splits this PDF into small paragraphs called chunks. It converts each chunk into numbers called embeddings and stores them in a search index. 

Now, student Priya opens her phone. She types a question: "What is the fine for returning a library book late?" 

The system converts Priya's question into an embedding. It searches the index and finds the exact chunk about library fines. This is the retrieval step. 

Next, the system takes that library chunk and adds it to Priya's prompt. This is the augmentation step. 

Finally, the LLM reads the rule chunk. Then the LLM writes the answer. It writes: "The fine for returning a library book late is five rupees per day." This is the generation step. Priya gets the exact right answer without any made-up facts.

## What RAG cannot do
RAG is very powerful, but it has limits. 

If your retrieval step finds the wrong document, the AI will still give a wrong answer. RAG reduces made-up answers, but it does not remove them completely. 

The AI can only read a limited amount of text at one time. This is called the context window limit. You cannot feed whole books all at once. You must rely on good retrieval to pick only the best parts.

## Quick recap
- An LLM predicts text but has a training cutoff date and can hallucinate.
- RAG stands for Retrieval-Augmented Generation.
- Retrieval finds relevant facts from your documents.
- Augmentation adds those facts to your prompt.
- Generation lets the LLM write the final answer.
- RAG needs good documents to give good answers.

## Check yourself
1. What is an LLM's training cutoff?
   Answer: The date when the model stopped learning new information.
2. What does a chunk mean in RAG?
   Answer: A small piece of a larger document.
3. Why do we turn text into embeddings?
   Answer: To get a list of numbers representing meaning so we can search similar text.
4. Does RAG retrain the LLM?
   Answer: No, it only adds retrieved text to the prompt at question time.

## Key words
- **LLM**: A large language model trained on text to generate language.
- **Prompt**: The message or question you send to an AI.
- **Hallucination**: When an AI model confidently makes up false facts.
- **Retrieval**: Finding relevant information from an external knowledge source.
- **Augmented**: Adding extra information to your question before sending it to the AI.
- **Generation**: The process where the LLM writes an answer.
- **Chunk**: A small piece of a larger document.
- **Embedding**: A list of numbers that capture the meaning of a text.

## Learn more
- [What is Retrieval-Augmented Generation (RAG)? | IBM Technology](https://www.youtube.com/watch?v=T-D1OfcDW1M) - IBM Technology, 7-minute video. A short video where an IBM scientist explains RAG on a board with a simple story.
- [What is RAG? - Retrieval-Augmented Generation AI Explained - AWS](https://aws.amazon.com/what-is/retrieval-augmented-generation/) - aws.amazon.com article. A short written explanation with the main benefits of RAG.
- [What is RAG (Retrieval Augmented Generation)? | IBM](https://www.ibm.com/think/topics/retrieval-augmented-generation) - ibm.com article. A longer article for when you want more detail.
- [7-Introduction To RAG(Retrieval-Augmented Generation?) In Hindi](https://www.youtube.com/watch?v=DKg6XUnclm8) - Krish Naik Hindi video [in Hindi], 15-minute video. A helpful explanation in Hindi to clear your basic doubts.
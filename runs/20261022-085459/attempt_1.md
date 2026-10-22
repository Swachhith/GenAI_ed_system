# Introduction to Embeddings

## What you will learn
- What embeddings are and why computers need them.
- How words and sentences change into lists of numbers.
- Why similar ideas sit close together in computer memory.
- How smart search engines use these numbers to find matching items.

## Before we start: Numbers and coordinates
You already know how a map works in real life. Think about finding a specific shop in a busy city like Bengaluru or Mumbai. You use an address with coordinates, like a latitude and a longitude value, to point to its exact spot. 

You will meet the word **vector**. Vector means a list of numbers that act like coordinates on a big map. If two shops sell similar items, their map addresses will be close to each other. This idea of putting things on a map using numbers is the secret key to our lesson today.

## What is Embeddings?
You will meet the word **embeddings**. Embeddings are numerical representations of real-world objects like words, sentences, or images converted into sequences of numbers called vectors. 

Computers cannot read text or look at photos the way you do. They only understand math. Embeddings translate human words and pictures into long lists of numbers. These numbers capture the true meaning of the data. 

## Why does it matter?
Traditional computer codes treat every item as completely unrelated. If you search a standard computer database for the word "puppy", it will never match the word "dog". 

Embeddings solve this big problem. They capture semantic meaning so that similar concepts are placed closer together in a multi-dimensional space. You will meet the word **semantic meaning**. Semantic meaning means the actual sense or concept behind words, rather than just the spelling. 

## How does it work?
Converting words into numbers happens in three simple steps. 

1. Raw data such as words or documents are fed into a trained neural network model. You will meet the word **neural network model**. A neural network model is a computer system inspired by the human brain that learns patterns from data.
2. The model analyzes the contexts in which words or items appear across vast amounts of training data. 
3. The model outputs a dense vector, which is a list of numbers representing coordinates in a high-dimensional space. You will meet the word **dense vector**. A dense vector is a long list of numbers where most spaces contain useful values instead of zeros.

## Let's follow one example
Imagine you run a large online bookstore in India. You want to help customers find books even if they use different words. 

First, you collect all your book descriptions and break them into smaller paragraphs. You save these paragraphs in your system. 

Second, you feed these paragraphs into a neural network model. The model reads the text and checks how words appear next to each other. 

Third, the model turns every paragraph into an embedding. A book about "tasty street food in Delhi" gets numbers like `[0.85, 0.12, 0.44]`. A book about "Mumbai vada pav recipes" gets numbers like `[0.83, 0.15, 0.46]`. 

When a user types "snacks to eat on the street", your system turns that query into numbers. It checks which book coordinates sit closest to the user's query coordinates using distance math. It shows the Delhi food book and the Mumbai food book, even though the words do not match the search box. This is a realistic use case of building a semantic search engine or recommendation system that finds documents or products with similar meanings rather than exact keyword matches.

## What it cannot do
Embeddings are very powerful, but they have clear limits. One major issue is lossy compression where some fine details or exact nuances of the original text can be lost during vector creation. 

Furthermore, embeddings do not hold exact dictionary definitions of words. They only show how words relate to each other based on training examples. If a rare word or local slang was missing from the training data, the model cannot understand it properly.

## Quick recap
- Embeddings turn words, sentences, and images into lists of numbers.
- Computers need these numbers because they cannot understand raw text directly.
- Similar words get numbers that sit close together on a mathematical map.
- A neural network model reads context to create these dense vectors.
- Semantic search engines use these numbers to match meanings instead of exact keywords.
- Some fine details can disappear during this number creation process.

## Check yourself
1. What is an embedding?
   Answer: An embedding is a numerical representation of real-world objects like words or sentences converted into a sequence of numbers.
2. Why do computers need embeddings?
   Answer: Computers need numbers to perform math and logic because they cannot understand raw text directly.
3. How are embeddings created?
   Answer: Raw data is fed into a neural network model that analyzes context and outputs a dense vector.
4. Can embeddings lose details?
   Answer: Yes, fine details or exact nuances of the original text can be lost during vector creation.

## Key words
- **Vector**: A list of numbers that act like coordinates on a map.
- **Embeddings**: Numerical representations of real-world data converted into sequences of numbers.
- **Semantic meaning**: The actual sense or concept behind words, rather than just the spelling.
- **Neural network model**: A computer system inspired by the human brain that learns patterns from data.
- **Dense vector**: A long list of numbers where most spaces contain useful values instead of zeros.

## Learn more
- [What Are Embeddings? Explained Simply for Beginners](https://www.youtube.com/watch?v=JWlkeUFeNPA) - The Data and AI Guy, 11-minute video. A quick introduction to how text becomes numbers.
- [Text Representation Using Word Embeddings: NLP Tutorial For Beginners](https://www.youtube.com/watch?v=Do8cVbx-HOs) - codebasics, 8-minute video. Learn how words map to vectors in simple steps.
- [RAG explained in Hindi under 5 mins](https://www.youtube.com/watch?v=9Ie4FUvtS0w) - Harshita Verma, 6-minute video [in Hindi]. A short explanation of vector search concepts in Hindi.
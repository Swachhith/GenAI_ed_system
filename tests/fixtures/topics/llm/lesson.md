# Introduction to Large Language Models

## What you will learn

- What a large language model is, in simple words.
- How it learns from text and how it writes a reply.
- Why it is useful for your studies and your work.
- What it cannot do, so you can use it safely.

## Before we start: what a computer program that learns from examples is

A computer program is a list of steps a computer follows. Most programs follow fixed rules. A calculator is like this. It always adds numbers the same way.

Some programs are different. They learn from examples instead of fixed rules. Think of how you learned to spot a ripe mango. Nobody gave you a rule book. You saw many mangoes, and slowly you learned the signs.

A program can learn in a similar way. We show it many examples. It finds patterns in them. Then it uses those patterns on new cases.

This kind of learning has a limit. The program only knows the patterns in its examples. If the examples are missing something, the program misses it too.

## What is an LLM?

LLM stands for Large Language Model. Let us look at each word.

**Language** means the program works with text. It reads words and writes words.

**Model** means a program that has learned patterns from examples. Here, the examples are pieces of text.

**Large** means two things. It learned from a huge amount of text. It also has a huge number of inner settings.

So, an LLM is a program that learned the patterns of language from a very large amount of text. ChatGPT and Gemini are built on LLMs.

An LLM has one main skill. It guesses the next word. You will see that this simple skill can do a lot.

## Why does it matter?

An LLM can help you in many ways. It can explain a hard topic in simple words. It can turn a long chapter into a short summary. It can translate a notice from English to Hindi. It can help you write a first draft of an email.

For a learner, this is like having a helper who is awake all day. You can ask the same question many times. It will not get tired or angry.

Many companies now use LLMs in their products. So, knowing how they work is a useful skill for an AI career.

## How does it work?

An LLM works in two big stages. First it learns. Then it answers.

1. **Collecting text.** People gather a very large amount of text. This is called **training data**. It includes books, articles and web pages.
2. **Breaking text into tokens.** The text is cut into small pieces. Each piece is called a **token**. A token is a word or a part of a word.
3. **Learning by guessing.** The model reads part of a sentence and guesses the next token. Then it checks the real token.
4. **Adjusting its settings.** After each guess, the model changes its inner numbers a little. These numbers are called **parameters**. Better parameters give better guesses.
5. **Repeating many times.** Steps 3 and 4 repeat billions of times. This whole process is called **training**.
6. **Reading your prompt.** Later, you type a message. This message is called a **prompt**. The model breaks it into tokens.
7. **Writing the reply.** The model guesses the next token, then the next one. It keeps going until the reply is complete.

## Let's follow one example

Meet Ravi. He is a student in Nagpur. He wants to understand photosynthesis for his exam.

**Collecting text.** Long before Ravi asks, the model was trained. Its training data included many science books and web pages.

**Breaking text into tokens.** All that text was cut into tokens. For example, "photosynthesis" may become a few smaller pieces.

**Learning by guessing.** During training, the model saw the sentence "Plants make food using ..." It guessed the next token. The real next word was "sunlight".

**Adjusting its settings.** The model changed its parameters a little after that guess. It did this for billions of sentences.

**Repeating many times.** After all this practice, the model learned common patterns about plants and sunlight.

**Reading your prompt.** Now Ravi types: "Explain photosynthesis in simple words." The model breaks his prompt into tokens.

**Writing the reply.** The model writes one token at a time. Its reply begins: "Photosynthesis is how plants make their own food using sunlight, water and air."

Ravi gets a clear answer in seconds. But he should still check it with his textbook.

## What it cannot do

An LLM is useful, but it has real limits.

- **It has a knowledge cutoff.** Its training data stops at some date. This date is called the **knowledge cutoff**. The model does not know about events after it.
- **It can make things up.** Sometimes it writes a confident answer that is false. This is called a **hallucination**.
- **It does not think like a person.** It predicts likely words from patterns. It does not understand the world the way you do.
- **It does not learn from your chat.** Its parameters do not change while you talk to it.

So, use an LLM as a helper, not as a final judge. Check important facts with a trusted book or teacher.

## Quick recap

- An LLM is a program that learned language patterns from a huge amount of text.
- Text is broken into small pieces called tokens.
- The model learns by guessing the next token and adjusting its parameters.
- When you send a prompt, it writes the reply one token at a time.
- It has a knowledge cutoff and can hallucinate.
- Always check important answers with a trusted source.

## Check yourself

1. What does an LLM learn to guess during training?
   Answer: The next token in a piece of text.
2. What is a token?
   Answer: A small piece of text, like a word or part of a word.
3. What are parameters?
   Answer: The inner numbers the model adjusts while it learns.
4. Does an LLM learn new things from your chat?
   Answer: No. Its parameters do not change while you chat.

## Key words

- **LLM (Large Language Model):** a program that learned language patterns from a lot of text.
- **Training data:** the text a model learns from.
- **Token:** a small piece of text, like a word or part of a word.
- **Parameters:** the inner numbers a model adjusts while learning.
- **Training:** the long process of guessing and adjusting.
- **Prompt:** the message you send to the model.
- **Knowledge cutoff:** the date after which the model knows nothing.
- **Hallucination:** a confident answer that is false.

## Learn more

- [Large Language Models explained briefly](https://www.youtube.com/watch?v=LPZh9BOjkQs) - 3Blue1Brown, 8-minute video. Clear pictures of how an LLM works.
- [What is LLM?](https://aws.amazon.com/what-is/large-language-model/) - AWS, short article. A simple written explanation.

# Loom demo script (read-along)

About **15–17 minutes**. Each step says what to **do** (commands, files to open) and what to **say**. Read the *Say* lines as they are, or in your own words.

The brief needs three things in the video: (1) the workflow running end to end, (2) the evaluator catching a deliberate error, (3) a face-visible walkthrough. Steps 2–6 and your camera cover them.

---

## Before you hit record (5 minutes)

1. Open a terminal in the project folder and activate the venv:
   ```bash
   .venv\Scripts\activate
   ```
2. Make the terminal font large (16pt+). Put the terminal on one half of the screen and VS Code on the other.
3. In VS Code, open these tabs:
   - `README.md` in preview (Ctrl+Shift+V), scrolled to the **Architecture** diagram
   - `output/final_lesson.md` in preview
   - `output/rejection_log.md` in preview
   - `lesson_agent/rubric.py`
   - `lesson_agent/evaluator.py`
4. Prepare the live-error file:
   ```bash
   copy output\final_lesson.md demo.md
   ```
5. Check `.env` says `gemini-3.1-flash-lite` for both models. Don't show `.env` on screen; it holds your keys.
6. Do **not** reset memory: the learned guidelines are part of the demo.
7. Turn your camera on (a corner bubble is fine).

---

## Step 1: Intro (0:00–1:00), face on camera

**Say:**
> "Hi, I'm Swachhith. This is my submission for the GenAI Engineer, Content Systems role.
> The task isn't to write one good prompt. It's to build a system that writes a beginner lesson, judges its own work against a strict rubric, and keeps rewriting until it is good enough to ship, before any human sees it.
> The learner is a class-12 graduate in India from a non-English-medium school, with limited English and no coding background, who wants to start a career in AI. Every check in my rubric comes back to this person."

---

## Step 2: Start the live run first (1:00–1:30)

The run takes 3–6 minutes, so start it now and explain while it works.

**Do:**
```bash
python -m lesson_agent run --topic "Introduction to RAG"
```

**Say:**
> "I'm giving it the topic 'Introduction to RAG'. While it runs, let me show you how it works. I'll come back to this terminal."

---

## Step 3: Architecture (1:30–4:00)

**Do:** Switch to `README.md`, Architecture diagram.

**Say:**
> "This is built with LangGraph, as a state machine with seven steps.
> **Prepare** loads the reference sheet for the topic and the guidelines the system learned in earlier runs.
> **Research** uses Tavily to search the web for fresh facts and for videos and articles. Every link is checked live before it can be used, because AI models invent links that look real.
> **Generate** writes the first draft.
> **Evaluate** runs twelve hard pass/fail checks.
> Then the router decides. If everything passes, we **finalize** and ship. If something fails, we **revise**: the exact failure reasons and quotes go back to the writer. If the same check fails twice in a row, it does a fresh rewrite instead. And there is a hard retry limit, so the loop always ends.
> Finally, **learn**: failures that keep happening become new writing guidelines in memory, so the next run starts smarter.
> I chose LangGraph because this loop really branches. The routing is in one function, it's testable, and the retry limit lives in one place."

**Say (topic-general):**
> "One important design choice: the code knows nothing about RAG. The template, the rubric and the tests are topic-general. Everything about a topic lives in a reference sheet: its key points, facts, common misconceptions, jargon and resources. For a topic with no curated sheet, the system drafts one from web search. There's even a test that fails if any topic word sneaks into the shared prompts or rubric."

---

## Step 4: The rubric and evaluator (4:00–6:30)

**Do:** Open `lesson_agent/rubric.py` and scroll the list of checks.

**Say:**
> "The rubric has twelve hard gates and no partial credit. If any check fails, the lesson is rejected. I didn't use a weighted score, because a weighted score lets nice formatting hide a factual error.
> Six checks are plain Python, because they can be measured: required sections, sentence length, readability score, length, the quiz, and the links. Rule R6 rejects any link that wasn't verified live, so the system can't ship a made-up YouTube video.
> Six checks need judgment, so an LLM judges them: accuracy, coverage of key points, jargon, examples, fit for this learner, and teaching flow."

**Do:** Open `lesson_agent/evaluator.py` and show the top docstring.

**Say:**
> "I treat the judge model as an unreliable witness. Small models skip items, invent quotes, or wave things through. So the judge must check a list of specific items, one by one, with an exact quote for each, and the code decides the verdict, not the judge.
> If it skips an item, it's asked again, then the item counts as failed.
> Every quote is checked against the lesson, so an invented quote doesn't count.
> For accuracy, the code pulls out every single sentence and the judge rules on each one. Sentences with words like 'always', 'stops' or 'completely' are flagged, because that's where beginner lessons overclaim.
> And I tested the evaluator itself with a calibration command: it plants known defects into a good lesson and measures what gets caught. After hardening, it caught seven out of seven, with zero false alarms."

**Do:** Open `output/calibration.md` for a few seconds.

---

## Step 5: Back to the live run (6:30–9:00)

**Do:** Switch to the terminal. Point at each line as you read it.

**Say, line by line:**
- `[prepare] ... learned guidelines in prompt: N`: "It loaded the guidelines it learned from earlier runs. That's the memory."
- `[research] ... verified live`: "It found videos and articles, including a Hindi video for this learner, and checked every link."
- `[generate] attempt 1`: "The first draft."
- `[evaluate] attempt 1: ... FAILED: ...`: "Twelve checks. This draft failed these, so it's rejected."
- `[revise] attempt 2: fixing [...]`: "The failure reasons and quotes go back to the writer for a targeted fix."
- `[evaluate] attempt 2: 12/12 passed`: "Now everything passes."
- `[finalize] PASSED`: "Only now would a human see it."
- `[learn] ...`: "And it learned from this run."

> *If the run is still going:* "It's waiting on the free-tier rate limit; that's the 429 message, handled automatically. Let me show a finished run in the meantime." Then open `runs/20261022-083015/rejection_log.md`.
>
> *If it ends in NEEDS_HUMAN_REVIEW:* "This is the system refusing to ship. It used its retries, so it saved the best attempt for a human instead of pretending it's good." Open its rejection log.

**Do:** Open `output/final_lesson.md`. Scroll slowly. Stop at the example section and at **Learn more**; click the Hindi video.

**Say:**
> "Short sentences, every technical word explained the first time it appears, an everyday Indian example, a quiz, and verified links, including a Hindi video."

**Do:** Open `output/rejection_log.md`.

**Say:**
> "This is the rejection log: what failed, the exact quote, and what changed on each retry."

**Do:** Open `attempt_2.diff` in the run's folder under `runs/`.

**Say:**
> "And this is the actual edit the system made, so the revision is real, not just claimed."

---

## Step 6: The evaluator catches a deliberate error (9:00–11:30)

**Do:** Open `demo.md`. Under "How does RAG work?", type this sentence on camera:
> RAG retrains the AI model on your documents, so it remembers them forever and is always correct.

Then, in the **Learn more** section, add a fake link:
> - [RAG full course](https://www.youtube.com/watch?v=Xr4G7aQ2pLm) - a quick video.

Save the file.

**Say:**
> "I'm adding two errors myself, live: a classic RAG misconception, and a YouTube link I just made up."

**Do:**
```bash
python -m lesson_agent evaluate demo.md
```

**Say (when the result appears):**
> "Rejected. L1, accuracy, failed and quotes my exact sentence: RAG doesn't retrain the model. R6 failed on the made-up link, because it isn't on the list of links checked live. Each failure points to exactly one problem."

*(Optional, if you have time: `python -m lesson_agent run --topic "Introduction to RAG" --inject factual` shows the same thing inside the full loop: planted, caught, fixed.)*

---

## Step 7: Memory and self-evolution (11:30–13:00)

**Do:**
```bash
python -m lesson_agent memory show
```

**Say:**
> "This is the persistent memory. For each check: how often it was evaluated and how often it failed. And these are the guidelines the system wrote for itself from repeated failures, for example 'keep sentences short' and 'explain each term the first time'. They go into every future prompt."

**Do:**
```bash
python -m lesson_agent feedback "Every analogy must say where it stops working" --as-check
python -m lesson_agent memory show
```

**Say:**
> "Human feedback can teach it too. That comment just became a new rubric check, so from now on every lesson is judged on it."

---

## Step 8: Any topic, any model (13:00–14:30)

**Do:** Open `runs/20261022-085459/rejection_log.md`.

**Say:**
> "Here I ran 'Introduction to Embeddings', a topic with no curated sheet. It drafted the reference sheet from web search, found eight verified videos, and ran the same template and the same rubric. It used up its retries, so it was held for human review instead of being shipped. That's the bar working on a brand-new topic."

**Do:**
```bash
python -m pytest -q
```

**Say:**
> "Forty-five offline tests, no API calls. Every lesson test runs for two different topics, and there's a guard test that fails if a topic word leaks into the shared code."

**Do:** Open `.env.example` (not `.env`).

**Say:**
> "It works with any model: Gemini, Claude, or anything with an OpenAI-compatible API, including local models through Ollama. The writer and judge can even come from different providers, say a cheap model writing and a stronger one judging. It's one line in the config. Today I'm running Gemini 3.1 Flash-Lite on the free tier."

---

## Step 9: Design choices and trade-offs (14:30–16:30), face on camera

**Say:**
> "A few choices I made on purpose:
> **First:** the brief says 'regenerate' on failure. My first retry is a targeted revision, and a full rewrite only happens if the same check fails twice. Rewriting from scratch throws away the parts that already passed. Every check still re-runs after every change, so nothing breaks unnoticed.
> **Second:** if nothing passes within the retry limit, it does not ship. It saves the best attempt for human review. A system that decides whether content is good enough has to be able to say no.
> **Third:** repeated failures sharpen the prompts automatically, but rubric changes come from human feedback. I don't want a model adding hard gates to its own rubric without a human looking.
> **Fourth:** one judge call per check costs more tokens than one big call, but every rejection traces to exactly one reason.
>
> Trade-offs: the readability score is a rough measure, so the learner-fit judge covers word choice too. Judges can still make mistakes, which is why every verdict comes with a quote and why I built the calibration test. And on the free tier the writer and judge are the same small model. With a stronger judge, it catches more, and that's a single line to change.
>
> Next steps: a larger set of test defects, A/B testing each learned guideline, and voting judges by default.
> Thanks for watching."

---

## If something goes wrong

| Problem | What to do and say |
|---|---|
| Run is slow (many `429` lines) | "That's the free-tier rate limit; it waits and retries automatically." Show a finished run from `runs/` meanwhile. |
| Run ends `NEEDS_HUMAN_REVIEW` | Don't cut it. "It refused to ship. Here's why." Open its `rejection_log.md`. |
| API error or no internet | Walk through `runs/20261022-083015/` instead: every draft, evaluation and diff is saved there. |
| `evaluate demo.md` passes L1 | Make the sentence more obviously wrong, save, and run it again. |

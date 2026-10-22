# Loom walkthrough plan

The brief asks for 15–20 minutes. The plan below runs about **16 minutes**. If you need to cut, the segments marked **(core)** add up to about 11 minutes and still cover all three required parts: the end-to-end run, the evaluator catching a deliberate error, and a face-visible walkthrough.

## Before recording

1. `python -m lesson_agent memory reset`, then one warm-up `python -m lesson_agent run`, so memory already holds a real run and at least one learned guideline to show.
2. On the free Gemini tier a run takes a few minutes because of rate-limit waits (`Gemini 429: waiting ...`). Either start the live run early and talk over the waits, or pause the recording during them and say so on camera.
3. Have open: VS Code on the repo, a terminal (venv activated), `README.md` in preview (Mermaid diagram), `output/rejection_log.md` and `output/calibration.md` in preview.
4. Keep your face on camera the whole time, at least as a small bubble.

## Timeline

| Time | Segment | What to show / say |
|---|---|---|
| 0:00–1:00 | **Intro (core)**, face full screen | Who you are. The task in one sentence: not "write a prompt", but a system that decides on its own whether a lesson can ship before a human sees it. The learner: class-12 graduate, non-English-medium school, starting from zero. Every rubric check traces back to this person. |
| 1:00–3:30 | **Architecture (core)** | README Mermaid diagram. Nodes: prepare → generate → evaluate → (revise / regenerate / finalize) → learn. Why LangGraph: the loop has three exits from `evaluate`, so explicit routing beats a hidden while-loop; nodes are testable; one function enforces the retry bound. Point at `graph.py` `route()`. |
| 3:30–6:00 | **Rubric and evaluator design (core)** | `rubric.py`: 11 hard gates, no partial credit, and why not a weighted score (formatting must never outweigh a factual error). Rules vs judges: 5 deterministic checks (`rules.py`) where it can be measured, 6 LLM judges only where judgment is needed. Then `evaluator.py`: itemized verdicts decided in code; the judge treated as an unreliable witness (must answer every item, quotes checked against the lesson, claim-by-claim accuracy, absolute words flagged); fails closed. Grounding: `knowledge/rag.json` (must-cover points, misconceptions). |
| 6:00–8:30 | **End-to-end run (core)** | `python -m lesson_agent run`. Narrate the log: `[prepare]` guidelines loaded → `[generate]` → 11 checks → route decision → revise → re-evaluate → finalize → learn. Open `output/final_lesson.md` and scroll it briefly. Open `output/rejection_log.md`: what failed, the quoted evidence, what changed on each retry. |
| 8:30–11:00 | **Evaluator catches a deliberate error (core)** | `python -m lesson_agent run --inject factual`. Point at the `[inject]` line, the FAIL on L1_ACCURACY with the planted sentence quoted, the targeted revise, then PASS. In the rejection log, show the "caught by" line, the evidence and the change log. |
| 11:00–12:30 | Evaluator catches a *real*, subtle error | `python -m lesson_agent evaluate runs/20261021-125344/final_lesson_copy.md`. This lesson passed the *old* rubric. The hardened rubric rejects it on "stops the AI from making up false answers", an overclaim (RAG only reduces made-up answers). Shows the evaluator improving, not just a staged demo. |
| 12:30–13:30 | Testing the evaluator itself | Show `output/calibration.md` (don't run it live, it takes ~8 minutes). 7 planted defects in a known-good lesson: first calibration 5/7 caught with a false alarm and 8 spillover; after fixes 7/7, 0 false alarms, 2 spillover. Say honestly: the set is small and was tuned on, and you removed example phrases from the judge prompts because they leaked the answers. |
| 13:30–15:00 | Memory and self-evolution | `python -m lesson_agent memory show`: per-check failure stats and learned guidelines (G1–G3). Show `[prepare] learned guidelines in prompt: N` from the earlier run. Live: `python -m lesson_agent feedback "Every analogy must say where it stops working" --as-check`, then `memory show` again to show the new rubric check. |
| 15:00–16:00 | Any model | `.env.example`: Claude, Gemini, or any OpenAI-compatible API (OpenRouter, Groq, Ollama...). `provider:model` lets a cheap model write while a stronger one judges. JSON fallback for models without structured output. Re-run `calibrate` after switching the judge. |
| 16:00–17:30 | **Design choices that differ from the brief, and trade-offs (core)** | See the talking points below. Close on camera: next steps (stronger judge, `JUDGE_VOTES=3`, held-out calibration set, A/B testing learned guidelines). |

## Deviations from the brief: say these out loud

| Brief says | What I built | Why |
|---|---|---|
| "Regenerate on any fail" | First retry is a **targeted revision** of the failed parts; a full regeneration happens only if the same check fails twice in a row | A full rewrite throws away the parts that already passed and often breaks them. Every check re-runs after every retry, so regressions are still caught. Each retry still feeds back the failure reasons. |
| "max 1–2 retries" | Default `MAX_RETRIES=2`; the config allows up to 3 | Matches the brief by default. The extra headroom is for experiments, and the loop is always bounded. |
| "Output the passing lesson" | If nothing passes within the budget, it saves `best_attempt_NEEDS_REVIEW.md` and does **not** ship | A system that decides whether content can ship must be able to say no. |
| "Learn from repeated failures to sharpen prompts/rubrics" | Repeated failures sharpen the **prompts** automatically (learned guidelines). The **rubric** grows from human feedback (`feedback --as-check`) | Letting a model add hard gates to its own rubric unsupervised risks gates that are impossible to pass, or that drift. A human approves rubric changes; prompts can evolve freely. |
| "INPUT: a topic" | `--topic` works and builds a reference sheet for any topic, but the lesson template and some checks are written for RAG | The submission topic is RAG. A topic-general template is the next step. |
| Trade-offs worth naming | One judge call per check (cost vs traceability); Flesch as a rough readability proxy; the same small model writing and judging on the free tier; judges vary from run to run | Each is in the README under Known limitations. |

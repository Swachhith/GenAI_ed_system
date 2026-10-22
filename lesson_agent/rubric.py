"""The rubric: a list of hard pass/fail checks.

Two kinds of check:
  * "rule" - deterministic Python (readability, sentence length, structure, length).
    Cheap, reproducible, impossible to sweet-talk.
  * "llm"  - an LLM judge answers ONE narrow yes/no question and must quote evidence.
    Used only where judgment is unavoidable (accuracy, jargon, examples, flow).

A lesson ships only if every check passes. There is no weighted score to hide behind.
Checks added from human feedback (see learner.py) live in memory and are appended here
at run time, so the rubric itself can grow.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

# Thresholds for the rule checks. Tuned for an ESL reader: plain English sits around
# Flesch 60-70; most Indian state-board English textbooks for class 8-10 land near there.
THRESHOLDS = {
    "avg_sentence_words_max": 15,
    "sentence_words_max": 25,
    "flesch_min": 60,
    "word_count_min": 850,  # generator is asked for 900-1400; small slack for the counter
    "word_count_max": 1800,
    "quiz_questions_min": 3,
}

# H2 headings the generator is told to use; the structure check looks for these keywords.
# Topic-free on purpose: the same template and checks serve any topic.
REQUIRED_SECTIONS = {
    "prerequisite": ["before we start"],
    "what": ["what is", "what are"],
    "why": ["why"],
    "how": ["how does", "how do", "how it works"],
    "example": ["example"],
    "limits": ["cannot", "limit"],
    "recap": ["recap", "summary"],
    "quiz": ["check yourself", "quiz"],
    "glossary": ["key words", "glossary", "new words"],
}


@dataclass(frozen=True)
class Check:
    id: str
    dimension: str
    name: str
    kind: str  # "rule" | "llm"
    criterion: str  # what PASS means, stated so a stranger could apply it
    source: str = "core"  # "core" | "human"

    def to_dict(self) -> dict:
        return asdict(self)


CORE_CHECKS: list[Check] = [
    # ---- deterministic --------------------------------------------------------------
    Check("R1_STRUCTURE", "coherent teaching flow", "Required sections present", "rule",
          "The lesson has an H2 section for each of: the prerequisite idea, what the topic is, why it matters, "
          "how it works, a worked example, limits, recap, a self-check quiz, and key words."),
    Check("R2_SENTENCES", "beginner-friendly language", "Short sentences", "rule",
          f"Average sentence length <= {THRESHOLDS['avg_sentence_words_max']} words AND no sentence "
          f"longer than {THRESHOLDS['sentence_words_max']} words."),
    Check("R3_READABILITY", "beginner-friendly language", "Plain-English readability", "rule",
          f"Flesch Reading Ease >= {THRESHOLDS['flesch_min']} on the lesson prose."),
    Check("R4_LENGTH", "covers the key points", "Right length for one sitting", "rule",
          f"Between {THRESHOLDS['word_count_min']} and {THRESHOLDS['word_count_max']} words "
          "(~10-15 minutes of reading for a slow reader)."),
    Check("R5_QUIZ", "teaches by example", "Self-check with answers", "rule",
          f"The quiz section has at least {THRESHOLDS['quiz_questions_min']} questions and gives the answers."),
    Check("R6_RESOURCES", "teaches by example", "Verified links to learn more", "rule",
          "A 'Learn more' section links 2-4 resources, at least one a video, and EVERY link in the lesson is on "
          "the list verified live during research (no invented or broken URLs)."),
    # ---- LLM judges -----------------------------------------------------------------
    Check("L1_ACCURACY", "accurate & grounded", "No false or misleading claims", "llm",
          "Every technical claim agrees with the reference facts. No listed misconception is stated or "
          "implied as true. Simplifications are allowed only if they do not create a wrong belief "
          "(a misconception from the reference sheet, even softened, is a FAIL)."),
    Check("L2_COVERAGE", "covers the key points", "All must-cover points taught", "llm",
          "Every must-cover point in the reference is actually taught (explained, not just named)."),
    Check("L3_JARGON", "clear, no unexplained jargon", "Every technical term explained", "llm",
          "Every technical or English-uncommon term is explained in simple words at or before its first "
          "use in the body (a glossary at the end alone does not count). Acronyms are expanded on first use."),
    Check("L4_EXAMPLES", "teaches by example", "Concrete analogy and walk-through", "llm",
          "The lesson has (a) at least one everyday analogy a young Indian learner would recognise, "
          "correctly mapped to the topic, AND (b) one concrete worked example that follows a single case "
          "through every step the lesson lists under 'How does it work?', in order, to its result."),
    Check("L5_LEARNER_FIT", "beginner-friendly language", "Fits a non-native English beginner", "llm",
          "Uses common, everyday English words; no idioms, slang, sarcasm or culturally obscure references; "
          "assumes no coding, maths beyond class 12, or prior AI knowledge; tone is encouraging and direct."),
    Check("L6_FLOW", "coherent teaching flow", "Builds step by step", "llm",
          "Ideas are introduced before they are used; sections go from what -> why -> how -> example -> "
          "limits -> recap; each section links to the previous one; nothing is repeated without purpose."),
]


def build_rubric(learned_checks: list[dict]) -> list[Check]:
    extra = [Check(**{**c, "kind": "llm", "source": "human"}) for c in learned_checks]
    return CORE_CHECKS + extra

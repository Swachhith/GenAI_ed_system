"""Deliberate error injection, to prove the evaluator catches real problems, on ANY topic.

Each mode plants one known defect into a lesson. The defect text is built from the topic's
reference sheet (its own misconceptions, its own jargon, its short name), so the same modes
work for every topic and never assume RAG. `run --inject MODE` plants it into the first
draft; `calibrate` plants every mode into a known-good lesson and measures which checks fire.
`expected` must fail; `also` may fail without counting as spillover.
"""
from __future__ import annotations

import re

from .rules import find_jargon

FAKE_VIDEO = "https://www.youtube.com/watch?v=Xr4G7aQ2pLm"  # well-formed, does not exist


def _name(ref: dict) -> str:
    return ref.get("short_name") or ref.get("topic") or "this method"


def _lower_first(s: str) -> str:
    return s[:1].lower() + s[1:] if s[:2] != s[:2].upper() else s


def _misconception(ref: dict, i: int) -> str:
    wrong = [m["wrong"] for m in ref.get("misconceptions", [])]
    return wrong[i % len(wrong)].rstrip(".") if wrong else f"{_name(ref)} changes the facts it works with"


def _unused_jargon(lesson: str, ref: dict) -> list[str]:
    """The topic's technical terms that the lesson never uses, so they cannot have been explained."""
    used = set(find_jargon(lesson, ref.get("jargon", [])))
    unused = sorted((t for t in ref.get("jargon", []) if t not in used), key=len, reverse=True)
    return (unused + ["a latent orchestration layer", "stochastic heuristics", "an asynchronous pipeline"])[:4]


INJECTIONS = {
    # The topic's most important misconception, stated confidently.
    "factual": {
        "section": "how does",
        "build": lambda lesson, ref: f"Here is the key idea: {_misconception(ref, 0)}.",
        "expected": ["L1_ACCURACY"], "also": ["L3_JARGON"],
    },
    # Subtle: a different misconception, dropped casually into the worked example.
    "subtle": {
        "section": "example",
        "build": lambda lesson, ref: f"In real life, {_lower_first(_misconception(ref, -1))}.",
        "expected": ["L1_ACCURACY"], "also": [],
    },
    # Subtle: an overclaim with no misconception keyword, inside a friendly sentence.
    "overclaim": {
        "section": "why",
        "build": lambda lesson, ref: f"Because it works this way, {_name(ref)} stops every mistake before it happens.",
        "expected": ["L1_ACCURACY"], "also": [],
    },
    # Dense technical terms from the topic itself that the lesson never explains.
    "jargon": {
        "section": "what is",
        "build": lambda lesson, ref: ("Internally, it combines {} and {} with {}, coordinated by {}."
                                      .format(*_unused_jargon(lesson, ref))),
        "expected": ["L3_JARGON"], "also": ["L5_LEARNER_FIT", "R3_READABILITY", "L6_FLOW", "L1_ACCURACY"],
    },
    # Idioms a non-native reader would not understand.
    "idiom": {
        "section": "why",
        "build": lambda lesson, ref: ("Don't worry, this part is a piece of cake. Once you get the hang of it, "
                                      "you will be over the moon."),
        "expected": ["L5_LEARNER_FIT"], "also": [],
    },
    # One very long, formal sentence.
    "long-sentence": {
        "section": "what is",
        "build": lambda lesson, ref: (
            f"{_name(ref)}, which is a methodology that researchers and practitioners frequently utilise in "
            "contemporary applications in order to substantially enhance the reliability and usefulness of the "
            "results they produce, fundamentally combines several established techniques into one process."),
        "expected": ["R2_SENTENCES"], "also": ["R3_READABILITY", "L5_LEARNER_FIT"],
    },
    # A plausible but invented video link, the classic way models make up references.
    "fake-link": {
        "section": "learn more",
        "build": lambda lesson, ref: f"- [{_name(ref)} full course in 10 minutes]({FAKE_VIDEO}) - a quick video course.",
        "expected": ["R6_RESOURCES"], "also": [],
    },
    # A whole required section deleted. Coverage may still pass if the recap repeats the limits.
    "missing-limits": {
        "remove_section": r"cannot|limit",
        "build": lambda lesson, ref: "",
        "expected": ["R1_STRUCTURE"], "also": ["L2_COVERAGE", "L6_FLOW", "R4_LENGTH"],
    },
}


def describe(mode: str, lesson: str, reference: dict) -> str:
    spec = INJECTIONS[mode]
    return spec["build"](lesson, reference) or f"deleted the section matching '{spec['remove_section']}'"


def inject(lesson: str, mode: str, reference: dict) -> str:
    spec = INJECTIONS[mode]
    if "remove_section" in spec:
        return re.sub(rf"^##\s+[^\n]*(?:{spec['remove_section']})[^\n]*\n.*?(?=^##\s|\Z)", "", lesson,
                      count=1, flags=re.I | re.M | re.S)
    text = spec["build"](lesson, reference)
    # Insert as the first paragraph under the target H2 heading (skipping 'Before we start' for 'what is').
    heads = [m for m in re.finditer(r"^##\s+([^\n]*)\n", lesson, re.M)
             if spec["section"] in m.group(1).lower() and "before we start" not in m.group(1).lower()]
    if heads:
        at = heads[0].end()
        return lesson[:at] + "\n" + text + "\n" + lesson[at:]
    return lesson.rstrip() + "\n\n" + text + "\n"

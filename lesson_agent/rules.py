"""Deterministic rubric checks. No model calls, so they are free, fast and reproducible."""
from __future__ import annotations

import re

from .rubric import REQUIRED_SECTIONS, THRESHOLDS


def _strip_markdown(md: str) -> str:
    md = re.sub(r"```.*?```", " ", md, flags=re.S)
    md = re.sub(r"`([^`]*)`", r"\1", md)
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", md)
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)
    md = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", md)
    return md


def prose_lines(md: str) -> list[str]:
    """Body text lines: no headings, tables, rules or blank lines; list markers removed."""
    out = []
    for line in _strip_markdown(md).splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "|")) or re.fullmatch(r"[-*_]{3,}", s):
            continue
        s = re.sub(r"^(\d+[.)]|[-*+])\s+", "", s.lstrip(">").strip())
        if s:
            out.append(s)
    return out


def sentences(md: str) -> list[str]:
    result = []
    for line in prose_lines(md):
        # Split on sentence-ending punctuation; each line (list item etc.) is its own boundary.
        for part in re.split(r"(?<=[.!?])\s+(?=[\"'(A-Z0-9])", line):
            if words(part):
                result.append(part.strip())
    return result


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'-]*|\d+", text)


def syllables(word: str) -> int:
    w = word.lower().strip("'")
    if w.isdigit():
        return 1
    # Acronyms (LLM, RAG, AI) are read letter by letter or as one short word.
    if word.isupper() and len(word) <= 4:
        return 1
    w = re.sub(r"[^a-z]", "", w)
    if not w:
        return 1
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def flesch_reading_ease(md: str) -> float:
    sents = sentences(md)
    ws = [w for s in sents for w in words(s)]
    if not sents or not ws:
        return 0.0
    syl = sum(syllables(w) for w in ws)
    return round(206.835 - 1.015 * (len(ws) / len(sents)) - 84.6 * (syl / len(ws)), 1)


def h2_headings(md: str) -> list[str]:
    return [m.group(1).strip().lower() for m in re.finditer(r"^##\s+(.+)$", md, flags=re.M)]


def section_body(md: str, keywords: list[str]) -> str:
    """Text under the first H2 whose heading contains any keyword, up to the next H2."""
    parts = re.split(r"^##\s+", md, flags=re.M)
    for part in parts[1:]:
        heading, _, body = part.partition("\n")
        if any(k in heading.lower() for k in keywords):
            return body
    return ""


# ---- the checks -----------------------------------------------------------------------
# Each returns (passed, evidence, fix_instruction, metrics).

def check_structure(md: str):
    heads = h2_headings(md)
    missing = [name for name, keys in REQUIRED_SECTIONS.items()
               if not any(k in h for h in heads for k in keys)]
    return (not missing,
            [f"Missing section: {m}" for m in missing],
            "Add an H2 section for: " + ", ".join(missing) if missing else "",
            {"h2_headings": heads})


def check_sentences(md: str):
    sents = sentences(md)
    lengths = [len(words(s)) for s in sents]
    avg = round(sum(lengths) / len(lengths), 1) if lengths else 0.0
    cap = THRESHOLDS["sentence_words_max"]
    long_ones = [s for s, n in zip(sents, lengths) if n > cap]
    passed = bool(lengths) and avg <= THRESHOLDS["avg_sentence_words_max"] and not long_ones
    evidence = [f"({len(words(s))} words) {s}" for s in long_ones[:8]]
    if avg > THRESHOLDS["avg_sentence_words_max"]:
        evidence.insert(0, f"Average sentence length is {avg} words (max {THRESHOLDS['avg_sentence_words_max']}).")
    fix = (f"Split every sentence longer than {cap} words into two or three short sentences. "
           "One idea per sentence.") if not passed else ""
    return passed, evidence, fix, {"avg_sentence_words": avg, "sentences": len(lengths), "over_cap": len(long_ones)}


def check_readability(md: str):
    score = flesch_reading_ease(md)
    passed = score >= THRESHOLDS["flesch_min"]
    hard = sorted({w for s in sentences(md) for w in words(s) if syllables(w) >= 4 and not w.isupper()})
    evidence = [] if passed else [f"Flesch Reading Ease = {score} (need >= {THRESHOLDS['flesch_min']})",
                                  "Long words found: " + ", ".join(hard[:25])]
    fix = ("Replace long words with short everyday words (e.g. 'use' not 'utilise', 'find' not 'identify') "
           "and shorten sentences. Keep the necessary technical terms, but explain them.") if not passed else ""
    return passed, evidence, fix, {"flesch": score}


def check_length(md: str):
    n = len(words(_strip_markdown(md)))
    lo, hi = THRESHOLDS["word_count_min"], THRESHOLDS["word_count_max"]
    passed = lo <= n <= hi
    fix = "" if passed else (f"Expand to at least {lo} words by adding explanation and examples."
                             if n < lo else f"Cut to under {hi} words: remove repetition, keep examples.")
    return passed, [] if passed else [f"Word count is {n} (allowed {lo}-{hi})."], fix, {"word_count": n}


def check_quiz(md: str):
    body = section_body(md, REQUIRED_SECTIONS["quiz"])
    q = len(re.findall(r"\?", body))
    has_answers = bool(re.search(r"answer", body, flags=re.I))
    need = THRESHOLDS["quiz_questions_min"]
    passed = q >= need and has_answers
    evidence = [] if passed else [f"Quiz has {q} question(s), answers given: {has_answers} (need >= {need} with answers)."]
    fix = "" if passed else f"Add a 'Check yourself' section with at least {need} short questions, each followed by its answer."
    return passed, evidence, fix, {"quiz_questions": q, "quiz_has_answers": has_answers}


RULES = {
    "R1_STRUCTURE": check_structure,
    "R2_SENTENCES": check_sentences,
    "R3_READABILITY": check_readability,
    "R4_LENGTH": check_length,
    "R5_QUIZ": check_quiz,
}


def _teaching_body(md: str) -> str:
    """Lesson body without the glossary and without the 'What you will learn' preview."""
    body = re.split(r"^##\s+(?:key words|glossary|new words).*$", md, flags=re.M | re.I)[0]
    return re.sub(r"^##\s+what you will learn.*?(?=^##\s)", "", body, flags=re.M | re.I | re.S)


def _stem(term: str) -> str:
    """Regex for a term plus simple inflections: chunk/chunks, hallucinate/hallucination."""
    base = re.escape(re.sub(r"(?:s|es|ion|e)$", "", term.lower()) if len(term) > 5 else term.lower())
    return rf"{base}(?:s|es|e|ed|ing|ion|ions)?"


def _term_re(term: str) -> re.Pattern:
    return re.compile(rf"(?<![a-z]){_stem(term)}(?![a-z])", re.I)


def find_jargon(md: str, jargon: list[str]) -> list[str]:
    """Technical terms that actually occur in the teaching body."""
    body = _teaching_body(md)
    return [t for t in jargon if _term_re(t).search(body)]


def _explains(term: str, sentence: str) -> bool:
    """Does this sentence explain `term`? Cues must attach to the term itself:
    "chunk (a small piece...)", "called a chunk", "a chunk is a...", "Chunk: a small...".
    """
    t = _stem(term)
    cues = [
        rf"{t}\)?\s*\(",                                              # term (meaning)
        rf"\bcalled\s+(?:\w+\s+){{0,2}}{t}",                          # ... called (a/model) term
        rf"{t}\)?\s+(?:means|is an?|is the|are|refers to|stands for)\b",  # term is a ...
        rf"^{t}\s*[:—-]\s",                                           # Term: meaning
    ]
    return any(re.search(c, sentence, re.I) for c in cues)


def undefined_at_first_use(md: str, terms: list[str]) -> list[tuple[str, str]]:
    """(term, sentence) pairs where the sentence that first uses the term has no definition cue.

    A cheap pre-screen, not a verdict: it hands the judge concrete suspects, which keeps a
    lenient judge from waving terms through without looking.
    """
    sents = sentences(_teaching_body(md))
    suspects = []
    for t in terms:
        idx = next((i for i, s in enumerate(sents) if _term_re(t).search(s)), None)
        # Look at the first-use sentence and the next few ("RAG stands for ... Retrieval means ...").
        if idx is not None and not any(_explains(t, s) for s in sents[idx:idx + 5]):
            suspects.append((t, sents[idx]))
    return suspects


# ---- evidence helpers for the LLM judges ------------------------------------------------
# These never decide a verdict on their own. They (a) hand the judge concrete suspects so a
# lenient model can't skim, and (b) check the judge's quotes, so it can't invent evidence.

def _norm_words(text: str) -> list[str]:
    text = _strip_markdown(text).lower().replace("’", "'").replace("‘", "'")
    return [w.strip("'") for w in re.findall(r"[a-z0-9']+", text) if w.strip("'")]


def grounded(quote: str, md: str, min_ratio: float = 0.8) -> bool:
    """Is `quote` really in the lesson? Tolerates markdown, punctuation, case and '...' elisions.

    Each elided fragment must appear in one place, with >= min_ratio of its words in order
    (so one changed word or a dropped comma doesn't reject a real quote).
    """
    from difflib import SequenceMatcher

    lesson = _norm_words(md)
    frags = [f for f in re.split(r"\.\.\.|…", quote) if _norm_words(f)]
    if not frags:
        return False
    for frag in frags:
        q = _norm_words(frag)
        anchor = SequenceMatcher(None, lesson, q, autojunk=False).find_longest_match(0, len(lesson), 0, len(q))
        start = max(0, anchor.a - anchor.b)
        window = lesson[start:start + len(q) + 5]
        matched = sum(b.size for b in SequenceMatcher(None, window, q, autojunk=False).get_matching_blocks())
        if matched < max(1, round(min_ratio * len(q))):
            return False
    return True


# Absolute wording is where beginner lessons most often overclaim ("RAG stops hallucinations").
ABSOLUTE_RE = re.compile(
    r"\b(always|never|every time|guarantee[sd]?|100 ?%|complete(?:ly)?|entirely|totally|perfect(?:ly)?|"
    r"forever|permanent(?:ly)?|eliminat\w*|stops?|prevents?|impossible|cannot be wrong|no mistakes?|"
    r"all the time|any question|everything|nothing)\b", re.I)

_CLAIM_HINT = re.compile(
    r"\b(rag|ai|llm|models?|chatgpt|retriev\w*|search\w*|documents?|chunks?|embedd\w*|vectors?|prompts?|"
    r"answers?|hallucinat\w*|train\w*|learn\w*|remember\w*|forget\w*|knows?|memory|database|index\w*|"
    r"generat\w*|augment\w*|facts?|information|sources?)\b", re.I)


def technical_claims(md: str, limit: int = 120) -> list[tuple[str, bool]]:
    """(sentence, uses_absolute_wording) for every sentence that states something about the topic.

    Covers the whole lesson except headings, the glossary-free quiz questions themselves, and
    pure instructions. Deterministic, so the accuracy judge verifies claim by claim and cannot
    skip a sentence. Absolute-wording claims are kept first if the list must be cut.
    """
    seen, out = set(), []
    for s in sentences(md):
        if s.endswith("?") or s in seen or not _CLAIM_HINT.search(s) or len(words(s)) < 4:
            continue
        seen.add(s)
        out.append((s, bool(ABSOLUTE_RE.search(s))))
    if len(out) > limit:
        flagged = [c for c in out if c[1]]
        out = flagged + [c for c in out if not c[1]][:max(0, limit - len(flagged))]
    return out


def repeated_definitions(md: str, terms: list[str], max_times: int = 3) -> list[tuple[str, int]]:
    """Terms explained more than `max_times` in the body: over-glossing reads as padding.

    Variants of one word (chunk / chunks) are reported once. Defining a key term in the
    explanation, the steps and the example (3 times) is normal teaching, so 4+ is flagged.
    """
    sents = sentences(_teaching_body(md))
    out, seen = [], set()
    for t in terms:
        if _stem(t) in seen:
            continue
        seen.add(_stem(t))
        n = sum(_explains(t, s) for s in sents)
        if n > max_times:
            out.append((t, n))
    return out

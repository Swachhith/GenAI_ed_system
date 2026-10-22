"""Structured-output schemas for every model call that must return data, not prose."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ItemCheck(BaseModel):
    item: str = Field(description="The requirement item being verified, copied from the list.")
    met: bool
    quote: str = Field(description="Exact quote from the lesson that shows the item is met, or that shows the problem. Empty only if the thing is absent.")


class JudgeVerdict(BaseModel):
    items: list[ItemCheck] = Field(default_factory=list, description="One entry per item in ITEMS TO VERIFY, in order.")
    reasoning: str = Field(description="2-4 sentences: what you checked and what you found.")
    verdict: Literal["PASS", "FAIL"]
    evidence: list[str] = Field(description="FAIL: exact quotes from the lesson, or names of missing items. PASS: may be empty.")
    fix: str = Field(description="FAIL: a specific, actionable fix. PASS: empty string.")


class ChangeLogEntry(BaseModel):
    check_id: str
    change: str = Field(description="What you changed to fix this check, in one sentence.")


class Revision(BaseModel):
    lesson_markdown: str = Field(description="The full revised lesson in Markdown.")
    change_log: list[ChangeLogEntry]


class GuidelineDecision(BaseModel):
    action: Literal["new", "duplicate"]
    duplicate_of: str = Field(description="Existing guideline id if action is 'duplicate', else empty.")
    guideline: str = Field(description="The new guideline if action is 'new', else empty.")


class NewCheck(BaseModel):
    name: str = Field(description="Short name, under 8 words.")
    dimension: str = Field(description="Rubric dimension, e.g. 'beginner-friendly language'.")
    criterion: str = Field(description="What PASS means, objectively.")


class MustCover(BaseModel):
    id: str
    point: str


class Misconception(BaseModel):
    wrong: str
    right: str


class ReferenceSheet(BaseModel):
    must_cover: list[MustCover]
    facts: list[str]
    misconceptions: list[Misconception]
    jargon: list[str]

"""
Pydantic schemas for the MarketLab REST API.

These are *presentation-layer* objects: they define the JSON contract
between frontend and backend.  They intentionally duplicate some
domain types to keep the domain layer framework-free.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field




class FieldOut(BaseModel):
    name: str
    type: str
    description: str


class TaskShort(BaseModel):
    """Compact representation for the task catalogue list."""
    id: str
    title: str
    topic: str


class TaskDetail(BaseModel):
    """Full task information shown on the solve page."""
    id: str
    title: str
    topic: str
    input_fields: list[FieldOut]
    output_fields: list[FieldOut]
    public_test: dict  # first generated test — always visible



class SubmissionIn(BaseModel):
    task_id: str
    user_code: str = Field(..., min_length=1, max_length=50_000)


class SubmissionOut(BaseModel):
    id: str | None = None
    verdict: str
    passed: int
    total: int
    message: str = ""
    failed_test_index: int | None = None
    failed_field: str | None = None
    created_at: datetime | None = None


class SubmissionShort(BaseModel):
    """Compact submission for history list."""
    id: str
    task_id: str
    verdict: str
    passed: int
    total: int
    created_at: datetime



from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class FieldOut(BaseModel):
    name: str
    type: str
    description: str


class TaskShort(BaseModel):
    id: str
    title: str
    topic: str


class TaskDetail(BaseModel):
    id: str
    title: str
    topic: str
    input_fields: list[FieldOut]
    output_fields: list[FieldOut]
    public_test: dict



class SubmissionIn(BaseModel):
    task_id: str
    user_code: str = Field(..., min_length=1, max_length=50_000)


class SubmissionOut(BaseModel):
    id: str = ""
    verdict: str
    passed: int
    total: int
    message: str = ""
    failed_test_index: int | None = None
    failed_field: str | None = None
    failed_input: dict[str, Any] | None = None
    failed_expected: dict[str, float] | None = None
    failed_got: dict[str, float] | None = None
    created_at: str = ""


class SubmissionShort(BaseModel):
    id: str
    task_id: str
    verdict: str
    passed: int
    total: int
    created_at: str = ""

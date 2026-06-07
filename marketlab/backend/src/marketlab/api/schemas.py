"""
Данный блок кода необходим для валидации входящего json-файла и сериализации ответа, 
используются pydantic модели
"""


from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field


class FieldOut(BaseModel):
    name: str
    type: str
    description: str


class UserOut(BaseModel):
    user_id: str
    email: str


class TaskShort(BaseModel):
    id: str
    title: str
    topic: str
    difficulty: int = 1


class TaskDetail(BaseModel):
    id: str
    title: str
    topic: str
    input_fields: list[FieldOut]
    output_fields: list[FieldOut]
    public_test: dict
    public_test_output: dict = {}


class SubmissionIn(BaseModel):
    task_id: str
    user_code: str = Field(..., min_length=1, max_length=50_000)


class SubmissionOut(BaseModel):
    id: str
    verdict: str
    passed: int
    total: int
    message: str = ""
    failed_test_index: int | None = None
    failed_field: str | None = None
    failed_input: dict[str, Any] | None = None
    failed_expected: dict[str, Any] | None = None
    failed_got: dict[str, Any] | None = None
    created_at: str
    saved: bool = False  


class SubmissionShort(BaseModel):
    id: str
    task_id: str
    verdict: str
    passed: int
    total: int
    created_at: str

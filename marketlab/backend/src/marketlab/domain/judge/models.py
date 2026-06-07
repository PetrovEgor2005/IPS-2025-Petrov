from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Literal
"""
Такие ответы будут получаться после проверки в тестирующем модуле, AC - Accepted, 
WA - Wrong Answer, RE - Runtime Error, TLE - Time Limit
Необходимо для того, чтобы фронту возвращать ответ, который в дальнейшем будет отображаться пользователю
""" 
Verdict = Literal["AC", "WA", "RE", "TLE"]
@dataclass(frozen=True, slots=True)
class JudgeReport:
    verdict: Verdict
    passed: int
    total: int
    message: str = ""
    failed_test_index: int | None = None
    failed_field: str | None = None
    failed_input: dict[str, Any] | None = None
    failed_expected: dict[str, Any] | None = None
    failed_got: dict[str, Any] | None = None

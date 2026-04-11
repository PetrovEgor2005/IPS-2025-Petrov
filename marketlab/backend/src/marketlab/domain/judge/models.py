from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

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
    failed_expected: dict[str, float] | None = None
    failed_got: dict[str, float] | None = None

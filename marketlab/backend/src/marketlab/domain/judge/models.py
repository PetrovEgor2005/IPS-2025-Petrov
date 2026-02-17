from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Verdict = Literal["AC", "WA", "RE", "TLE"]


@dataclass(frozen=True, slots=True)
class JudgeReport:
    verdict: Verdict
    passed: int
    total: int
    message: str = ""
    failed_test_index: int | None = None
    failed_field: str | None = None

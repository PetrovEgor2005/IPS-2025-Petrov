from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from marketlab.domain.judge.models import JudgeReport
from marketlab.usecases.judge_v1 import JudgeSettings, run_judge_v1
from marketlab.usecases.registry import TASK_REGISTRY


@dataclass(frozen=True, slots=True)
class SubmitSolutionInput:
    task_id: str
    user_code: str
    tests: list[dict[str, Any]]


def submit_solution(inp: SubmitSolutionInput, settings: JudgeSettings = JudgeSettings()) -> JudgeReport:
    spec, oracle = TASK_REGISTRY[inp.task_id]
    return run_judge_v1(
        spec=spec,
        oracle=oracle,  # callable(params)->Result
        user_code=inp.user_code,
        tests=inp.tests,
        settings=settings,
    )

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from marketlab.domain.judge.models import JudgeReport
from marketlab.domain.tasks import Result, TaskSpec
from marketlab.infra.judge.runner_inprocess import TimeoutError, compile_user_solve, time_limit


@dataclass(frozen=True, slots=True)
class JudgeSettings:
    time_limit_sec: int = 1
    abs_tol: float = 1e-6
    rel_tol: float = 1e-6


def _validate_result(spec: TaskSpec, user_result: Any) -> Result | None:
    if not isinstance(user_result, dict):
        return None

    expected_keys = {f.name for f in spec.output_fields}
    got_keys = set(user_result.keys())
    if got_keys != expected_keys:
        return None

    casted: dict[str, float] = {}
    for key in expected_keys:
        val = user_result[key]
        if not isinstance(val, (int, float)):
            return None
        casted[key] = float(val)

    return casted


def _close_enough(a: float, b: float, abs_tol: float, rel_tol: float) -> bool:
    diff = abs(a - b)
    if diff <= abs_tol:
        return True
    denom = max(1.0, abs(b))
    return diff / denom <= rel_tol


def run_judge_v1(
    *,
    spec: TaskSpec,
    oracle,
    user_code: str,
    tests: list[dict[str, Any]],
    settings: JudgeSettings = JudgeSettings(),
) -> JudgeReport:
    try:
        with time_limit(settings.time_limit_sec):
            solve = compile_user_solve(user_code)
    except TimeoutError:
        return JudgeReport(verdict="TLE", passed=0, total=len(tests), message="TLE during compilation")
    except Exception as e:
        return JudgeReport(verdict="RE", passed=0, total=len(tests), message=f"Compile error: {e}")

    passed = 0
    total = len(tests)
    first_failed_index = None
    first_failed_field = None
    first_fail_message = ""
    first_failed_input = None
    first_failed_expected = None
    first_failed_got = None

    for i, params in enumerate(tests):
        try:
            with time_limit(settings.time_limit_sec):
                user_out_raw = solve(params)
        except TimeoutError:
            return JudgeReport(
                verdict="TLE", passed=passed, total=total,
                message="TLE", failed_test_index=i,
                failed_input=params,
            )
        except Exception as e:
            if first_failed_index is None:
                first_failed_index = i
                first_fail_message = f"Runtime error: {e}"
                first_failed_input = params
            continue

        user_out = _validate_result(spec, user_out_raw)
        if user_out is None:
            if first_failed_index is None:
                first_failed_index = i
                first_fail_message = "Wrong output format/keys"
                first_failed_input = params
            continue

        expected = oracle(params)

        field_ok = True
        for field, exp_val in expected.items():
            got_val = user_out[field]
            if not _close_enough(got_val, exp_val, settings.abs_tol, settings.rel_tol):
                field_ok = False
                if first_failed_index is None:
                    first_failed_index = i
                    first_failed_field = field
                    first_fail_message = "Wrong answer"
                    first_failed_input = params
                    first_failed_expected = expected
                    first_failed_got = user_out
                break

        if field_ok:
            passed += 1

    if passed == total:
        return JudgeReport(verdict="AC", passed=passed, total=total, message="Accepted")

    return JudgeReport(
        verdict="WA",
        passed=passed,
        total=total,
        message=first_fail_message,
        failed_test_index=first_failed_index,
        failed_field=first_failed_field,
        failed_input=first_failed_input,
        failed_expected=first_failed_expected,
        failed_got=first_failed_got,
    )

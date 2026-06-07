"""
В данном блоке кода происходит сравнение пользовательского решения по тестам, проходимся по тестам, 
сравниваем с результатами из из солвера, делаем формирование отчёта для пользователя
"""


from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from marketlab.domain.judge.models import JudgeReport
from marketlab.domain.tasks import Result, TaskSpec
from marketlab.infra.judge.runner_inprocess import run_tests_subprocess


@dataclass(frozen=True, slots=True)
class JudgeSettings:
    time_limit_sec: int = 1
    abs_tol: float = 1e-6
    rel_tol: float = 1e-6

#в данной функции происходит проверка кода, что он содержит те поля, которые были заложены в задаче
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
        #исключаем случай передачи неправильных типов, которые с точки зрение питона сравнимы
        if isinstance(val, bool) or not isinstance(val, (int, float)):
            return None
        casted[key] = float(val)

    return casted

#сравнение чисел по точности 
def _close_enough(a: float, b: float, abs_tol: float, rel_tol: float) -> bool:
    diff = abs(a - b)
    if diff <= abs_tol:
        return True
    denom = max(abs(a), abs(b), 1.0)
    return diff / denom <= rel_tol


def run_judge_v1(
    *,
    spec: TaskSpec,
    oracle,
    user_code: str,
    tests: list[dict[str, Any]],
    settings: JudgeSettings = JudgeSettings(),
) -> JudgeReport:
    total = len(tests)
    #запускаем пользовательский код в раннере 
    run = run_tests_subprocess(user_code, tests, settings.time_limit_sec)
    #получаем от него результат 
    status = run.get("status")
    per_test_results: list[dict[str, Any]] = run.get("results", [])
    #переупаковываем в вывод, который пойдёт для пользователя(случай, когда до прогона тестов дело не дошло)
    if status == "compile_error":
        return JudgeReport(
            verdict="RE",
            passed=0,
            total=total,
            message=f"Compile error: {run.get('message', '')}",
        )
    if status == "tle" and not per_test_results:
        return JudgeReport(
            verdict="TLE",
            passed=0,
            total=total,
            message="Time limit exceeded (global)",
        )
    if status == "crashed":
        return JudgeReport(
            verdict="RE",
            passed=0,
            total=total,
            message=run.get("message", "Worker process crashed"),
        )

    passed = 0
    first_failed_index: int | None = None
    first_failed_field: str | None = None
    first_fail_message = ""
    first_failed_input: dict[str, Any] | None = None
    first_failed_expected: dict[str, Any] | None = None
    first_failed_got: dict[str, Any] | None = None
    had_runtime_error = False
    had_tle = False
    #запускаем основную волну проверок кода через тесты
    for i, params in enumerate(tests):
        if i >= len(per_test_results):
            break
        r = per_test_results[i]
        r_status = r.get("status")

        if r_status == "tle":
            had_tle = True
            if first_failed_index is None:
                first_failed_index = i
                first_fail_message = "Time limit exceeded"
                first_failed_input = params
            break

        if r_status == "runtime_error":
            had_runtime_error = True
            if first_failed_index is None:
                first_failed_index = i
                first_fail_message = f"Runtime error: {r.get('message', '')}"
                first_failed_input = params
            continue

        user_out = _validate_result(spec, r.get("result"))
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
    #формирование результата для фронтэнда
    if passed == total:
        return JudgeReport(verdict="AC", passed=passed, total=total, message="Accepted")
    #важность приоритета вердиктов
    if had_tle:
        verdict = "TLE"
    elif had_runtime_error and first_fail_message.startswith("Runtime error"):
        verdict = "RE"
    else:
        verdict = "WA"

    return JudgeReport(
        verdict=verdict,
        passed=passed,
        total=total,
        message=first_fail_message,
        failed_test_index=first_failed_index,
        failed_field=first_failed_field,
        failed_input=first_failed_input,
        failed_expected=first_failed_expected,
        failed_got=first_failed_got,
    )

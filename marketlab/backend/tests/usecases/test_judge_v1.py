import pytest

from marketlab.usecases.submit_solution import SubmitSolutionInput, submit_solution


GOOD_CODE = """
def solve(params: dict) -> dict:
    a = float(params["a"]); b = float(params["b"])
    c = float(params["c"]); d = float(params["d"])
    mode = params["mode"]
    t = float(params.get("t", 0.0))

    # Producer price depends on policy wedge
    # Equilibrium: a - bP = c + d*(P - t) for tax, c + d*(P + t) for subsidy
    denom = b + d
    if mode == "none":
        p = (a - c) / denom
    elif mode == "tax":
        p = (a - c + d * t) / denom
    else:  # subsidy
        p = (a - c - d * t) / denom

    q = a - b * p
    return {"p_eq": p, "q_eq": q}
"""

BAD_IGNORES_MODE = """
def solve(params: dict) -> dict:
    a = float(params["a"]); b = float(params["b"])
    c = float(params["c"]); d = float(params["d"])
    # ignores mode and t
    p = (a - c) / (b + d)
    q = a - b * p
    return {"p_eq": p, "q_eq": q}
"""

BAD_KEYS = """
def solve(params: dict) -> dict:
    return {"price": 1.0, "qty": 2.0}
"""

RUNTIME_ERROR = """
def solve(params: dict) -> dict:
    return 1 / 0
"""

TLE_CODE = """
def solve(params: dict) -> dict:
    while True:
        pass
"""


def make_tests_pack():
    return [
        {"a": 120, "b": 3, "c": -10, "d": 2, "mode": "none"},
        {"a": 120, "b": 3, "c": -10, "d": 2, "mode": "tax", "t": 10},
        {"a": 120, "b": 3, "c": -10, "d": 2, "mode": "subsidy", "t": 10},
    ]



def test_judge_accepts_good_solution():
    report = submit_solution(
        SubmitSolutionInput(
            task_id="equilibrium_linear_v1",
            user_code=GOOD_CODE,
            tests=make_tests_pack(),
        )
    )
    assert report.verdict == "AC"
    assert report.passed == report.total


def test_judge_wrong_answer_if_mode_ignored():
    report = submit_solution(
        SubmitSolutionInput(
            task_id="equilibrium_linear_v1",
            user_code=BAD_IGNORES_MODE,
            tests=make_tests_pack(),
        )
    )
    assert report.verdict == "WA"
    assert report.failed_test_index is not None


def test_judge_wrong_format_if_keys_wrong():
    report = submit_solution(
        SubmitSolutionInput(
            task_id="equilibrium_linear_v1",
            user_code=BAD_KEYS,
            tests=make_tests_pack(),
        )
    )
    assert report.verdict == "WA"
    assert report.message.lower().startswith("wrong output")


def test_judge_runtime_error():
    report = submit_solution(
        SubmitSolutionInput(
            task_id="equilibrium_linear_v1",
            user_code=RUNTIME_ERROR,
            tests=make_tests_pack(),
        )
    )
    assert report.verdict == "RE"


def test_judge_timeout():
    report = submit_solution(
        SubmitSolutionInput(
            task_id="equilibrium_linear_v1",
            user_code=TLE_CODE,
            tests=make_tests_pack()
        )
    )
    assert report.verdict == "TLE"

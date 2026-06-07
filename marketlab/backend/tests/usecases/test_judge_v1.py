from marketlab.usecases.submit_solution import SubmitSolutionInput, submit_solution

GOOD_CODE = """
def solve(params: dict) -> dict:
    a = float(params["a"]); b = float(params["b"])
    c = float(params["c"]); d = float(params["d"])
    mode = params["mode"]
    t = float(params.get("t", 0.0))

    # цена продавца зависит от налогового клина
    # равновесие: a - bP = c + d*(P - t) при налоге, c + d*(P + t) при субсидии
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
    # игнорирует mode и t — должен завалиться на тестах с налогом/субсидией
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
            task_id="equilibrium_linear_v1", user_code=TLE_CODE, tests=make_tests_pack()
        )
    )
    assert report.verdict == "TLE"


SANDBOXED_IMPORT = """
def solve(params):
    import os
    return {"p_eq": 0.0, "q_eq": 0.0}
"""


def test_sandbox_blocks_imports():
    """User code is run with a restricted builtins map; `import` must fail at runtime."""
    report = submit_solution(
        SubmitSolutionInput(
            task_id="equilibrium_linear_v1",
            user_code=SANDBOXED_IMPORT,
            tests=make_tests_pack(),
        )
    )
    # __import__ нет в SAFE_BUILTINS → код упадёт с NameError на этапе исполнения
    assert report.verdict == "RE"


SANDBOXED_ROUND = """
def solve(params):
    a = float(params["a"]); b = float(params["b"])
    c = float(params["c"]); d = float(params["d"])
    mode = params["mode"]; t = float(params.get("t", 0.0))
    denom = b + d
    if mode == "none":
        p = (a - c) / denom
    elif mode == "tax":
        p = (a - c + d * t) / denom
    else:
        p = (a - c - d * t) / denom
    return {"p_eq": round(p, 6), "q_eq": round(a - b * p, 6)}
"""


def test_sandbox_allows_round():
    """`round` must be available in the sandbox — solvers and students rely on it."""
    report = submit_solution(
        SubmitSolutionInput(
            task_id="equilibrium_linear_v1",
            user_code=SANDBOXED_ROUND,
            tests=make_tests_pack(),
        )
    )
    assert report.verdict == "AC"

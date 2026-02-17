from __future__ import annotations

import signal
from contextlib import contextmanager
from types import MappingProxyType
from typing import Any, Callable

from marketlab.domain.judge.models import JudgeReport, Verdict


class TimeoutError(Exception):
    pass


@contextmanager
def time_limit(seconds: int):
    """
    Simple timeout using signal.alarm (works on Unix/macOS).
    Later we will replace with subprocess/multiprocessing sandbox.
    """
    if seconds <= 0:
        yield
        return

    def handler(signum, frame):  # noqa: ARG001
        raise TimeoutError("Time limit exceeded")

    old_handler = signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


def compile_user_solve(user_code: str) -> Callable[[dict[str, Any]], dict[str, float]]:
    """
    Executes user's code and returns solve(params)->dict function.
    """
    # restricted-ish globals (not a real sandbox)
    safe_builtins = {
        "abs": abs,
        "min": min,
        "max": max,
        "sum": sum,
        "len": len,
        "range": range,
        "float": float,
        "int": int,
        "str": str,
        "print": print,  # можно убрать позже
    }

    globals_dict: dict[str, Any] = {"__builtins__": MappingProxyType(safe_builtins)}
    locals_dict: dict[str, Any] = {}

    exec(user_code, globals_dict, locals_dict)  # noqa: S102

    solve = locals_dict.get("solve") or globals_dict.get("solve")
    if not callable(solve):
        raise ValueError("User code must define function solve(params: dict) -> dict[str, float]")

    return solve  # type: ignore[return-value]

from __future__ import annotations

import signal
import threading
from contextlib import contextmanager
from types import MappingProxyType
from typing import Any, Callable


class TimeoutError(Exception):
    pass


def _is_main_thread() -> bool:
    return threading.current_thread() is threading.main_thread()


@contextmanager
def time_limit(seconds: int):
    if seconds <= 0:
        yield
        return

    if _is_main_thread():
        def handler(signum, frame):  # noqa: ARG001
            raise TimeoutError("Time limit exceeded")

        old_handler = signal.signal(signal.SIGALRM, handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
    else:
        timed_out = threading.Event()

        def _interrupt():
            timed_out.set()

        timer = threading.Timer(seconds, _interrupt)
        timer.start()
        try:
            yield
            if timed_out.is_set():
                raise TimeoutError("Time limit exceeded")
        finally:
            timer.cancel()


def compile_user_solve(user_code: str) -> Callable[[dict[str, Any]], dict[str, float]]:
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
        "print": print,
    }

    globals_dict: dict[str, Any] = {"__builtins__": MappingProxyType(safe_builtins)}
    locals_dict: dict[str, Any] = {}

    exec(user_code, globals_dict, locals_dict)  # noqa: S102

    solve = locals_dict.get("solve") or globals_dict.get("solve")
    if not callable(solve):
        raise ValueError("User code must define function solve(params: dict) -> dict[str, float]")

    return solve  # type: ignore[return-value]

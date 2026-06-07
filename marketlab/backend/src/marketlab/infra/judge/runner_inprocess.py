"""
Самый ответственный файл проекта — песочница для пользовательского кода.
Что тут делается:
 - SAFE_BUILTINS: белый список встроенных функций, всё остальное (import/open/eval) отрезано
 - compile_user_solve: exec кода в namespace с подменённым __builtins__
 - subprocess через multiprocessing.spawn — изоляция от main-процесса бекенда
 - SIGALRM на каждый тест и общий таймаут снаружи — двойная защита от висящего кода
 - threading.Semaphore — чтобы 40 студентов одновременно не съели всю ОЗУ VPS
"""

from __future__ import annotations

import multiprocessing
import os
import signal
import threading
from collections.abc import Callable
from contextlib import contextmanager
from types import MappingProxyType
from typing import Any


class TimeoutError(Exception):
    pass


# Сколько судей разрешено одновременно. Каждый подпроцесс — ~30–50 МБ,
# больше 4 на VPS с 1 ГБ ОЗУ — риск OOM при пиковой нагрузке.
_MAX_CONCURRENT_JUDGES = max(1, int(os.environ.get("MAX_CONCURRENT_JUDGES", "4")))
_judge_semaphore = threading.Semaphore(_MAX_CONCURRENT_JUDGES)


# Белый список встроенных функций, доступных пользовательскому коду.
# Всё, чего здесь нет (import, open, eval, getattr и т.д.), будет падать с NameError.
SAFE_BUILTINS: dict[str, Any] = {
    "abs": abs,
    "min": min,
    "max": max,
    "sum": sum,
    "pow": pow,
    "divmod": divmod,
    "round": round,
    "len": len,
    "range": range,
    "enumerate": enumerate,
    "zip": zip,
    "reversed": reversed,
    "sorted": sorted,
    "map": map,
    "filter": filter,
    "any": any,
    "all": all,
    "float": float,
    "int": int,
    "str": str,
    "bool": bool,
    "dict": dict,
    "list": list,
    "tuple": tuple,
    "set": set,
    "frozenset": frozenset,
    "isinstance": isinstance,
    "type": type,
    "Exception": Exception,
    "ValueError": ValueError,
    "ZeroDivisionError": ZeroDivisionError,
    "TypeError": TypeError,
    "KeyError": KeyError,
    "IndexError": IndexError,
    "ArithmeticError": ArithmeticError,
    "print": print,
}


@contextmanager
def time_limit(seconds: int):
    # SIGALRM умеет прерывать только main-thread процесса. В подпроцессе судьи
    # мы как раз в main-thread, поэтому таймаут срабатывает.
    if seconds <= 0:
        yield
        return

    is_main = threading.current_thread() is threading.main_thread()
    if is_main and hasattr(signal, "SIGALRM"):

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
        # Не main-thread — SIGALRM не работает. На этот случай есть глобальный
        # таймаут в родительском процессе, который убьёт подпроцесс целиком.
        yield


def compile_user_solve(user_code: str) -> Callable[[dict[str, Any]], dict[str, float]]:
    # MappingProxyType — иммутабельный view на dict. Даже если пользователь
    # попробует подменить __builtins__, у него ничего не получится.
    globals_dict: dict[str, Any] = {"__builtins__": MappingProxyType(SAFE_BUILTINS)}
    locals_dict: dict[str, Any] = {}

    exec(user_code, globals_dict, locals_dict)  # noqa: S102

    solve = locals_dict.get("solve") or globals_dict.get("solve")
    if not callable(solve):
        raise ValueError("User code must define function solve(params: dict) -> dict[str, float]")

    return solve  # type: ignore[return-value]


def _subprocess_worker(
    user_code: str,
    tests: list[dict[str, Any]],
    time_limit_sec: int,
    result_queue: Any,
) -> None:
    # Выполняется уже внутри отдельного процесса.
    try:
        solve = compile_user_solve(user_code)
    except Exception as e:
        result_queue.put({"status": "compile_error", "message": str(e), "results": []})
        return

    per_test: list[dict[str, Any]] = []
    for params in tests:
        try:
            with time_limit(time_limit_sec):
                out = solve(params)
        except TimeoutError:
            per_test.append({"status": "tle"})
            # На первом TLE прекращаем — вердикт всё равно будет TLE.
            result_queue.put({"status": "done", "results": per_test})
            return
        except Exception as e:
            per_test.append({"status": "runtime_error", "message": str(e)})
            continue
        per_test.append({"status": "ok", "result": out})

    result_queue.put({"status": "done", "results": per_test})


# spawn запускает чистый интерпретатор. fork в многопоточном FastAPI
# может породить дедлок, поэтому именно spawn.
_START_METHOD = "spawn"


def run_tests_subprocess(
    user_code: str,
    tests: list[dict[str, Any]],
    time_limit_sec: int,
) -> dict[str, Any]:
    # Семафор блокирует, если уже занято MAX_CONCURRENT_JUDGES слотов.
    with _judge_semaphore:
        ctx = multiprocessing.get_context(_START_METHOD)
        queue: Any = ctx.Queue()
        proc = ctx.Process(
            target=_subprocess_worker,
            args=(user_code, tests, time_limit_sec, queue),
            daemon=True,
        )
        proc.start()
        # Глобальный потолок: время на каждый тест × число тестов + запас на запуск/выход.
        total_timeout = time_limit_sec * max(1, len(tests)) + 10
        proc.join(timeout=total_timeout)

        if proc.is_alive():
            # Сначала SIGTERM, через 2 секунды — SIGKILL, если процесс жив.
            proc.terminate()
            proc.join(timeout=2)
            if proc.is_alive():
                proc.kill()
                proc.join()
            return {"status": "tle", "results": []}

        try:
            return queue.get_nowait()
        except Exception:
            # Процесс завершился, но в очереди ничего нет — упал по segfault или OOM.
            return {
                "status": "crashed",
                "message": f"Worker process exited with code {proc.exitcode}",
                "results": [],
            }

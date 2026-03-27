from __future__ import annotations

import random
from typing import Any

from marketlab.usecases.registry import TASK_REGISTRY


def generate_tests(
    task_id: str,
    *,
    n: int = 25,
    seed: int | None = None,
) -> list[dict[str, Any]]:

    gen = _GENERATORS.get(task_id)
    if gen is None:
        raise ValueError(f"No test generator registered for task '{task_id}'")

    spec, oracle = TASK_REGISTRY[task_id]

    return gen(oracle=oracle, n=n, seed=seed)


def _gen_equilibrium_linear(
    *,
    oracle,
    n: int,
    seed: int | None,
) -> list[dict[str, Any]]:
    rng = random.Random(seed)

    public_test: dict[str, Any] = {
        "a": 120.0,
        "b": 3.0,
        "c": -10.0,
        "d": 2.0,
        "mode": "tax",
        "t": 10.0,
    }

    tests: list[dict[str, Any]] = [public_test]
    modes = ("none", "tax", "subsidy")

    forced_modes = list(modes)
    rng.shuffle(forced_modes)

    attempts = 0
    max_attempts = n * 20

    while len(tests) < n and attempts < max_attempts:
        attempts += 1

        if forced_modes:
            mode = forced_modes.pop()
        else:
            mode = rng.choice(modes)

        a = round(rng.uniform(20, 300), 2)
        b = round(rng.uniform(0.5, 10), 2)
        d = round(rng.uniform(0.5, 10), 2)
        c = round(rng.uniform(-100, a * 0.4), 2)

        if mode == "none":
            t = 0.0
        else:
            t = round(rng.uniform(1, 30), 2)

        params: dict[str, Any] = {
            "a": a, "b": b, "c": c, "d": d, "mode": mode, "t": t,
        }

        try:
            oracle(params)
        except Exception:
            continue

        tests.append(params)

    return tests


_GENERATORS = {
    "equilibrium_linear_v1": _gen_equilibrium_linear,
}

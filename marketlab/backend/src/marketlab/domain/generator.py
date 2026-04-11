from __future__ import annotations

import random
from typing import Any

from marketlab.usecases.registry import TASK_REGISTRY


def generate_tests(task_id: str, *, n: int = 25, seed: int | None = None) -> list[dict[str, Any]]:
    gen = _GENERATORS.get(task_id)
    if gen is None:
        raise ValueError(f"No test generator registered for task '{task_id}'")
    spec, oracle = TASK_REGISTRY[task_id]
    return gen(oracle=oracle, n=n, seed=seed)


def _gen_equilibrium_linear(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests: list[dict[str, Any]] = [{"a": 120.0, "b": 3.0, "c": -10.0, "d": 2.0, "mode": "tax", "t": 10.0}]
    modes = ("none", "tax", "subsidy")
    remaining = n - 1
    per_mode = remaining // 3
    schedule = []
    for m in modes:
        schedule.extend([m] * per_mode)
    while len(schedule) < remaining:
        schedule.append(rng.choice(modes))
    rng.shuffle(schedule)
    idx = 0
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        mode = schedule[idx] if idx < len(schedule) else rng.choice(modes)
        a = round(rng.uniform(20, 300), 2)
        b = round(rng.uniform(0.5, 10), 2)
        d = round(rng.uniform(0.5, 10), 2)
        c = round(rng.uniform(-100, a * 0.4), 2)
        t = 0.0 if mode == "none" else round(rng.uniform(5, 50), 2)
        params = {"a": a, "b": b, "c": c, "d": d, "mode": mode, "t": t}
        try:
            oracle(params)
        except Exception:
            continue
        tests.append(params)
        idx += 1
    return tests


def _gen_surplus(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 200.0, "b": 4.0, "c": 20.0, "d": 2.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        a = round(rng.uniform(50, 300), 2)
        b = round(rng.uniform(0.5, 8), 2)
        d = round(rng.uniform(0.5, 8), 2)
        c = round(rng.uniform(-50, a * 0.3), 2)
        params = {"a": a, "b": b, "c": c, "d": d}
        try:
            r = oracle(params)
            if r["cs"] <= 0 or r["ps"] <= 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_dwl(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 150.0, "b": 2.0, "c": 10.0, "d": 3.0, "t": 15.0, "mode": "tax"}]
    modes = ("tax", "subsidy")
    schedule = []
    remaining = n - 1
    for m in modes:
        schedule.extend([m] * (remaining // 2))
    while len(schedule) < remaining:
        schedule.append(rng.choice(modes))
    rng.shuffle(schedule)
    idx = 0
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        mode = schedule[idx] if idx < len(schedule) else rng.choice(modes)
        a = round(rng.uniform(50, 300), 2)
        b = round(rng.uniform(0.5, 8), 2)
        d = round(rng.uniform(0.5, 8), 2)
        c = round(rng.uniform(-50, a * 0.3), 2)
        t = round(rng.uniform(5, 40), 2)
        params = {"a": a, "b": b, "c": c, "d": d, "t": t, "mode": mode}
        try:
            r = oracle(params)
            if r["q_new"] <= 0 or r["dwl"] < 0:
                continue
        except Exception:
            continue
        tests.append(params)
        idx += 1
    return tests


def _gen_elasticity(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 120.0, "b": 3.0, "p": 15.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        a = round(rng.uniform(50, 300), 2)
        b = round(rng.uniform(0.5, 8), 2)
        max_p = a / b
        p = round(rng.uniform(max_p * 0.1, max_p * 0.9), 2)
        params = {"a": a, "b": b, "p": p}
        try:
            oracle(params)
            if a - b * p <= 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_price_ceiling(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 200.0, "b": 2.0, "c": 20.0, "d": 1.0, "p_ceil": 50.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        a = round(rng.uniform(50, 300), 2)
        b = round(rng.uniform(0.5, 8), 2)
        d = round(rng.uniform(0.5, 8), 2)
        c = round(rng.uniform(-50, a * 0.3), 2)
        p_eq = (a - c) / (b + d)
        # Half tests binding, half not
        if rng.random() < 0.6:
            p_ceil = round(rng.uniform(p_eq * 0.3, p_eq * 0.9), 2)
        else:
            p_ceil = round(rng.uniform(p_eq * 1.1, p_eq * 2.0), 2)
        params = {"a": a, "b": b, "c": c, "d": d, "p_ceil": p_ceil}
        try:
            r = oracle(params)
            if r["q_traded"] <= 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_tax_revenue(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 180.0, "b": 3.0, "c": 10.0, "d": 2.0, "t": 12.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        a = round(rng.uniform(50, 300), 2)
        b = round(rng.uniform(0.5, 8), 2)
        d = round(rng.uniform(0.5, 8), 2)
        c = round(rng.uniform(-50, a * 0.3), 2)
        t = round(rng.uniform(3, 40), 2)
        params = {"a": a, "b": b, "c": c, "d": d, "t": t}
        try:
            r = oracle(params)
            if r["q_tax"] <= 0 or r["tax_revenue"] <= 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_demand_shift(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 100.0, "b": 2.0, "c": 20.0, "d": 1.0, "a_new": 150.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        a = round(rng.uniform(50, 250), 2)
        b = round(rng.uniform(0.5, 8), 2)
        d = round(rng.uniform(0.5, 8), 2)
        c = round(rng.uniform(-50, a * 0.3), 2)
        shift = round(rng.uniform(-a * 0.5, a * 0.8), 2)
        a_new = round(a + shift, 2)
        params = {"a": a, "b": b, "c": c, "d": d, "a_new": a_new}
        try:
            r = oracle(params)
            if r["q_new"] <= 0 or r["q_old"] <= 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


_GENERATORS = {
    "equilibrium_linear_v1": _gen_equilibrium_linear,
    "surplus_calc_v1": _gen_surplus,
    "dwl_tax_v1": _gen_dwl,
    "elasticity_v1": _gen_elasticity,
    "price_ceiling_v1": _gen_price_ceiling,
    "tax_revenue_v1": _gen_tax_revenue,
    "demand_shift_v1": _gen_demand_shift,
}

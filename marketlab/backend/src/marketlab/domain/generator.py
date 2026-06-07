"""
В данной файле собраны генераторы тестов для каждой из задач из общего пулла задач, 
при создании новых задач необходимо добавить сюда генератор
Общий цикл их работы заключается в создании случайных параметров для задачи, которые должны быть
экономически осмысленнными, затем берётся солвер задачи и проверяется, достигается ли на данных значениях
корректное с точки зрения экономики решение, в случае успеха тест добавляется в пул тестов, если нет - то 
продолжается дальнейшее генерирование параметров 
"""

from __future__ import annotations
import random
from typing import Any
from marketlab.usecases.registry import TASK_REGISTRY

"""
Данная функция является связующим звеном между задачей и генератором, производится поиск необходимого генератора из банка
"""
def generate_tests(task_id: str, *, n: int = 25, seed: int | None = None) -> list[dict[str, Any]]:
    gen = _GENERATORS.get(task_id)
    if gen is None:
        raise ValueError(f"No test generator registered for task '{task_id}'")
    _, oracle = TASK_REGISTRY[task_id]
    return gen(oracle=oracle, n=n, seed=seed)

"""
Каждая из таких функций имеет схожую структуру:
1) Формирование публичного теста
1) Инициализация генератора случайных чисел с заданным сидом для воспроизводимости
2) Создание начального теста с фиксированными параметрами для гарантии наличия хотя бы одного корректного теста
3) Цикл генерации случайных параметров, проверка их на корректность с помощью солвера , добавление в пул тестов при успехе
Далее просто происходит повторение данного шаблона для каждого из тестов с учётом особенностей задачи
"""
def _gen_equilibrium_linear(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests: list[dict[str, Any]] = [
        {"a": 120.0, "b": 3.0, "c": -10.0, "d": 2.0, "mode": "tax", "t": 10.0}
    ]
    modes = ("none", "tax", "subsidy")
    remaining = n - 1
    per_mode = remaining // 3
    schedule = []
    for m in modes:
        schedule.extend([m] * per_mode) #делаем так, чтобы количество тестов с разными режимами влияния государство было равномерным(примерно)
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


def _gen_price_floor(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 200.0, "b": 2.0, "c": 20.0, "d": 1.0, "p_floor": 70.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        a = round(rng.uniform(50, 300), 2)
        b = round(rng.uniform(0.5, 8), 2)
        d = round(rng.uniform(0.5, 8), 2)
        c = round(rng.uniform(-50, a * 0.3), 2)
        p_eq = (a - c) / (b + d)
        if rng.random() < 0.6:
            p_floor = round(rng.uniform(p_eq * 1.1, p_eq * 2.0), 2)
        else:
            p_floor = round(rng.uniform(p_eq * 0.3, p_eq * 0.9), 2)
        params = {"a": a, "b": b, "c": c, "d": d, "p_floor": p_floor}
        try:
            r = oracle(params)
            if r["q_traded"] <= 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_supply_shift(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 150.0, "b": 2.0, "c": 10.0, "d": 1.5, "c_new": 40.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        a = round(rng.uniform(50, 250), 2)
        b = round(rng.uniform(0.5, 8), 2)
        d = round(rng.uniform(0.5, 8), 2)
        c = round(rng.uniform(-50, a * 0.3), 2)
        shift = round(rng.uniform(-a * 0.5, a * 0.8), 2)
        c_new = round(c + shift, 2)
        params = {"a": a, "b": b, "c": c, "d": d, "c_new": c_new}
        try:
            r = oracle(params)
            if r["q_new"] <= 0 or r["q_old"] <= 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_income_elasticity(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"q1": 100.0, "i1": 2000.0, "q2": 130.0, "i2": 2500.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        i1 = round(rng.uniform(500, 5000), 2)
        i2 = round(rng.uniform(500, 5000), 2)
        if abs(i2 - i1) < 50:
            continue
        q1 = round(rng.uniform(10, 500), 2)
        good_type = rng.choice(["normal", "inferior", "luxury"])
        income_ratio = i2 / i1
        if good_type == "normal":
            q2 = round(q1 * (1 + rng.uniform(0.02, 0.5) * (income_ratio - 1)), 2)
        elif good_type == "inferior":
            q2 = round(q1 * (1 - rng.uniform(0.05, 0.4) * abs(income_ratio - 1)), 2)
        else:  # luxury
            q2 = round(q1 * (1 + rng.uniform(1.0, 3.0) * abs(income_ratio - 1)), 2)
        if q1 <= 0 or q2 <= 0:
            continue
        params = {"q1": q1, "i1": i1, "q2": q2, "i2": i2}
        try:
            oracle(params)
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_demand_aggregation(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a1": 100.0, "b1": 2.0, "a2": 80.0, "b2": 1.5, "c": 10.0, "d": 2.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        force_segment_2 = rng.random() < 0.3
        if force_segment_2:
            a1 = round(rng.uniform(20, 50), 2)
            b1 = round(rng.uniform(2, 6), 2)
            a2 = round(rng.uniform(120, 250), 2)
            b2 = round(rng.uniform(0.5, 2), 2)
            d = round(rng.uniform(1, 4), 2)
            c = round(rng.uniform(-20, 20), 2)
        else:
            a1 = round(rng.uniform(30, 200), 2)
            b1 = round(rng.uniform(0.5, 6), 2)
            a2 = round(rng.uniform(30, 200), 2)
            b2 = round(rng.uniform(0.5, 6), 2)
            d = round(rng.uniform(0.5, 6), 2)
            c = round(rng.uniform(-20, min(a1, a2) * 0.2), 2)
        params = {"a1": a1, "b1": b1, "a2": a2, "b2": b2, "c": c, "d": d}
        try:
            r = oracle(params)
            if r["q_eq"] <= 0 or r["p_eq"] <= 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_monopoly(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"A": 100.0, "B": 2.0, "mc": 20.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        A = round(rng.uniform(50, 400), 2)
        B = round(rng.uniform(0.5, 10), 2)
        mc = round(rng.uniform(1, A * 0.6), 2)
        if A <= mc:
            continue
        params = {"A": A, "B": B, "mc": mc}
        try:
            r = oracle(params)
            if r["q_monopoly"] <= 0 or r["profit"] <= 0 or r["dwl"] < 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_ad_valorem_tax(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 200.0, "b": 3.0, "c": 10.0, "d": 2.0, "tau": 0.2}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        a = round(rng.uniform(50, 300), 2)
        b = round(rng.uniform(0.5, 8), 2)
        d = round(rng.uniform(0.5, 8), 2)
        c = round(rng.uniform(-30, a * 0.3), 2)
        tau = round(rng.uniform(0.05, 0.5), 3)
        params = {"a": a, "b": b, "c": c, "d": d, "tau": tau}
        try:
            r = oracle(params)
            if r["q_new"] <= 0 or r["dwl"] < 0 or r["tax_revenue"] <= 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_trade_tariff(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 300.0, "b": 4.0, "c": 20.0, "d": 3.0, "p_world": 30.0, "tariff": 10.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        a = round(rng.uniform(100, 400), 2)
        b = round(rng.uniform(1, 8), 2)
        d = round(rng.uniform(0.5, 6), 2)
        c = round(rng.uniform(-30, a * 0.2), 2)
        p_eq = (a - c) / (b + d)
        if p_eq <= 0 or p_eq * 0.3 >= p_eq * 0.8:
            continue
        p_world = round(rng.uniform(p_eq * 0.3, p_eq * 0.8), 2)
        max_tariff = (p_eq - p_world) * 0.8
        if max_tariff <= p_world * 0.05:
            continue
        tariff = round(rng.uniform(p_world * 0.05, max_tariff), 2)
        params = {"a": a, "b": b, "c": c, "d": d, "p_world": p_world, "tariff": tariff}
        try:
            r = oracle(params)
            if r["imports_free"] <= 0 or r["dwl"] < 0 or r["tariff_revenue"] <= 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_pigouvian_tax(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 200.0, "b": 4.0, "c": 20.0, "d": 2.0, "e": 5.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        a = round(rng.uniform(50, 300), 2)
        b = round(rng.uniform(0.5, 8), 2)
        d = round(rng.uniform(0.5, 8), 2)
        c = round(rng.uniform(-30, a * 0.3), 2)
        p_eq = (a - c) / (b + d)
        e = round(rng.uniform(1, p_eq * 0.4), 2)
        params = {"a": a, "b": b, "c": c, "d": d, "e": e}
        try:
            r = oracle(params)
            if r["q_social"] <= 0 or r["dwl_without_tax"] < 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_simultaneous_shift(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 200.0, "b": 3.0, "c": 10.0, "d": 2.0, "a_new": 250.0, "c_new": 30.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        a = round(rng.uniform(50, 250), 2)
        b = round(rng.uniform(0.5, 8), 2)
        d = round(rng.uniform(0.5, 8), 2)
        c = round(rng.uniform(-30, a * 0.3), 2)
        a_new = round(a + rng.uniform(-a * 0.4, a * 0.6), 2)
        c_new = round(c + rng.uniform(-40, 80), 2)
        params = {"a": a, "b": b, "c": c, "d": d, "a_new": a_new, "c_new": c_new}
        try:
            r = oracle(params)
            if r["q_old"] <= 0 or r["q_new"] <= 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_gov_price_support(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 200.0, "b": 2.0, "c": 20.0, "d": 3.0, "p_support": 55.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        a = round(rng.uniform(50, 300), 2)
        b = round(rng.uniform(0.5, 8), 2)
        d = round(rng.uniform(0.5, 8), 2)
        c = round(rng.uniform(-30, a * 0.3), 2)
        p_eq = (a - c) / (b + d)
        p_support = round(rng.uniform(p_eq * 1.1, p_eq * 2.0), 2)
        params = {"a": a, "b": b, "c": c, "d": d, "p_support": p_support}
        try:
            r = oracle(params)
            if r["gov_purchase"] <= 0 or r["dwl"] < 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_revenue_max(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 120.0, "b": 3.0, "p_current": 15.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        a = round(rng.uniform(50, 300), 2)
        b = round(rng.uniform(0.5, 8), 2)
        p_max = a / b
        p_opt = a / (2 * b)
        p_current = round(rng.uniform(p_max * 0.1, p_max * 0.95), 2)
        if abs(p_current - p_opt) < 0.5:
            continue
        params = {"a": a, "b": b, "p_current": p_current}
        try:
            r = oracle(params)
            if r["revenue_gain"] < 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_welfare_supply_improvement(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 200.0, "b": 3.0, "c": 10.0, "d": 2.0, "c_new": 40.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        a = round(rng.uniform(50, 250), 2)
        b = round(rng.uniform(0.5, 8), 2)
        d = round(rng.uniform(0.5, 8), 2)
        c = round(rng.uniform(-30, a * 0.25), 2)
        c_new = round(c + rng.uniform(5, 80), 2)
        params = {"a": a, "b": b, "c": c, "d": d, "c_new": c_new}
        try:
            r = oracle(params)
            if r["p_old"] <= 0 or r["p_new"] <= 0 or r["delta_cs"] < 0 or r["delta_ts"] < 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests


def _gen_laffer_commodity(*, oracle, n: int, seed: int | None) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    tests = [{"a": 200.0, "b": 3.0, "c": 10.0, "d": 2.0, "current_tax": 8.0}]
    attempts = 0
    while len(tests) < n and attempts < n * 20:
        attempts += 1
        a = round(rng.uniform(50, 300), 2)
        b = round(rng.uniform(0.5, 8), 2)
        d = round(rng.uniform(0.5, 8), 2)
        c = round(rng.uniform(-30, a * 0.3), 2)
        q0 = (a * d + b * c) / (b + d)
        slope = b * d / (b + d)
        if q0 <= 0 or slope <= 0:
            continue
        t_opt = q0 / (2 * slope)
        current_tax = round(rng.uniform(t_opt * 0.1, t_opt * 1.8), 2)
        params = {"a": a, "b": b, "c": c, "d": d, "current_tax": current_tax}
        try:
            r = oracle(params)
            if r["t_opt"] <= 0 or r["revenue_max"] <= 0:
                continue
        except Exception:
            continue
        tests.append(params)
    return tests

"""
Собираем в общий словарь, чтобы в функции generate_tests по id задачи можно было найти нужный генератор, при добавлении новых задач необходимо сюда добавить генератор
"""
_GENERATORS = {
    "equilibrium_linear_v1": _gen_equilibrium_linear,
    "surplus_calc_v1": _gen_surplus,
    "dwl_tax_v1": _gen_dwl,
    "elasticity_v1": _gen_elasticity,
    "price_ceiling_v1": _gen_price_ceiling,
    "tax_revenue_v1": _gen_tax_revenue,
    "demand_shift_v1": _gen_demand_shift,
    "price_floor_v1": _gen_price_floor,
    "supply_shift_v1": _gen_supply_shift,
    "income_elasticity_v1": _gen_income_elasticity,
    "demand_aggregation_v1": _gen_demand_aggregation,
    "monopoly_v1": _gen_monopoly,
    "ad_valorem_tax_v1": _gen_ad_valorem_tax,
    "trade_tariff_v1": _gen_trade_tariff,
    "pigouvian_tax_v1": _gen_pigouvian_tax,
    "simultaneous_shift_v1": _gen_simultaneous_shift,
    "gov_price_support_v1": _gen_gov_price_support,
    "revenue_max_v1": _gen_revenue_max,
    "welfare_supply_improvement_v1": _gen_welfare_supply_improvement,
    "laffer_commodity_v1": _gen_laffer_commodity,
}

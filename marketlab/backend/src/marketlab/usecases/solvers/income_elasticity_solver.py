"""
Генератор к задаче, тема которой это эластичность спроса по доходу, наиболее сложна здесь формула 
для расчёта дуговой эластичности:
E_I = ((Q2 - Q1) / ((Q2 + Q1) / 2)) / ((I2 - I1) / ((I2 + I1) / 2))
"""



from __future__ import annotations
from typing import Any


def solve_income_elasticity(params: dict[str, Any]) -> dict[str, float]:
    q1: float = float(params["q1"])
    q2: float = float(params["q2"])
    i1: float = float(params["i1"])
    i2: float = float(params["i2"])

    if q1 <= 0 or q2 <= 0 or i1 <= 0 or i2 <= 0:
        raise ValueError("All quantities and incomes must be positive")
    if i1 == i2:
        raise ValueError("Incomes must differ")

    dq = q2 - q1
    di = i2 - i1
    avg_q = (q1 + q2) / 2
    avg_i = (i1 + i2) / 2
    income_elasticity = (dq / avg_q) / (di / avg_i)
    if income_elasticity > 1e-9: #здесь рассматриваются три вида товаров
        is_normal = 1.0
    elif income_elasticity < -1e-9:
        is_normal = -1.0
    else:
        is_normal = 0.0

    if income_elasticity > 1: #рассматриваем градацию по критерию роскоши и первой необходимости
        is_luxury = 1.0
    else:
        is_luxury = 0.0

    return {
        "income_elasticity": round(income_elasticity, 6),
        "is_normal": is_normal,
        "is_luxury": is_luxury,
    }

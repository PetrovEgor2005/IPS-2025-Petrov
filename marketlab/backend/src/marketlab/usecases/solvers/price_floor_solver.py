"""
Задача на минимальную цену на конкурентном рынке, обнаружение избыточного предложения
"""


from __future__ import annotations
from typing import Any


def solve_price_floor(params: dict[str, Any]) -> dict[str, float]:
    a: float = float(params["a"])
    b: float = float(params["b"])
    c: float = float(params["c"])
    d: float = float(params["d"])
    p_floor: float = float(params["p_floor"])

    if b <= 0 or d <= 0:
        raise ValueError("b and d must be positive")

    p_eq = (a - c) / (b + d)
    if p_floor > p_eq:
        p_actual = p_floor
        binding = 1.0
    else:
        p_actual = p_eq
        binding = 0.0
    q_demanded = max(0.0, a - b * p_actual)
    q_supplied = max(0.0, c + d * p_actual)
    q_traded = min(q_demanded, q_supplied)
    surplus_qty = max(0.0, q_supplied - q_demanded)

    return {
        "p_actual": round(p_actual, 6),
        "q_demanded": round(q_demanded, 6),
        "q_supplied": round(q_supplied, 6),
        "q_traded": round(q_traded, 6),
        "surplus_qty": round(surplus_qty, 6),
        "binding": binding,
    }

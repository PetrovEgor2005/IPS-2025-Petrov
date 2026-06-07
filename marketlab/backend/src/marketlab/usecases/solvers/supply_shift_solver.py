"""
Задача направлена на рассмотрение такого шока, как сдвиг кривой предложения и нахождение
нового равновесия
"""

from __future__ import annotations
from typing import Any


def solve_supply_shift(params: dict[str, Any]) -> dict[str, float]:
    a: float = float(params["a"])
    b: float = float(params["b"])
    c: float = float(params["c"])
    d: float = float(params["d"])
    c_new: float = float(params["c_new"])

    if b <= 0 or d <= 0:
        raise ValueError("b and d must be positive")
    p_old = (a - c) / (b + d)
    q_old = a - b * p_old
    p_new = (a - c_new) / (b + d)
    q_new = a - b * p_new
    if q_old <= 0 or q_new <= 0:
        raise ValueError("Equilibrium quantities must be positive")

    return {
        "p_old": round(p_old, 6),
        "q_old": round(q_old, 6),
        "p_new": round(p_new, 6),
        "q_new": round(q_new, 6),
        "delta_p": round(p_new - p_old, 6),
        "delta_q": round(q_new - q_old, 6),
    }

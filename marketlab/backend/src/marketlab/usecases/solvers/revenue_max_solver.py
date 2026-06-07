from __future__ import annotations
from typing import Any


def solve_revenue_max(params: dict[str, Any]) -> dict[str, float]:
    # Максимизация выручки на линейном спросе Qd = a - bP. Оптимум: P* = a/(2b).
    a = float(params["a"])
    b = float(params["b"])
    p_current = float(params["p_current"])

    if b <= 0:
        raise ValueError("b must be positive")
    if a <= 0:
        raise ValueError("a must be positive")
    if not (0 < p_current < a / b):
        raise ValueError("p_current must be between 0 and a/b (so Q > 0)")

    # Максимизируем выручку
    p_optimal = a / (2 * b)
    q_optimal = a / 2
    tr_max = a**2 / (4 * b)
    q_current = a - b * p_current
    tr_current = p_current * q_current
    revenue_gain = tr_max - tr_current

    # Эластичность
    ed_current = -b * p_current / q_current

    return {
        "p_optimal": round(p_optimal, 6),
        "q_optimal": round(q_optimal, 6),
        "tr_max": round(tr_max, 6),
        "tr_current": round(tr_current, 6),
        "revenue_gain": round(revenue_gain, 6),
        "ed_current": round(ed_current, 6),
    }

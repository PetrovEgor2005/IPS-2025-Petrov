from __future__ import annotations
from typing import Any


def solve_laffer_commodity(params: dict[str, Any]) -> dict[str, float]:
    # Кривая Лаффера: ищем налоговую ставку, максимизирующую поступления.
    a = float(params["a"])
    b = float(params["b"])
    c = float(params["c"])
    d = float(params["d"])
    current_tax = float(params["current_tax"])

    if b <= 0:
        raise ValueError("b must be positive")
    if d <= 0:
        raise ValueError("d must be positive")
    if current_tax <= 0:
        raise ValueError("current_tax must be positive")

    # объём при налоге: Q(t) = Q0 - slope*t
    q0 = (a * d + b * c) / (b + d)
    slope = b * d / (b + d)
    if q0 <= 0:
        raise ValueError("Q0 must be positive")

    # Поступления R(t) = t * (Q0 - slope*t) — парабола, максимум в t_opt = Q0/(2*slope).
    t_opt = q0 / (2 * slope)
    if t_opt <= 0:
        raise ValueError("t_opt must be positive")
    q_at_opt = q0 / 2
    revenue_max = t_opt * q_at_opt

    # Цены при оптимальной ставке
    p_buyer_opt = (a - c + d * t_opt) / (b + d)
    p_seller_opt = p_buyer_opt - t_opt

    # Запретительная ставка, при которой объём = 0, поступления = 0.
    t_prohibitive = q0 / slope

    # Поступления при текущей ставке
    q_current = q0 - slope * current_tax
    rev_current = current_tax * q_current if q_current > 0 else 0.0
    return {
        "t_opt": round(t_opt, 6),
        "q_at_opt": round(q_at_opt, 6),
        "revenue_max": round(revenue_max, 6),
        "p_buyer_opt": round(p_buyer_opt, 6),
        "p_seller_opt": round(p_seller_opt, 6),
        "t_prohibitive": round(t_prohibitive, 6),
        "rev_current": round(rev_current, 6),
    }

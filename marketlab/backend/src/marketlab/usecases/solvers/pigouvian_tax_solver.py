from __future__ import annotations
from typing import Any


def solve_pigouvian_tax(params: dict[str, Any]) -> dict[str, float]:
    # Налог Пигу, корректирует отрицательный внешний эффект производства до социального оптимума.
    a = float(params["a"])
    b = float(params["b"])
    c = float(params["c"])
    d = float(params["d"])
    e = float(params["e"])

    if b <= 0:
        raise ValueError("b must be positive")
    if d <= 0:
        raise ValueError("d must be positive")
    if e <= 0:
        raise ValueError("e (external_cost) must be positive")

    # Равновесие без налога
    p_market = (a - c) / (b + d)
    q_market = a - b * p_market

    # Точка, оптимальная для общества
    p_social = (a - c + d * e) / (b + d)
    q_social = a - b * p_social
    if q_social <= 0:
        raise ValueError("Q_social must be positive")
    pigouvian_tax = e
    external_damage = e * q_market
    dwl_without_tax = 0.5 * e * (q_market - q_social)

    return {
        "p_market": round(p_market, 6),
        "q_market": round(q_market, 6),
        "p_social": round(p_social, 6),
        "q_social": round(q_social, 6),
        "pigouvian_tax": round(pigouvian_tax, 6),
        "external_damage": round(external_damage, 6),
        "dwl_without_tax": round(dwl_without_tax, 6),
    }

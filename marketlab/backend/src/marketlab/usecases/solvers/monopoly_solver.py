"""
В данной задаче рассматривается равновесие монополиста на рынке, необходимо 
расчитать обратную функцию спроса и знать условте конкуретного равновесия
"""

from __future__ import annotations
from typing import Any


def solve_monopoly(params: dict[str, Any]) -> dict[str, float]:
    A: float = float(params["A"])
    B: float = float(params["B"])
    mc: float = float(params["mc"])

    if B <= 0:
        raise ValueError("B must be positive")
    if A <= mc:
        raise ValueError("A must be greater than mc for a viable market")
    if mc < 0:
        raise ValueError("Marginal cost mc must be non-negative")

    q_monopoly = (A - mc) / (2 * B)
    p_monopoly = (A + mc) / 2
    profit = (p_monopoly - mc) * q_monopoly 
    cs = 0.5 * (A - p_monopoly) * q_monopoly 
    q_competitive = (A - mc) / B
    p_competitive = mc
    dwl = 0.5 * (p_monopoly - p_competitive) * (q_competitive - q_monopoly)

    return {
        "p_monopoly": round(p_monopoly, 6),
        "q_monopoly": round(q_monopoly, 6),
        "profit": round(profit, 6),
        "cs": round(cs, 6),
        "p_competitive": round(p_competitive, 6),
        "q_competitive": round(q_competitive, 6),
        "dwl": round(dwl, 6),
    }

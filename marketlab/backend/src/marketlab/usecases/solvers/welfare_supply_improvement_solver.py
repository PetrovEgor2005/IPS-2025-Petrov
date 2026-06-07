

from __future__ import annotations
from typing import Any


def solve_welfare_supply_improvement(params: dict[str, Any]) -> dict[str, float]:
    # Технологический прогресс, значит сдвиг предложения вправо, оказывается влияние на CS/PS.
    a = float(params["a"])
    b = float(params["b"])
    c = float(params["c"])
    d = float(params["d"])
    c_new = float(params["c_new"])
    if b <= 0:
        raise ValueError("b must be positive")
    if d <= 0:
        raise ValueError("d must be positive")
    if c_new <= c:
        raise ValueError("c_new must be greater than c (rightward supply shift)")
    p_old = (a - c) / (b + d)
    q_old = a - b * p_old

    if q_old <= 0:
        raise ValueError("Q_old must be positive")
    p_new = (a - c_new) / (b + d)
    q_new = a - b * p_new
    if q_new <= 0:
        raise ValueError("Q_new must be positive")
    
    cs_old = 0.5 * (a / b - p_old) * q_old
    ps_old = 0.5 * (p_old + c / d) * q_old
    cs_new = 0.5 * (a / b - p_new) * q_new
    ps_new = 0.5 * (p_new + c_new / d) * q_new #рассчитываем благосостояние

    delta_cs = cs_new - cs_old
    delta_ps = ps_new - ps_old
    delta_ts = delta_cs + delta_ps #рассчитываем изменение благосостояния
    price_drop_pct = (p_old - p_new) / p_old * 100
    return {
        "p_old": round(p_old, 6),
        "p_new": round(p_new, 6),
        "cs_old": round(cs_old, 6),
        "cs_new": round(cs_new, 6),
        "ps_old": round(ps_old, 6),
        "ps_new": round(ps_new, 6),
        "delta_cs": round(delta_cs, 6),
        "delta_ps": round(delta_ps, 6),
        "delta_ts": round(delta_ts, 6),
        "price_drop_pct": round(price_drop_pct, 6),
    }

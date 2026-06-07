from __future__ import annotations

from typing import Any


def solve_simultaneous_shift(params: dict[str, Any]) -> dict[str, float]:
    # Одновременный сдвиг спроса и предложения: считаем изменение CS и PS.
    a = float(params["a"])
    b = float(params["b"])
    c = float(params["c"])
    d = float(params["d"])
    a_new = float(params["a_new"])
    c_new = float(params["c_new"])

    if b <= 0:
        raise ValueError("b must be positive")
    if d <= 0:
        raise ValueError("d must be positive")

    # Старое равновесие
    p_old = (a - c) / (b + d)
    q_old = a - b * p_old

    if q_old <= 0:
        raise ValueError("Q_old must be positive")

    # Новое равновесие
    p_new = (a_new - c_new) / (b + d)
    q_new = a_new - b * p_new
    if q_new <= 0:
        raise ValueError("Q_new must be positive")
    delta_p = p_new - p_old
    delta_q = q_new - q_old

    # Расчёт благосостояния
    cs_old = 0.5 * (a / b - p_old) * q_old
    ps_old = 0.5 * (p_old + c / d) * q_old
    cs_new = 0.5 * (a_new / b - p_new) * q_new
    ps_new = 0.5 * (p_new + c_new / d) * q_new
    delta_cs = cs_new - cs_old
    delta_ps = ps_new - ps_old

    return {
        "p_old": round(p_old, 6),
        "q_old": round(q_old, 6),
        "p_new": round(p_new, 6),
        "q_new": round(q_new, 6),
        "delta_p": round(delta_p, 6),
        "delta_q": round(delta_q, 6),
        "delta_cs": round(delta_cs, 6),
        "delta_ps": round(delta_ps, 6),
    }

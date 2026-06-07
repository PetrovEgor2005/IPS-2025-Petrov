from __future__ import annotations

from typing import Any


def solve_demand_aggregation(params: dict[str, Any]) -> dict[str, float]:
    # Агрегирование спроса двух потребителей с линейными Qd1, Qd2.
    # Рыночное равновесие может оказаться в двух сегментах: оба активны или
    # «дешёвый» отсечён ценой — это обрабатывается ниже.
    a1: float = float(params["a1"])
    b1: float = float(params["b1"])
    a2: float = float(params["a2"])
    b2: float = float(params["b2"])
    c: float = float(params["c"])
    d: float = float(params["d"])

    if b1 <= 0 or b2 <= 0 or d <= 0:
        raise ValueError("Slope parameters must be positive")

    # Choke-цены (при них Qd = 0).
    p_choke1 = a1 / b1
    p_choke2 = a2 / b2

    p_choke_low = min(p_choke1, p_choke2)
    p_choke_high = max(p_choke1, p_choke2)

    # «Более терпеливый» потребитель — тот, у кого choke-цена выше.
    if p_choke1 <= p_choke2:
        a_high, b_high = a2, b2
    else:
        a_high, b_high = a1, b1

    # Сегмент 1: оба потребителя активны (P <= p_choke_low).
    # Суммарный спрос: (a1+a2) - (b1+b2)*P = c + d*P  →  P = (a1+a2-c)/(b1+b2+d).
    p_eq = (a1 + a2 - c) / (b1 + b2 + d)

    if p_eq <= p_choke_low:
        q_eq = c + d * p_eq
        q1_eq = a1 - b1 * p_eq
        q2_eq = a2 - b2 * p_eq
    else:
        # Сегмент 2: «дешёвый» потребитель выбит ценой. Решаем заново
        # только с «терпеливым»: P = (a_high - c) / (b_high + d).
        p_eq = (a_high - c) / (b_high + d)
        if not (p_choke_low < p_eq <= p_choke_high):
            raise ValueError("No positive equilibrium: even the high-choke consumer is priced out")
        q_eq = c + d * p_eq
        q_high_eq = a_high - b_high * p_eq
        if p_choke1 >= p_choke2:
            q1_eq = q_high_eq
            q2_eq = 0.0
        else:
            q1_eq = 0.0
            q2_eq = q_high_eq

    if q_eq <= 0:
        raise ValueError("Equilibrium quantity must be positive")

    # CS каждого потребителя — треугольник между его choke-ценой и p_eq.
    cs1 = 0.5 * max(0.0, (a1 / b1) - p_eq) * q1_eq if q1_eq > 0 else 0.0
    cs2 = 0.5 * max(0.0, (a2 / b2) - p_eq) * q2_eq if q2_eq > 0 else 0.0

    # PS — треугольник от p_eq до минимальной цены продавца -c/d (может быть < 0).
    ps_min = -c / d
    ps = 0.5 * (p_eq - ps_min) * q_eq

    return {
        "p_eq": round(p_eq, 6),
        "q_eq": round(q_eq, 6),
        "q1_eq": round(q1_eq, 6),
        "q2_eq": round(q2_eq, 6),
        "cs1": round(cs1, 6),
        "cs2": round(cs2, 6),
        "ps": round(ps, 6),
    }

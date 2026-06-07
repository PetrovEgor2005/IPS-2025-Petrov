from __future__ import annotations
from typing import Any


def solve_gov_price_support(params: dict[str, Any]) -> dict[str, float]:
    # Государственная поддержка цены: цена выше равновесной, государство
    # выкупает весь избыток предложения.
    a = float(params["a"])
    b = float(params["b"])
    c = float(params["c"])
    d = float(params["d"])
    p_support = float(params["p_support"])
    if b <= 0:
        raise ValueError("b must be positive")
    if d <= 0:
        raise ValueError("d must be positive")

    # Равновесие без вмешательств
    p_eq = (a - c) / (b + d)
    q_eq = a - b * p_eq
    if p_support <= p_eq:
        raise ValueError("p_support must be above free market equilibrium (binding floor)")

    # Спрос и предложение при новых мерах
    qd = a - b * p_support
    qs = c + d * p_support
    if qd <= 0:
        raise ValueError("qd must be positive")
    if qs <= 0:
        raise ValueError("qs must be positive")
    gov_purchase = qs - qd
    gov_expenditure = gov_purchase * p_support

    # Излишки при цене новой
    cs = 0.5 * (a / b - p_support) * qd
    ps = 0.5 * (p_support + c / d) * qs

    # Излишки при рынке, когда нет вмешательства
    cs_free = 0.5 * (a / b - p_eq) * q_eq
    ps_free = 0.5 * (p_eq + c / d) * q_eq

    # потеря мёрвого груза 
    dwl = (cs_free + ps_free) - (cs + ps - gov_expenditure)
    return {
        "qd": round(qd, 6),
        "qs": round(qs, 6),
        "gov_purchase": round(gov_purchase, 6),
        "gov_expenditure": round(gov_expenditure, 6),
        "cs": round(cs, 6),
        "ps": round(ps, 6),
        "dwl": round(dwl, 6),
    }

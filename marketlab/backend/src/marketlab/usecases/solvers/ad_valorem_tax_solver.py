from __future__ import annotations

from typing import Any


def solve_ad_valorem_tax(params: dict[str, Any]) -> dict[str, float]:
    # Адвалорный (процентный) налог на продавцов: распределение бремени, поступления, DWL.
    a = float(params["a"])
    b = float(params["b"])
    c = float(params["c"])
    d = float(params["d"])
    tau = float(params["tau"])

    if b <= 0:
        raise ValueError("b must be positive")
    if d <= 0:
        raise ValueError("d must be positive")
    if not (0 < tau < 1):
        raise ValueError("tau must be between 0 and 1 (exclusive)")

    # Равновесие без налога
    p0 = (a - c) / (b + d)
    q0 = a - b * p0

    # При налоге tau с продавцов: предложение становится Qs = c + d*(1-tau)*P_buyer.
    # Из a - b*P = c + d*(1-tau)*P получаем P_buyer = (a-c) / (b + d*(1-tau)).
    p_buyer = (a - c) / (b + d * (1 - tau))
    p_seller = (1 - tau) * p_buyer
    q_new = a - b * p_buyer

    if q_new <= 0:
        raise ValueError("Q_new must be positive (tax too large)")

    tax_per_unit = p_buyer - p_seller  # = tau * p_buyer
    tax_revenue = tax_per_unit * q_new

    # Излишки
    cs_before = 0.5 * (a / b - p0) * q0
    ps_before = 0.5 * (p0 + c / d) * q0
    cs_after = 0.5 * (a / b - p_buyer) * q_new
    ps_after = 0.5 * (p_seller + c / d) * q_new

    dwl = cs_before + ps_before - cs_after - ps_after - tax_revenue

    # Распределение налогового бремени
    buyer_share = (p_buyer - p0) / tax_per_unit
    seller_share = (p0 - p_seller) / tax_per_unit

    return {
        "p_buyer": round(p_buyer, 6),
        "p_seller": round(p_seller, 6),
        "q_new": round(q_new, 6),
        "tax_revenue": round(tax_revenue, 6),
        "cs_after": round(cs_after, 6),
        "ps_after": round(ps_after, 6),
        "dwl": round(dwl, 6),
        "buyer_share": round(buyer_share, 6),
        "seller_share": round(seller_share, 6),
    }

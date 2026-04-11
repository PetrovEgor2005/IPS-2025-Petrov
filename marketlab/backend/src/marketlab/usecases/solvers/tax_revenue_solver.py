from __future__ import annotations
from marketlab.domain.tasks import Params, Result


def solve_tax_revenue(params: Params) -> Result:
    a = float(params["a"])
    b = float(params["b"])
    c = float(params["c"])
    d = float(params["d"])
    t = float(params["t"])
    denom = b + d
    p0 = (a - c) / denom
    q0 = a - b * p0
    p_buyer = (a - c + d * t) / denom
    p_seller = p_buyer - t
    q_tax = a - b * p_buyer
    tax_revenue = t * q_tax
    price_increase = p_buyer - p0
    quantity_decrease = q0 - q_tax

    return {
        "p_buyer": p_buyer,
        "p_seller": p_seller,
        "q_tax": q_tax,
        "tax_revenue": tax_revenue,
        "price_increase": price_increase,
        "quantity_decrease": quantity_decrease,
    }

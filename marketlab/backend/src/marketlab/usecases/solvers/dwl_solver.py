
"""
Данный солвер предназначен для решения задачи с потерей благосостояния,
основным моментом является сравнение общего благосостояния до и после введения налога или субсидии.
"""

from __future__ import annotations
from marketlab.domain.tasks import Params, Result


def solve_dwl(params: Params) -> Result:
    a = float(params["a"])
    b = float(params["b"])
    c = float(params["c"])
    d = float(params["d"])
    t = float(params["t"])
    mode = params["mode"]
    if t <= 0:
        raise ValueError("t must be positive")
    if mode not in ("tax", "subsidy"):
        raise ValueError("mode must be 'tax' or 'subsidy'")
    denom = b + d
    p0 = (a - c) / denom
    q0 = a - b * p0
    p_max_demand = a / b
    p_min_supply = -c / d
    cs_before = 0.5 * (p_max_demand - p0) * q0
    ps_before = 0.5 * (p0 - p_min_supply) * q0
    total_before = cs_before + ps_before
    if mode == "tax":
        p_buyer = (a - c + d * t) / denom
        p_seller = p_buyer - t
    else:
        p_buyer = (a - c - d * t) / denom
        p_seller = p_buyer + t

    q_new = a - b * p_buyer
    cs_after = 0.5 * (p_max_demand - p_buyer) * q_new
    ps_after = 0.5 * (p_seller - p_min_supply) * q_new
    if mode == "tax":
        gov_balance = t * q_new
    else:
        gov_balance = -t * q_new

    total_after = cs_after + ps_after + gov_balance
    dwl = total_before - total_after
    buyer_burden = abs(p_buyer - p0)
    seller_burden = abs(p0 - p_seller)
    buyer_share = buyer_burden / t
    seller_share = seller_burden / t

    return {
        "p_buyer": p_buyer,
        "p_seller": p_seller,
        "q_new": q_new,
        "cs_after": cs_after,
        "ps_after": ps_after,
        "gov_balance": gov_balance,
        "dwl": dwl,
        "buyer_share": buyer_share,
        "seller_share": seller_share,
    }

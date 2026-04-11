from __future__ import annotations
from marketlab.domain.tasks import Params, Result


def solve_price_ceiling(params: Params) -> Result:
    a = float(params["a"])
    b = float(params["b"])
    c = float(params["c"])
    d = float(params["d"])
    p_ceil = float(params["p_ceil"])
    p_eq = (a - c) / (b + d)
    q_eq = a - b * p_eq
    if p_ceil >= p_eq:
        return {
            "p_actual": p_eq,
            "q_demanded": q_eq,
            "q_supplied": q_eq,
            "q_traded": q_eq,
            "shortage": 0.0,
            "binding": 0.0,
        }
    q_demanded = a - b * p_ceil
    q_supplied = c + d * p_ceil
    q_traded = q_supplied
    shortage = q_demanded - q_supplied

    return {
        "p_actual": p_ceil,
        "q_demanded": q_demanded,
        "q_supplied": q_supplied,
        "q_traded": q_traded,
        "shortage": shortage,
        "binding": 1.0,
    }

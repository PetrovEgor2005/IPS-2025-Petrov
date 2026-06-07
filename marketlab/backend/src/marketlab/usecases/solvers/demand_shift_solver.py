from __future__ import annotations

from marketlab.domain.tasks import Params, Result


def solve_demand_shift(params: Params) -> Result:
    a = float(params["a"])
    b = float(params["b"])
    c = float(params["c"])
    d = float(params["d"])
    a_new = float(params["a_new"])
    denom = b + d
    p_old = (a - c) / denom
    q_old = a - b * p_old
    p_new = (a_new - c) / denom
    q_new = a_new - b * p_new
    delta_p = p_new - p_old
    delta_q = q_new - q_old

    return {
        "p_old": p_old,
        "q_old": q_old,
        "p_new": p_new,
        "q_new": q_new,
        "delta_p": delta_p,
        "delta_q": delta_q,
    }

from __future__ import annotations
from marketlab.domain.tasks import Params, Result


def solve_surplus(params: Params) -> Result:
    a = float(params["a"])
    b = float(params["b"])
    c = float(params["c"])
    d = float(params["d"])
    p_eq = (a - c) / (b + d)
    q_eq = a - b * p_eq
    p_max = a / b
    p_min = -c / d
    cs = 0.5 * (p_max - p_eq) * q_eq
    ps = 0.5 * (p_eq - p_min) * q_eq
    total_surplus = cs + ps

    return {"cs": cs, "ps": ps, "total_surplus": total_surplus}

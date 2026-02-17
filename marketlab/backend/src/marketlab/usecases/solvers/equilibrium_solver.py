from __future__ import annotations

from marketlab.domain.equilibrium import compute_equilibrium
from marketlab.domain.models import LinearDemand, LinearSupply, MarketPolicy
from marketlab.domain.tasks import Params, Result


def solve_equilibrium_linear(params: Params) -> Result:
    """
    Solver for task: linear equilibrium with optional per-unit tax/subsidy.

    Expected input keys:
      a, b, c, d, mode, t
    Returns:
      p_eq, q_eq
    """
    a = float(params["a"])
    b = float(params["b"])
    c = float(params["c"])
    d = float(params["d"])
    mode = str(params["mode"])
    t = float(params.get("t", 0.0))

    demand = LinearDemand(a=a, b=b)
    supply = LinearSupply(c=c, d=d)
    policy = MarketPolicy(mode=mode, t=t if mode != "none" else 0.0)

    eq = compute_equilibrium(demand, supply, policy)

    return {
        "p_eq": eq.p,
        "q_eq": eq.q,
    }

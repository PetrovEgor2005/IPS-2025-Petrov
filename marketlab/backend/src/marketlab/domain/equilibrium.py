from __future__ import annotations
from dataclasses import dataclass
from .errors import NoEquilibriumError
from .models import LinearDemand, LinearSupply, MarketPolicy


@dataclass(frozen=True, slots=True)
class Equilibrium:
    p: float
    q: float


def compute_equilibrium(
    demand: LinearDemand,
    supply: LinearSupply,
    policy: MarketPolicy,
) -> Equilibrium:
    """
    Solves market equilibrium under a per-unit policy wedge on producers.

    Consumer price = P
    Producer price = Pp = policy.producer_price(P)

    Equilibrium condition:
        Qd(P) = Qs(Pp)
    where:
        Qd(P) = a - bP
        Qs(Pp) = c + d*Pp
    """
    a, b = demand.a, demand.b
    c, d = supply.c, supply.d
    t = policy.t

    # Solve: a - bP = c + d*(P - t)  for tax
    #        a - bP = c + d*(P + t)  for subsidy
    #        a - bP = c + d*P        for none
    if policy.mode == "none":
        denom = b + d
        p = (a - c) / denom
    elif policy.mode == "tax":
        denom = b + d
        p = (a - c + d * t) / denom
    else:  # subsidy
        denom = b + d
        p = (a - c - d * t) / denom

    q = demand.quantity(p)

    if p <= 0 or q <= 0:
        raise NoEquilibriumError("Equilibrium must satisfy P*>0 and Q*>0 for this task family.")

    return Equilibrium(p=p, q=q)

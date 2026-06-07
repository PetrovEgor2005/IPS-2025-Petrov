"""
В данном файле рассчитывается равновесие при заданных уравнениях кривых спроса и предложения,
поддерживаются параметры для налога и субсидий.
Также проверяются параметры, что при таких значениях коэффициентов кривых будет найдено равновесие, 
иначе получаем исключение NoEquilibriumError
"""


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
    a, b = demand.a, demand.b
    c, d = supply.c, supply.d
    t = policy.t
    if policy.mode == "none":
        denom = b + d
        p = (a - c) / denom
    elif policy.mode == "tax":
        denom = b + d
        p = (a - c + d * t) / denom
    else:
        denom = b + d
        p = (a - c - d * t) / denom

    q = demand.quantity(p)

    if p <= 0 or q <= 0:
        raise NoEquilibriumError("Equilibrium must satisfy P*>0 and Q*>0 for this task family.")

    return Equilibrium(p=p, q=q)

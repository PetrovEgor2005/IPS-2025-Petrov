"""
В данном файле представлено решение задачи нахождения рыночного равновесия для линейных функций спроса и предложения
Солвер достаёт параметры, строит доменные объекты, вызывает функцию compute_equilibrium и возвращает результат в виде словаря с равновесной ценой и количеством
"""


from __future__ import annotations
from marketlab.domain.equilibrium import compute_equilibrium
from marketlab.domain.models import LinearDemand, LinearSupply, MarketPolicy
from marketlab.domain.tasks import Params, Result


def solve_equilibrium_linear(params: Params) -> Result:
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

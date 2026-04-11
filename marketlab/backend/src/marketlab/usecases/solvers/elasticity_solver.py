from __future__ import annotations
from marketlab.domain.tasks import Params, Result


def solve_elasticity(params: Params) -> Result:
    a = float(params["a"])
    b = float(params["b"])
    p = float(params["p"])
    q = a - b * p
    elasticity = (-b) * (p / q)
    revenue = p * q
    abs_e = abs(elasticity)
    if abs_e > 1.0001:
        elastic_type = 1.0
    elif abs_e < 0.9999:
        elastic_type = -1.0
    else:
        elastic_type = 0.0

    return {"elasticity": elasticity, "revenue": revenue, "elastic_type": elastic_type}

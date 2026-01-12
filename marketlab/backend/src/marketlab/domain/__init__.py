"""
Domain layer for MarketLab.

Contains pure economic models and rules:
- demand and supply functions
- market policies
- equilibrium computation
- domain-level errors

This layer must not depend on:
- FastAPI
- databases
- infrastructure code
"""

from .errors import (
    DomainError,
    InvalidParameterError,
    NoEquilibriumError,
)
from .models import (
    LinearDemand,
    LinearSupply,
    MarketPolicy,
)
from .equilibrium import (
    Equilibrium,
    compute_equilibrium,
)

__all__ = [
    # errors
    "DomainError",
    "InvalidParameterError",
    "NoEquilibriumError",
    # models
    "LinearDemand",
    "LinearSupply",
    "MarketPolicy",
    # services
    "Equilibrium",
    "compute_equilibrium",
]

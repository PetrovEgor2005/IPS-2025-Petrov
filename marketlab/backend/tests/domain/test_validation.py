import pytest

from marketlab.domain.errors import InvalidParameterError, NoEquilibriumError
from marketlab.domain.equilibrium import compute_equilibrium
from marketlab.domain.models import LinearDemand, LinearSupply, MarketPolicy


def test_invalid_demand():
    with pytest.raises(InvalidParameterError):
        LinearDemand(a=0, b=1)

    with pytest.raises(InvalidParameterError):
        LinearDemand(a=10, b=0)


def test_invalid_supply():
    with pytest.raises(InvalidParameterError):
        LinearSupply(c=0, d=0)


def test_invalid_policy_none_requires_t_zero():
    with pytest.raises(InvalidParameterError):
        MarketPolicy(mode="none", t=5)


def test_no_equilibrium_when_negative_price_or_quantity():
    dmd = LinearDemand(a=1, b=10)
    spl = LinearSupply(c=100, d=1)
    policy = MarketPolicy(mode="none", t=0)

    with pytest.raises(NoEquilibriumError):
        compute_equilibrium(dmd, spl, policy)

import pytest

from marketlab.domain.equilibrium import compute_equilibrium
from marketlab.domain.models import LinearDemand, LinearSupply, MarketPolicy


def test_equilibrium_none():
    dmd = LinearDemand(a=120, b=3)
    spl = LinearSupply(c=-10, d=2)
    policy = MarketPolicy(mode="none", t=0)

    eq = compute_equilibrium(dmd, spl, policy)
    assert eq.p == pytest.approx(26.0)
    assert eq.q == pytest.approx(42.0)


def test_equilibrium_tax_example_from_readme():
    dmd = LinearDemand(a=120, b=3)
    spl = LinearSupply(c=-10, d=2)
    policy = MarketPolicy(mode="tax", t=10)

    eq = compute_equilibrium(dmd, spl, policy)
    assert eq.p == pytest.approx(30.0)
    assert eq.q == pytest.approx(30.0)


def test_equilibrium_subsidy():
    dmd = LinearDemand(a=120, b=3)
    spl = LinearSupply(c=-10, d=2)
    policy = MarketPolicy(mode="subsidy", t=10)

    eq = compute_equilibrium(dmd, spl, policy)
    # subsidy should lower consumer price vs none
    assert eq.p < 26.0
    assert eq.q > 42.0

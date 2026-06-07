"""Тесты для каждого солвера из реестра задач."""

import pytest

from marketlab.usecases.solvers.ad_valorem_tax_solver import solve_ad_valorem_tax
from marketlab.usecases.solvers.demand_aggregation_solver import solve_demand_aggregation
from marketlab.usecases.solvers.demand_shift_solver import solve_demand_shift
from marketlab.usecases.solvers.dwl_solver import solve_dwl
from marketlab.usecases.solvers.elasticity_solver import solve_elasticity
from marketlab.usecases.solvers.gov_price_support_solver import solve_gov_price_support
from marketlab.usecases.solvers.income_elasticity_solver import solve_income_elasticity
from marketlab.usecases.solvers.laffer_commodity_solver import solve_laffer_commodity
from marketlab.usecases.solvers.monopoly_solver import solve_monopoly
from marketlab.usecases.solvers.pigouvian_tax_solver import solve_pigouvian_tax
from marketlab.usecases.solvers.price_ceiling_solver import solve_price_ceiling
from marketlab.usecases.solvers.price_floor_solver import solve_price_floor
from marketlab.usecases.solvers.revenue_max_solver import solve_revenue_max
from marketlab.usecases.solvers.simultaneous_shift_solver import solve_simultaneous_shift
from marketlab.usecases.solvers.supply_shift_solver import solve_supply_shift
from marketlab.usecases.solvers.surplus_solver import solve_surplus
from marketlab.usecases.solvers.tax_revenue_solver import solve_tax_revenue
from marketlab.usecases.solvers.trade_tariff_solver import solve_trade_tariff
from marketlab.usecases.solvers.welfare_supply_improvement_solver import (
    solve_welfare_supply_improvement,
)

# Базовый рынок: Qd = 120 - 3P, Qs = -10 + 2P  →  P* = 26, Q* = 42
BASE = {"a": 120.0, "b": 3.0, "c": -10.0, "d": 2.0}


class TestSurplusSolver:
    # p_max = 120/3 = 40, p_min = 10/2 = 5, p_eq=26, q_eq=42
    # CS = 0.5*(40-26)*42 = 294, PS = 0.5*(26-5)*42 = 441, TS = 735

    def test_basic_values(self):
        result = solve_surplus(BASE)
        assert result["cs"] == pytest.approx(294.0)
        assert result["ps"] == pytest.approx(441.0)
        assert result["total_surplus"] == pytest.approx(735.0)

    def test_total_surplus_equals_cs_plus_ps(self):
        result = solve_surplus(BASE)
        assert result["total_surplus"] == pytest.approx(result["cs"] + result["ps"])

    def test_returns_required_keys(self):
        result = solve_surplus(BASE)
        assert set(result.keys()) == {"cs", "ps", "total_surplus"}

    def test_cs_and_ps_are_positive(self):
        result = solve_surplus(BASE)
        assert result["cs"] > 0
        assert result["ps"] > 0


class TestDwlSolver:
    # Налог t=10: p_buyer=30, p_seller=20, q_new=30
    # CS_after=150, PS_after=225, gov_balance=300
    # total_before=735, total_after=675, DWL=60
    # buyer_burden=4, seller_burden=6  → buyer_share=0.4, seller_share=0.6

    TAX_PARAMS = {**BASE, "t": 10.0, "mode": "tax"}

    def test_tax_prices(self):
        result = solve_dwl(self.TAX_PARAMS)
        assert result["p_buyer"] == pytest.approx(30.0)
        assert result["p_seller"] == pytest.approx(20.0)

    def test_tax_quantity(self):
        result = solve_dwl(self.TAX_PARAMS)
        assert result["q_new"] == pytest.approx(30.0)

    def test_tax_surplus_components(self):
        result = solve_dwl(self.TAX_PARAMS)
        assert result["cs_after"] == pytest.approx(150.0)
        assert result["ps_after"] == pytest.approx(225.0)
        assert result["gov_balance"] == pytest.approx(300.0)

    def test_tax_dwl(self):
        result = solve_dwl(self.TAX_PARAMS)
        assert result["dwl"] == pytest.approx(60.0)

    def test_tax_burden_shares_sum_to_one(self):
        result = solve_dwl(self.TAX_PARAMS)
        assert result["buyer_share"] + result["seller_share"] == pytest.approx(1.0)

    def test_tax_burden_split(self):
        result = solve_dwl(self.TAX_PARAMS)
        assert result["buyer_share"] == pytest.approx(0.4)
        assert result["seller_share"] == pytest.approx(0.6)

    def test_subsidy_gov_balance_is_negative(self):
        params = {**BASE, "t": 10.0, "mode": "subsidy"}
        result = solve_dwl(params)
        # Субсидия: государство платит, поэтому gov_balance < 0.
        assert result["gov_balance"] < 0
        assert result["gov_balance"] == pytest.approx(-10.0 * result["q_new"])
        assert result["p_buyer"] < 26.0  # цена для покупателей падает

    def test_returns_required_keys(self):
        result = solve_dwl(self.TAX_PARAMS)
        assert set(result.keys()) == {
            "p_buyer",
            "p_seller",
            "q_new",
            "cs_after",
            "ps_after",
            "gov_balance",
            "dwl",
            "buyer_share",
            "seller_share",
        }


class TestElasticitySolver:
    # Qd = 120 - 3P, b=3

    def test_elastic_demand(self):
        # При p=26, q=42: Ed = -3*(26/42) ≈ -1.857 → эластичный спрос
        params = {**BASE, "p": 26.0}
        result = solve_elasticity(params)
        assert result["elasticity"] == pytest.approx(-3 * 26 / 42)
        assert result["elastic_type"] == pytest.approx(1.0)

    def test_inelastic_demand(self):
        # При p=10, q=90: Ed = -3*(10/90) ≈ -0.333 → неэластичный спрос
        params = {**BASE, "p": 10.0}
        result = solve_elasticity(params)
        assert result["elasticity"] == pytest.approx(-3 * 10 / 90)
        assert result["elastic_type"] == pytest.approx(-1.0)

    def test_unit_elastic_demand(self):
        # При p = a/(2b) = 120/6 = 20, q=60: Ed = -3*(20/60) = -1.0 → единичная эластичность
        params = {**BASE, "p": 20.0}
        result = solve_elasticity(params)
        assert result["elasticity"] == pytest.approx(-1.0)
        assert result["elastic_type"] == pytest.approx(0.0)

    def test_revenue(self):
        params = {**BASE, "p": 26.0}
        result = solve_elasticity(params)
        assert result["revenue"] == pytest.approx(26.0 * 42.0)

    def test_returns_required_keys(self):
        params = {**BASE, "p": 26.0}
        result = solve_elasticity(params)
        assert set(result.keys()) == {"elasticity", "revenue", "elastic_type"}


class TestPriceCeilingSolver:
    # p_eq=26, q_eq=42

    def test_binding_ceiling(self):
        # p_ceil=20 < p_eq=26 → потолок действует, возникает дефицит
        params = {**BASE, "p_ceil": 20.0}
        result = solve_price_ceiling(params)
        assert result["p_actual"] == pytest.approx(20.0)
        assert result["q_demanded"] == pytest.approx(60.0)  # 120 - 3*20
        assert result["q_supplied"] == pytest.approx(30.0)  # -10 + 2*20
        assert result["q_traded"] == pytest.approx(30.0)
        assert result["shortage"] == pytest.approx(30.0)
        assert result["binding"] == pytest.approx(1.0)

    def test_non_binding_ceiling(self):
        # p_ceil=30 > p_eq=26 → потолок не действует, рынок в равновесии
        params = {**BASE, "p_ceil": 30.0}
        result = solve_price_ceiling(params)
        assert result["p_actual"] == pytest.approx(26.0)
        assert result["q_demanded"] == pytest.approx(42.0)
        assert result["q_supplied"] == pytest.approx(42.0)
        assert result["shortage"] == pytest.approx(0.0)
        assert result["binding"] == pytest.approx(0.0)

    def test_ceiling_at_equilibrium_is_not_binding(self):
        params = {**BASE, "p_ceil": 26.0}
        result = solve_price_ceiling(params)
        assert result["binding"] == pytest.approx(0.0)

    def test_returns_required_keys(self):
        params = {**BASE, "p_ceil": 20.0}
        result = solve_price_ceiling(params)
        assert set(result.keys()) == {
            "p_actual",
            "q_demanded",
            "q_supplied",
            "q_traded",
            "shortage",
            "binding",
        }


class TestTaxRevenueSolver:
    # t=10: p_buyer=30, p_seller=20, q_tax=30
    # tax_revenue=300, price_increase=4, quantity_decrease=12

    TAX_PARAMS = {**BASE, "t": 10.0}

    def test_prices(self):
        result = solve_tax_revenue(self.TAX_PARAMS)
        assert result["p_buyer"] == pytest.approx(30.0)
        assert result["p_seller"] == pytest.approx(20.0)

    def test_quantity_and_revenue(self):
        result = solve_tax_revenue(self.TAX_PARAMS)
        assert result["q_tax"] == pytest.approx(30.0)
        assert result["tax_revenue"] == pytest.approx(300.0)

    def test_price_and_quantity_changes(self):
        result = solve_tax_revenue(self.TAX_PARAMS)
        assert result["price_increase"] == pytest.approx(4.0)
        assert result["quantity_decrease"] == pytest.approx(12.0)

    def test_tax_revenue_equals_t_times_q(self):
        result = solve_tax_revenue(self.TAX_PARAMS)
        assert result["tax_revenue"] == pytest.approx(10.0 * result["q_tax"])

    def test_returns_required_keys(self):
        result = solve_tax_revenue(self.TAX_PARAMS)
        assert set(result.keys()) == {
            "p_buyer",
            "p_seller",
            "q_tax",
            "tax_revenue",
            "price_increase",
            "quantity_decrease",
        }


class TestDemandShiftSolver:
    # a_new=140: p_new=(140+10)/5=30, q_new=140-3*30=50
    # delta_p=4, delta_q=8

    SHIFT_PARAMS = {**BASE, "a_new": 140.0}

    def test_old_equilibrium(self):
        result = solve_demand_shift(self.SHIFT_PARAMS)
        assert result["p_old"] == pytest.approx(26.0)
        assert result["q_old"] == pytest.approx(42.0)

    def test_new_equilibrium(self):
        result = solve_demand_shift(self.SHIFT_PARAMS)
        assert result["p_new"] == pytest.approx(30.0)
        assert result["q_new"] == pytest.approx(50.0)

    def test_deltas(self):
        result = solve_demand_shift(self.SHIFT_PARAMS)
        assert result["delta_p"] == pytest.approx(4.0)
        assert result["delta_q"] == pytest.approx(8.0)

    def test_demand_decrease_shifts_down(self):
        params = {**BASE, "a_new": 100.0}
        result = solve_demand_shift(params)
        assert result["p_new"] < result["p_old"]
        assert result["q_new"] < result["q_old"]
        assert result["delta_p"] < 0
        assert result["delta_q"] < 0

    def test_delta_equals_new_minus_old(self):
        result = solve_demand_shift(self.SHIFT_PARAMS)
        assert result["delta_p"] == pytest.approx(result["p_new"] - result["p_old"])
        assert result["delta_q"] == pytest.approx(result["q_new"] - result["q_old"])

    def test_returns_required_keys(self):
        result = solve_demand_shift(self.SHIFT_PARAMS)
        assert set(result.keys()) == {"p_old", "q_old", "p_new", "q_new", "delta_p", "delta_q"}


class TestPriceFloorSolver:
    # p_eq = 26, q_eq = 42
    def test_binding_floor(self):
        # p_floor = 30 > p_eq → пол действует; q_supplied > q_demanded → избыток
        r = solve_price_floor({**BASE, "p_floor": 30.0})
        assert r["binding"] == 1.0
        assert r["p_actual"] == pytest.approx(30.0)
        assert r["q_demanded"] == pytest.approx(30.0)  # 120 - 3*30
        assert r["q_supplied"] == pytest.approx(50.0)  # -10 + 2*30
        assert r["q_traded"] == pytest.approx(30.0)
        assert r["surplus_qty"] == pytest.approx(20.0)

    def test_non_binding_floor(self):
        r = solve_price_floor({**BASE, "p_floor": 20.0})
        assert r["binding"] == 0.0
        assert r["p_actual"] == pytest.approx(26.0)
        assert r["surplus_qty"] == pytest.approx(0.0)


class TestSupplyShiftSolver:
    def test_rightward_shift_lowers_price(self):
        # c_new = 40 (было -10): предложение сдвигается вправо → цена падает, объём растёт
        r = solve_supply_shift({**BASE, "c_new": 40.0})
        assert r["p_old"] == pytest.approx(26.0)
        assert r["p_new"] < r["p_old"]
        assert r["q_new"] > r["q_old"]


class TestIncomeElasticitySolver:
    def test_normal_good(self):
        # q1=100, q2=110, i1=2000, i2=2500: q растёт слабо → 0 < E < 1 → нормальное, не роскошь
        r = solve_income_elasticity({"q1": 100, "i1": 2000, "q2": 110, "i2": 2500})
        assert r["income_elasticity"] > 0
        assert r["income_elasticity"] < 1
        assert r["is_normal"] == 1.0
        assert r["is_luxury"] == 0.0

    def test_luxury_good(self):
        # Большой скачок q при малом росте дохода → E > 1 → товар-роскошь
        r = solve_income_elasticity({"q1": 50, "i1": 2000, "q2": 150, "i2": 2200})
        assert r["income_elasticity"] > 1
        assert r["is_luxury"] == 1.0

    def test_inferior_good(self):
        r = solve_income_elasticity({"q1": 100, "i1": 2000, "q2": 80, "i2": 2500})
        assert r["income_elasticity"] < 0
        assert r["is_normal"] == -1.0
        assert r["is_luxury"] == 0.0

    def test_zero_change_is_neither(self):
        r = solve_income_elasticity({"q1": 100, "i1": 2000, "q2": 100, "i2": 2500})
        assert r["income_elasticity"] == pytest.approx(0.0)
        assert r["is_normal"] == 0.0


class TestDemandAggregationSolver:
    def test_both_consumers_active(self):
        # Цены насыщения обоих потребителей выше равновесия → сегмент 1 (оба активны)
        r = solve_demand_aggregation({"a1": 100, "b1": 2, "a2": 80, "b2": 1.5, "c": 10, "d": 2})
        assert r["q1_eq"] > 0
        assert r["q2_eq"] > 0
        assert r["q_eq"] == pytest.approx(r["q1_eq"] + r["q2_eq"])

    def test_low_choke_consumer_drops_out(self):
        # a1/b1 = 30/3 = 10 — низкая цена насыщения; предложение крутое → равновесие выше порога потребителя 1
        r = solve_demand_aggregation({"a1": 30, "b1": 3, "a2": 200, "b2": 1, "c": 0, "d": 2})
        assert r["q1_eq"] == 0.0 or r["q2_eq"] == 0.0
        assert r["q_eq"] > 0


class TestMonopolySolver:
    def test_basic(self):
        # A=100, B=2, mc=20 → Q_m=(100-20)/4=20, P_m=(100+20)/2=60
        r = solve_monopoly({"A": 100, "B": 2, "mc": 20})
        assert r["q_monopoly"] == pytest.approx(20.0)
        assert r["p_monopoly"] == pytest.approx(60.0)
        assert r["q_competitive"] == pytest.approx(40.0)
        assert r["p_competitive"] == pytest.approx(20.0)
        # profit = (60-20)*20 = 800
        assert r["profit"] == pytest.approx(800.0)
        # DWL = 0.5 * (60-20) * (40-20) = 400
        assert r["dwl"] == pytest.approx(400.0)

    def test_rejects_unviable_market(self):
        with pytest.raises(ValueError):
            solve_monopoly({"A": 10, "B": 1, "mc": 50})


class TestAdValoremTaxSolver:
    def test_basic_incidence(self):
        r = solve_ad_valorem_tax({"a": 200, "b": 3, "c": 10, "d": 2, "tau": 0.2})
        # Сумма долей покупателя и продавца = 1
        assert r["buyer_share"] + r["seller_share"] == pytest.approx(1.0, abs=1e-6)
        assert r["q_new"] > 0
        assert r["tax_revenue"] > 0
        assert r["dwl"] >= 0


class TestTradeTariffSolver:
    def test_basic_tariff(self):
        # цена автаркии = (300-20)/(4+3) = 40; p_world=30, тариф=5 — ниже порога закрытия рынка
        r = solve_trade_tariff({"a": 300, "b": 4, "c": 20, "d": 3, "p_world": 30, "tariff": 5})
        assert r["imports_free"] > r["imports_tariff"] > 0
        assert r["consumer_loss"] > 0
        assert r["producer_gain"] > 0
        assert r["tariff_revenue"] > 0
        assert r["dwl"] >= 0

    def test_autarky_cap(self):
        # Огромный тариф: внутренняя цена не может подняться выше автаркийного равновесия
        r = solve_trade_tariff({"a": 300, "b": 4, "c": 20, "d": 3, "p_world": 30, "tariff": 500})
        assert r["imports_tariff"] == pytest.approx(0.0)
        assert r["tariff_revenue"] == pytest.approx(0.0)


class TestPigouvianTaxSolver:
    def test_basic(self):
        r = solve_pigouvian_tax({"a": 200, "b": 4, "c": 20, "d": 2, "e": 5})
        assert r["q_social"] < r["q_market"]
        assert r["p_social"] > r["p_market"]
        assert r["pigouvian_tax"] == pytest.approx(5.0)
        assert r["dwl_without_tax"] >= 0


class TestSimultaneousShiftSolver:
    def test_both_curves_shift_right(self):
        # a_new > a (спрос вверх), c_new > c (предложение вправо): q растёт, p — неоднозначно
        r = solve_simultaneous_shift({"a": 200, "b": 3, "c": 10, "d": 2, "a_new": 250, "c_new": 30})
        assert r["q_new"] > r["q_old"]
        assert r["delta_q"] == pytest.approx(r["q_new"] - r["q_old"])


class TestGovPriceSupportSolver:
    def test_basic(self):
        r = solve_gov_price_support({"a": 200, "b": 2, "c": 20, "d": 3, "p_support": 55})
        assert r["gov_purchase"] > 0
        assert r["gov_expenditure"] == pytest.approx(r["gov_purchase"] * 55)
        assert r["dwl"] >= 0


class TestRevenueMaxSolver:
    def test_basic(self):
        # a=120, b=3 → p_opt = 20, q_opt = 60, tr_max = 1200
        r = solve_revenue_max({"a": 120, "b": 3, "p_current": 10})
        assert r["p_optimal"] == pytest.approx(20.0)
        assert r["q_optimal"] == pytest.approx(60.0)
        assert r["tr_max"] == pytest.approx(1200.0)
        # at p_current=10 → q=90, tr=900
        assert r["tr_current"] == pytest.approx(900.0)
        assert r["revenue_gain"] == pytest.approx(300.0)

    def test_elasticity_at_optimum_is_minus_one(self):
        r = solve_revenue_max({"a": 120, "b": 3, "p_current": 20})
        # at P_opt, |Ed| = 1
        assert r["ed_current"] == pytest.approx(-1.0)


class TestWelfareSupplyImprovementSolver:
    def test_basic(self):
        r = solve_welfare_supply_improvement({"a": 200, "b": 3, "c": 10, "d": 2, "c_new": 40})
        assert r["p_new"] < r["p_old"]
        assert r["delta_cs"] > 0
        assert r["delta_ts"] == pytest.approx(r["delta_cs"] + r["delta_ps"])


class TestLafferCommoditySolver:
    def test_basic(self):
        r = solve_laffer_commodity({"a": 200, "b": 3, "c": 10, "d": 2, "current_tax": 8})
        assert r["t_opt"] > 0
        assert r["revenue_max"] > 0
        # для линейной Q(t): t_prohibitive = 2 * t_opt
        assert r["t_prohibitive"] == pytest.approx(2 * r["t_opt"])


# ---------- Параметрический smoke: оракул работает для каждой зарегистрированной задачи ----------


@pytest.mark.parametrize(
    "task_id",
    [
        "equilibrium_linear_v1",
        "surplus_calc_v1",
        "dwl_tax_v1",
        "elasticity_v1",
        "price_ceiling_v1",
        "tax_revenue_v1",
        "demand_shift_v1",
        "price_floor_v1",
        "supply_shift_v1",
        "income_elasticity_v1",
        "demand_aggregation_v1",
        "monopoly_v1",
        "ad_valorem_tax_v1",
        "trade_tariff_v1",
        "pigouvian_tax_v1",
        "simultaneous_shift_v1",
        "gov_price_support_v1",
        "revenue_max_v1",
        "welfare_supply_improvement_v1",
        "laffer_commodity_v1",
    ],
)
def test_oracle_produces_valid_results_for_generated_tests(task_id):
    """Каждая задача реестра: 25 сгенерированных тестов, оракул возвращает задекларированные поля с конечными числами."""
    from marketlab.domain.generator import generate_tests
    from marketlab.usecases.registry import TASK_REGISTRY

    spec, oracle = TASK_REGISTRY[task_id]
    expected_keys = {f.name for f in spec.output_fields}

    tests = generate_tests(task_id, n=25, seed=42)
    assert len(tests) == 25

    for params in tests:
        result = oracle(params)
        assert set(result.keys()) == expected_keys
        for k, v in result.items():
            assert isinstance(v, (int, float)), f"{task_id} {k}={v!r} not numeric"
            assert v == v, f"{task_id} {k} is NaN"  # проверка на NaN (NaN != NaN)

from __future__ import annotations

from marketlab.domain.tasks import FieldSpec, TaskSpec
from marketlab.usecases.solvers import (
    solve_equilibrium_linear,
    solve_surplus,
    solve_dwl,
    solve_elasticity,
    solve_price_ceiling,
    solve_tax_revenue,
    solve_demand_shift,
)

EQUILIBRIUM_LINEAR = TaskSpec(
    id="equilibrium_linear_v1",
    title="Равновесие на конкурентном рынке",
    topic="equilibrium",
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("c", "float", "Параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
        FieldSpec("mode", "str", "Режим: none | tax | subsidy"),
        FieldSpec("t", "float", "Величина налога/субсидии"),
    ),
    output_fields=(
        FieldSpec("p_eq", "float", "Равновесная цена"),
        FieldSpec("q_eq", "float", "Равновесный объём"),
    ),
)

SURPLUS_CALC = TaskSpec(
    id="surplus_calc_v1",
    title="Излишки потребителя и производителя",
    topic="welfare",
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("c", "float", "Параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
    ),
    output_fields=(
        FieldSpec("cs", "float", "Потребительский излишек (CS)"),
        FieldSpec("ps", "float", "Производственный излишек (PS)"),
        FieldSpec("total_surplus", "float", "Общий излишек"),
    ),
)

DWL_TAX = TaskSpec(
    id="dwl_tax_v1",
    title="Потери благосостояния от налога",
    topic="welfare",
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("c", "float", "Параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
        FieldSpec("t", "float", "Размер налога или субсидии"),
        FieldSpec("mode", "str", "Режим: tax | subsidy"),
    ),
    output_fields=(
        FieldSpec("p_buyer", "float", "Цена покупателя"),
        FieldSpec("p_seller", "float", "Цена продавца"),
        FieldSpec("q_new", "float", "Объём после вмешательства"),
        FieldSpec("cs_after", "float", "CS после вмешательства"),
        FieldSpec("ps_after", "float", "PS после вмешательства"),
        FieldSpec("gov_revenue", "float", "Налоговые поступления"),
        FieldSpec("dwl", "float", "Потери благосостояния"),
        FieldSpec("buyer_share", "float", "Доля покупателя в бремени"),
        FieldSpec("seller_share", "float", "Доля продавца в бремени"),
    ),
)

ELASTICITY = TaskSpec(
    id="elasticity_v1",
    title="Эластичность спроса по цене",
    topic="elasticity",
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("p", "float", "Цена для расчёта эластичности"),
    ),
    output_fields=(
        FieldSpec("elasticity", "float", "Точечная эластичность (Ed)"),
        FieldSpec("revenue", "float", "Выручка (P * Q)"),
        FieldSpec("elastic_type", "float", "1=эластичный, -1=неэластичный, 0=единичная"),
    ),
)

PRICE_CEILING = TaskSpec(
    id="price_ceiling_v1",
    title="Потолок цены на рынке аренды",
    topic="equilibrium",
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("c", "float", "Параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
        FieldSpec("p_ceil", "float", "Потолок цены"),
    ),
    output_fields=(
        FieldSpec("p_actual", "float", "Фактическая цена"),
        FieldSpec("q_demanded", "float", "Объём спроса при данной цене"),
        FieldSpec("q_supplied", "float", "Объём предложения при данной цене"),
        FieldSpec("q_traded", "float", "Фактический объём сделок"),
        FieldSpec("shortage", "float", "Дефицит (Qd - Qs)"),
        FieldSpec("binding", "float", "1 если потолок действует, 0 если нет"),
    ),
)

TAX_REVENUE = TaskSpec(
    id="tax_revenue_v1",
    title="Налоговые поступления",
    topic="welfare",
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("c", "float", "Параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
        FieldSpec("t", "float", "Размер налога"),
    ),
    output_fields=(
        FieldSpec("p_buyer", "float", "Цена покупателя"),
        FieldSpec("p_seller", "float", "Цена продавца"),
        FieldSpec("q_tax", "float", "Объём с налогом"),
        FieldSpec("tax_revenue", "float", "Налоговые поступления"),
        FieldSpec("price_increase", "float", "Рост цены для покупателя"),
        FieldSpec("quantity_decrease", "float", "Сокращение объёма"),
    ),
)

DEMAND_SHIFT = TaskSpec(
    id="demand_shift_v1",
    title="Сдвиг кривой спроса",
    topic="equilibrium",
    input_fields=(
        FieldSpec("a", "float", "Старый параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("c", "float", "Параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
        FieldSpec("a_new", "float", "Новый параметр спроса после сдвига"),
    ),
    output_fields=(
        FieldSpec("p_old", "float", "Старая равновесная цена"),
        FieldSpec("q_old", "float", "Старый равновесный объём"),
        FieldSpec("p_new", "float", "Новая равновесная цена"),
        FieldSpec("q_new", "float", "Новый равновесный объём"),
        FieldSpec("delta_p", "float", "Изменение цены"),
        FieldSpec("delta_q", "float", "Изменение объёма"),
    ),
)


TASK_REGISTRY: dict[str, tuple[TaskSpec, object]] = {
    EQUILIBRIUM_LINEAR.id: (EQUILIBRIUM_LINEAR, solve_equilibrium_linear),
    SURPLUS_CALC.id: (SURPLUS_CALC, solve_surplus),
    DWL_TAX.id: (DWL_TAX, solve_dwl),
    ELASTICITY.id: (ELASTICITY, solve_elasticity),
    PRICE_CEILING.id: (PRICE_CEILING, solve_price_ceiling),
    TAX_REVENUE.id: (TAX_REVENUE, solve_tax_revenue),
    DEMAND_SHIFT.id: (DEMAND_SHIFT, solve_demand_shift),
}


def get_task_spec(task_id: str) -> TaskSpec:
    spec, _solver = TASK_REGISTRY[task_id]
    return spec


def solve_task(task_id: str, params: dict) -> dict[str, float]:
    spec, solver = TASK_REGISTRY[task_id]
    result = solver(params)
    expected = {f.name for f in spec.output_fields}
    got = set(result.keys())
    if got != expected:
        raise ValueError(f"Solver returned keys {sorted(got)}, expected {sorted(expected)}")
    return result

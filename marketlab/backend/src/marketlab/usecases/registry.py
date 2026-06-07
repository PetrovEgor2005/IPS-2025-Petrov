"""
В данном блоке кода собран каталог задач, каждая из задач представляет собой обьект класса TaskSpec,
которому передаётся основаня информация задаче, а именно, тема, названия, сложность, стандарт входных и 
выходных полей, является одним из пунктов этапа добавления новой задачи
"""



from __future__ import annotations
from marketlab.domain.tasks import FieldSpec, TaskSpec
from marketlab.usecases.solvers import (
    solve_ad_valorem_tax,
    solve_demand_aggregation,
    solve_demand_shift,
    solve_dwl,
    solve_elasticity,
    solve_equilibrium_linear,
    solve_gov_price_support,
    solve_income_elasticity,
    solve_laffer_commodity,
    solve_monopoly,
    solve_pigouvian_tax,
    solve_price_ceiling,
    solve_price_floor,
    solve_revenue_max,
    solve_simultaneous_shift,
    solve_supply_shift,
    solve_surplus,
    solve_tax_revenue,
    solve_trade_tariff,
    solve_welfare_supply_improvement,
)

EQUILIBRIUM_LINEAR = TaskSpec(
    id="equilibrium_linear_v1",
    title="Равновесие на конкурентном рынке",
    topic="equilibrium",
    difficulty=1,
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
    difficulty=2,
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
    difficulty=3,
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
        FieldSpec("gov_balance", "float", "Баланс государства (+налог / −субсидия)"),
        FieldSpec("dwl", "float", "Потери благосостояния"),
        FieldSpec("buyer_share", "float", "Доля покупателя в налоговом клине"),
        FieldSpec("seller_share", "float", "Доля продавца в налоговом клине"),
    ),
)

ELASTICITY = TaskSpec(
    id="elasticity_v1",
    title="Эластичность спроса по цене",
    topic="elasticity",
    difficulty=2,
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
    difficulty=2,
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
    title="Акциз на потребительский товар",
    topic="welfare",
    difficulty=2,
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
    difficulty=1,
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


PRICE_FLOOR = TaskSpec(
    id="price_floor_v1",
    title="Ценовой пол на рынке труда",
    topic="equilibrium",
    difficulty=2,
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("c", "float", "Параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
        FieldSpec("p_floor", "float", "Ценовой пол (минимальная цена)"),
    ),
    output_fields=(
        FieldSpec("p_actual", "float", "Фактическая цена"),
        FieldSpec("q_demanded", "float", "Объём спроса при данной цене"),
        FieldSpec("q_supplied", "float", "Объём предложения при данной цене"),
        FieldSpec("q_traded", "float", "Фактический объём сделок"),
        FieldSpec("surplus_qty", "float", "Избыток предложения (Qs - Qd)"),
        FieldSpec("binding", "float", "1 если пол действует, 0 если нет"),
    ),
)

SUPPLY_SHIFT = TaskSpec(
    id="supply_shift_v1",
    title="Сдвиг кривой предложения",
    topic="equilibrium",
    difficulty=1,
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("c", "float", "Старый параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
        FieldSpec("c_new", "float", "Новый параметр предложения после сдвига"),
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

INCOME_ELASTICITY = TaskSpec(
    id="income_elasticity_v1",
    title="Эластичность спроса по доходу",
    topic="elasticity",
    difficulty=2,
    input_fields=(
        FieldSpec("q1", "float", "Объём спроса при доходе i1"),
        FieldSpec("i1", "float", "Начальный доход"),
        FieldSpec("q2", "float", "Объём спроса при доходе i2"),
        FieldSpec("i2", "float", "Конечный доход"),
    ),
    output_fields=(
        FieldSpec("income_elasticity", "float", "Дуговая эластичность по доходу"),
        FieldSpec("is_normal", "float", "1 если нормальное благо, -1 если инфериорное"),
        FieldSpec("is_luxury", "float", "1 если предмет роскоши (E>1), иначе 0"),
    ),
)

DEMAND_AGGREGATION = TaskSpec(
    id="demand_aggregation_v1",
    title="Агрегирование рыночного спроса",
    topic="aggregation",
    difficulty=3,
    input_fields=(
        FieldSpec("a1", "float", "Параметр спроса потребителя 1: Qd1 = a1 - b1*P"),
        FieldSpec("b1", "float", "Наклон спроса потребителя 1 (b1>0)"),
        FieldSpec("a2", "float", "Параметр спроса потребителя 2: Qd2 = a2 - b2*P"),
        FieldSpec("b2", "float", "Наклон спроса потребителя 2 (b2>0)"),
        FieldSpec("c", "float", "Параметр предложения: Qs = c + d*P"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
    ),
    output_fields=(
        FieldSpec("p_eq", "float", "Равновесная цена"),
        FieldSpec("q_eq", "float", "Суммарный равновесный объём"),
        FieldSpec("q1_eq", "float", "Объём потребителя 1 в равновесии"),
        FieldSpec("q2_eq", "float", "Объём потребителя 2 в равновесии"),
        FieldSpec("cs1", "float", "Излишек потребителя 1"),
        FieldSpec("cs2", "float", "Излишек потребителя 2"),
        FieldSpec("ps", "float", "Излишек производителя"),
    ),
)

MONOPOLY = TaskSpec(
    id="monopoly_v1",
    title="Равновесие монополиста",
    topic="monopoly",
    difficulty=3,
    input_fields=(
        FieldSpec("A", "float", "Параметр обратного спроса: P = A - B*Q"),
        FieldSpec("B", "float", "Наклон обратного спроса (B>0)"),
        FieldSpec("mc", "float", "Постоянные предельные издержки (mc >= 0)"),
    ),
    output_fields=(
        FieldSpec("p_monopoly", "float", "Монопольная цена"),
        FieldSpec("q_monopoly", "float", "Монопольный объём"),
        FieldSpec("profit", "float", "Прибыль монополиста"),
        FieldSpec("cs", "float", "Потребительский излишек"),
        FieldSpec("p_competitive", "float", "Конкурентная цена (P = MC)"),
        FieldSpec("q_competitive", "float", "Конкурентный объём"),
        FieldSpec("dwl", "float", "Потери благосостояния (DWL)"),
    ),
)


AD_VALOREM_TAX = TaskSpec(
    id="ad_valorem_tax_v1",
    title="НДС на рынке электроники",
    topic="taxes_subsidies",
    difficulty=3,
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("c", "float", "Параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
        FieldSpec("tau", "float", "Ставка налога ad valorem (0 < tau < 1)"),
    ),
    output_fields=(
        FieldSpec("p_buyer", "float", "Цена покупателя"),
        FieldSpec("p_seller", "float", "Цена, получаемая продавцом"),
        FieldSpec("q_new", "float", "Объём с налогом"),
        FieldSpec("tax_revenue", "float", "Налоговые поступления"),
        FieldSpec("cs_after", "float", "CS после налога"),
        FieldSpec("ps_after", "float", "PS после налога"),
        FieldSpec("dwl", "float", "Потери благосостояния"),
        FieldSpec("buyer_share", "float", "Доля налогового бремени покупателя"),
        FieldSpec("seller_share", "float", "Доля налогового бремени продавца"),
    ),
)

TRADE_TARIFF = TaskSpec(
    id="trade_tariff_v1",
    title="Импортный тариф на бытовую технику",
    topic="trade",
    difficulty=3,
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("c", "float", "Параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
        FieldSpec("p_world", "float", "Мировая цена (p_world < P*)"),
        FieldSpec("tariff", "float", "Удельный тариф на импорт"),
    ),
    output_fields=(
        FieldSpec("imports_free", "float", "Объём импорта при свободной торговле"),
        FieldSpec("qs_tariff", "float", "Отечественное предложение с тарифом"),
        FieldSpec("qd_tariff", "float", "Отечественный спрос с тарифом"),
        FieldSpec("imports_tariff", "float", "Объём импорта с тарифом"),
        FieldSpec("tariff_revenue", "float", "Таможенные поступления"),
        FieldSpec("consumer_loss", "float", "Потери потребителей (CS_free − CS_tariff)"),
        FieldSpec("producer_gain", "float", "Выигрыш отечественных производителей"),
        FieldSpec("dwl", "float", "Чистые потери благосостояния"),
    ),
)

PIGOUVIAN_TAX = TaskSpec(
    id="pigouvian_tax_v1",
    title="Экологический налог на химический завод",
    topic="externality",
    difficulty=3,
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("c", "float", "Параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
        FieldSpec("e", "float", "Внешние издержки на единицу продукции (e>0)"),
    ),
    output_fields=(
        FieldSpec("p_market", "float", "Рыночная цена (без налога)"),
        FieldSpec("q_market", "float", "Рыночный объём (без налога)"),
        FieldSpec("p_social", "float", "Социально оптимальная цена"),
        FieldSpec("q_social", "float", "Социально оптимальный объём"),
        FieldSpec("pigouvian_tax", "float", "Оптимальный налог Пигу (= e)"),
        FieldSpec("external_damage", "float", "Суммарный внешний ущерб при рыночном объёме"),
        FieldSpec("dwl_without_tax", "float", "Потери благосостояния без налога"),
    ),
)

SIMULTANEOUS_SHIFT = TaskSpec(
    id="simultaneous_shift_v1",
    title="Рынок солнечных панелей: технологии и мода",
    topic="equilibrium",
    difficulty=3,
    input_fields=(
        FieldSpec("a", "float", "Старый параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("c", "float", "Старый параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
        FieldSpec("a_new", "float", "Новый параметр спроса после сдвига"),
        FieldSpec("c_new", "float", "Новый параметр предложения после сдвига"),
    ),
    output_fields=(
        FieldSpec("p_old", "float", "Старая равновесная цена"),
        FieldSpec("q_old", "float", "Старый равновесный объём"),
        FieldSpec("p_new", "float", "Новая равновесная цена"),
        FieldSpec("q_new", "float", "Новый равновесный объём"),
        FieldSpec("delta_p", "float", "Изменение цены"),
        FieldSpec("delta_q", "float", "Изменение объёма"),
        FieldSpec("delta_cs", "float", "Изменение потребительского излишка"),
        FieldSpec("delta_ps", "float", "Изменение производственного излишка"),
    ),
)

GOV_PRICE_SUPPORT = TaskSpec(
    id="gov_price_support_v1",
    title="Государственные закупки пшеницы",
    topic="welfare",
    difficulty=3,
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("c", "float", "Параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
        FieldSpec("p_support", "float", "Цена поддержки (p_support > P*)"),
    ),
    output_fields=(
        FieldSpec("qd", "float", "Спрос при цене поддержки"),
        FieldSpec("qs", "float", "Предложение при цене поддержки"),
        FieldSpec("gov_purchase", "float", "Объём государственных закупок"),
        FieldSpec("gov_expenditure", "float", "Расходы государства"),
        FieldSpec("cs", "float", "Потребительский излишек"),
        FieldSpec("ps", "float", "Производственный излишек (с учётом госзакупок)"),
        FieldSpec("dwl", "float", "Потери общественного благосостояния"),
    ),
)

REVENUE_MAX = TaskSpec(
    id="revenue_max_v1",
    title="Оптимальная цена авиабилетов",
    topic="elasticity",
    difficulty=2,
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("p_current", "float", "Текущая цена"),
    ),
    output_fields=(
        FieldSpec("p_optimal", "float", "Цена, максимизирующая выручку"),
        FieldSpec("q_optimal", "float", "Объём при оптимальной цене"),
        FieldSpec("tr_max", "float", "Максимальная выручка"),
        FieldSpec("tr_current", "float", "Текущая выручка"),
        FieldSpec("revenue_gain", "float", "Прирост выручки при переходе к P*"),
        FieldSpec("ed_current", "float", "Эластичность при текущей цене"),
    ),
)

WELFARE_SUPPLY_IMPROVEMENT = TaskSpec(
    id="welfare_supply_improvement_v1",
    title="Технический прогресс в производстве смартфонов",
    topic="welfare",
    difficulty=3,
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("c", "float", "Старый параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
        FieldSpec("c_new", "float", "Новый параметр предложения (c_new > c)"),
    ),
    output_fields=(
        FieldSpec("p_old", "float", "Старая равновесная цена"),
        FieldSpec("p_new", "float", "Новая равновесная цена"),
        FieldSpec("cs_old", "float", "CS до улучшения"),
        FieldSpec("cs_new", "float", "CS после улучшения"),
        FieldSpec("ps_old", "float", "PS до улучшения"),
        FieldSpec("ps_new", "float", "PS после улучшения"),
        FieldSpec("delta_cs", "float", "Прирост потребительского излишка"),
        FieldSpec("delta_ps", "float", "Прирост производственного излишка"),
        FieldSpec("delta_ts", "float", "Прирост общего излишка"),
        FieldSpec("price_drop_pct", "float", "Снижение цены (%)"),
    ),
)

LAFFER_COMMODITY = TaskSpec(
    id="laffer_commodity_v1",
    title="Кривая Лаффера на рынке сахара",
    topic="taxes_subsidies",
    difficulty=3,
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0)"),
        FieldSpec("c", "float", "Параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0)"),
        FieldSpec("current_tax", "float", "Текущий налог (для сравнения)"),
    ),
    output_fields=(
        FieldSpec("t_opt", "float", "Налог, максимизирующий поступления"),
        FieldSpec("q_at_opt", "float", "Объём при оптимальном налоге"),
        FieldSpec("revenue_max", "float", "Максимальные налоговые поступления"),
        FieldSpec("p_buyer_opt", "float", "Цена покупателя при оптимальном налоге"),
        FieldSpec("p_seller_opt", "float", "Цена продавца при оптимальном налоге"),
        FieldSpec("t_prohibitive", "float", "Запретительный налог (объём → 0)"),
        FieldSpec("rev_current", "float", "Поступления при текущем налоге"),
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
    PRICE_FLOOR.id: (PRICE_FLOOR, solve_price_floor),
    SUPPLY_SHIFT.id: (SUPPLY_SHIFT, solve_supply_shift),
    INCOME_ELASTICITY.id: (INCOME_ELASTICITY, solve_income_elasticity),
    DEMAND_AGGREGATION.id: (DEMAND_AGGREGATION, solve_demand_aggregation),
    MONOPOLY.id: (MONOPOLY, solve_monopoly),
    AD_VALOREM_TAX.id: (AD_VALOREM_TAX, solve_ad_valorem_tax),
    TRADE_TARIFF.id: (TRADE_TARIFF, solve_trade_tariff),
    PIGOUVIAN_TAX.id: (PIGOUVIAN_TAX, solve_pigouvian_tax),
    SIMULTANEOUS_SHIFT.id: (SIMULTANEOUS_SHIFT, solve_simultaneous_shift),
    GOV_PRICE_SUPPORT.id: (GOV_PRICE_SUPPORT, solve_gov_price_support),
    REVENUE_MAX.id: (REVENUE_MAX, solve_revenue_max),
    WELFARE_SUPPLY_IMPROVEMENT.id: (WELFARE_SUPPLY_IMPROVEMENT, solve_welfare_supply_improvement),
    LAFFER_COMMODITY.id: (LAFFER_COMMODITY, solve_laffer_commodity),
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

// Самая большая страница проекта — здесь пользователь решает задачу.
// Структура файла:
// 1)Большие справочники с данными по 20 задачам: поля ввода/вывода, подписи, шаблон кода, текст условия
// 2)Функции построения точек для графиков (одна на каждый тип задачи)
// 3)Сам компонент со всеми хуками состояния, отправкой решения и отображением результата
// Большая часть строк — это данные и JSX-разметка, чистой логики тут не так много.

import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { ArrowLeft, Play, RotateCcw, Lightbulb } from "lucide-react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ReferenceDot, ReferenceLine
} from "recharts";


// ============================================================
//  ДАННЫЕ ПО ЗАДАЧАМ (статические справочники)
//  Ниже четыре больших словаря: какие поля у каждой задачи,
//  как их подписывать, шаблон кода, текст условия. Это просто
//  данные, никакой логики тут нет.
// ============================================================

const taskInputKeys: Record<string, string[]> = {
  "equilibrium_linear_v1": ["a", "b", "c", "d", "mode", "t"],
  "surplus_calc_v1": ["a", "b", "c", "d"],
  "dwl_tax_v1": ["a", "b", "c", "d", "t", "mode"],
  "elasticity_v1": ["a", "b", "p"],
  "price_ceiling_v1": ["a", "b", "c", "d", "p_ceil"],
  "tax_revenue_v1": ["a", "b", "c", "d", "t"],
  "demand_shift_v1": ["a", "b", "c", "d", "a_new"],
  "price_floor_v1": ["a", "b", "c", "d", "p_floor"],
  "supply_shift_v1": ["a", "b", "c", "d", "c_new"],
  "income_elasticity_v1": ["q1", "i1", "q2", "i2"],
  "demand_aggregation_v1": ["a1", "b1", "a2", "b2", "c", "d"],
  "monopoly_v1": ["A", "B", "mc"],
  "ad_valorem_tax_v1": ["a", "b", "c", "d", "tau"],
  "trade_tariff_v1": ["a", "b", "c", "d", "p_world", "tariff"],
  "pigouvian_tax_v1": ["a", "b", "c", "d", "e"],
  "simultaneous_shift_v1": ["a", "b", "c", "d", "a_new", "c_new"],
  "gov_price_support_v1": ["a", "b", "c", "d", "p_support"],
  "revenue_max_v1": ["a", "b", "p_current"],
  "welfare_supply_improvement_v1": ["a", "b", "c", "d", "c_new"],
  "laffer_commodity_v1": ["a", "b", "c", "d", "current_tax"],
};

const taskOutputKeys: Record<string, string[]> = {
  "equilibrium_linear_v1": ["p_eq", "q_eq"],
  "surplus_calc_v1": ["cs", "ps", "total_surplus"],
  "dwl_tax_v1": ["p_buyer", "p_seller", "q_new", "cs_after", "ps_after", "gov_balance", "dwl", "buyer_share", "seller_share"],
  "elasticity_v1": ["elasticity", "revenue", "elastic_type"],
  "price_ceiling_v1": ["p_actual", "q_demanded", "q_supplied", "q_traded", "shortage", "binding"],
  "tax_revenue_v1": ["p_buyer", "p_seller", "q_tax", "tax_revenue", "price_increase", "quantity_decrease"],
  "demand_shift_v1": ["p_old", "q_old", "p_new", "q_new", "delta_p", "delta_q"],
  "price_floor_v1": ["p_actual", "q_demanded", "q_supplied", "q_traded", "surplus_qty", "binding"],
  "supply_shift_v1": ["p_old", "q_old", "p_new", "q_new", "delta_p", "delta_q"],
  "income_elasticity_v1": ["income_elasticity", "is_normal", "is_luxury"],
  "demand_aggregation_v1": ["p_eq", "q_eq", "q1_eq", "q2_eq", "cs1", "cs2", "ps"],
  "monopoly_v1": ["p_monopoly", "q_monopoly", "profit", "cs", "p_competitive", "q_competitive", "dwl"],
  "ad_valorem_tax_v1": ["p_buyer", "p_seller", "q_new", "tax_revenue", "cs_after", "ps_after", "dwl", "buyer_share", "seller_share"],
  "trade_tariff_v1": ["imports_free", "qs_tariff", "qd_tariff", "imports_tariff", "tariff_revenue", "consumer_loss", "producer_gain", "dwl"],
  "pigouvian_tax_v1": ["p_market", "q_market", "p_social", "q_social", "pigouvian_tax", "external_damage", "dwl_without_tax"],
  "simultaneous_shift_v1": ["p_old", "q_old", "p_new", "q_new", "delta_p", "delta_q", "delta_cs", "delta_ps"],
  "gov_price_support_v1": ["qd", "qs", "gov_purchase", "gov_expenditure", "cs", "ps", "dwl"],
  "revenue_max_v1": ["p_optimal", "q_optimal", "tr_max", "tr_current", "revenue_gain", "ed_current"],
  "welfare_supply_improvement_v1": ["p_old", "p_new", "cs_old", "cs_new", "ps_old", "ps_new", "delta_cs", "delta_ps", "delta_ts", "price_drop_pct"],
  "laffer_commodity_v1": ["t_opt", "q_at_opt", "revenue_max", "p_buyer_opt", "p_seller_opt", "t_prohibitive", "rev_current"],
};

const fieldLabels: Record<string, string> = {
  a: "a (свободный член спроса)",
  b: "b (наклон спроса)",
  c: "c (свободный член предложения)",
  d: "d (наклон предложения)",
  t: "t (размер налога/субсидии)",
  p: "P (цена)",
  mode: "mode (режим)",
  p_ceil: "P_ceil (потолок цены)",
  a_new: "a_new (новый свободный член спроса)",
  p_eq: "P* (равновесная цена)",
  q_eq: "Q* (равновесное количество)",
  cs: "CS (излишек потребителя)",
  ps: "PS (излишек производителя)",
  total_surplus: "Total Surplus (общий излишек)",
  p_buyer: "P_buyer (цена покупателя)",
  p_seller: "P_seller (цена продавца)",
  q_new: "Q_new (новый объём)",
  cs_after: "CS_after (излишек потребителя после)",
  ps_after: "PS_after (излишек производителя после)",
  gov_balance: "Gov Balance (+налог / −субсидия)",
  dwl: "DWL (потери благосостояния)",
  buyer_share: "Buyer Share (доля бремени покупателя)",
  seller_share: "Seller Share (доля бремени продавца)",
  elasticity: "Ed (эластичность)",
  revenue: "TR (выручка)",
  elastic_type: "Тип эластичности (1 / -1 / 0)",
  p_actual: "P_actual (фактическая цена)",
  q_demanded: "Q_demanded (величина спроса)",
  q_supplied: "Q_supplied (величина предложения)",
  q_traded: "Q_traded (объём сделок)",
  shortage: "Shortage (дефицит)",
  binding: "Binding (потолок действует: 0/1)",
  q_tax: "Q_tax (объём с налогом)",
  tax_revenue: "Tax Revenue (налоговые поступления)",
  price_increase: "Price Increase (рост цены для покупателя)",
  quantity_decrease: "Quantity Decrease (снижение объёма)",
  p_old: "P_old (старая равновесная цена)",
  q_old: "Q_old (старый равновесный объём)",
  p_new: "P_new (новая равновесная цена)",
  delta_p: "ΔP (изменение цены)",
  delta_q: "ΔQ (изменение объёма)",
  p_floor: "P_floor (ценовой пол)",
  surplus_qty: "Surplus (избыток предложения)",
  c_new: "c_new (новый свободный член предложения)",
  q1: "Q1 (объём спроса при доходе I1)",
  i1: "I1 (начальный доход)",
  q2: "Q2 (объём спроса при доходе I2)",
  i2: "I2 (конечный доход)",
  income_elasticity: "E_I (эластичность по доходу)",
  is_normal: "Is Normal (1 = нормальное, -1 = инфериорное)",
  is_luxury: "Is Luxury (1 = предмет роскоши, 0 = нет)",
  a1: "a1 (свободный член спроса потребителя 1)",
  b1: "b1 (наклон спроса потребителя 1)",
  a2: "a2 (свободный член спроса потребителя 2)",
  b2: "b2 (наклон спроса потребителя 2)",
  q1_eq: "Q1* (объём потребителя 1 в равновесии)",
  q2_eq: "Q2* (объём потребителя 2 в равновесии)",
  cs1: "CS1 (излишек потребителя 1)",
  cs2: "CS2 (излишек потребителя 2)",
  A: "A (параметр обратного спроса: P = A − B·Q)",
  B: "B (наклон обратного спроса)",
  mc: "MC (предельные издержки)",
  p_monopoly: "P_monopoly (монопольная цена)",
  q_monopoly: "Q_monopoly (монопольный объём)",
  profit: "Profit (прибыль монополиста)",
  p_competitive: "P_competitive (конкурентная цена)",
  q_competitive: "Q_competitive (конкурентный объём)",
  tau: "τ (ставка НДС, доля от цены покупателя)",
  p_world: "P_world (мировая цена)",
  tariff: "Tariff (размер тарифа)",
  imports_free: "Imports Free (импорт при свободной торговле)",
  qs_tariff: "Qs Tariff (отечественное предложение с тарифом)",
  qd_tariff: "Qd Tariff (отечественный спрос с тарифом)",
  imports_tariff: "Imports Tariff (импорт с тарифом)",
  tariff_revenue: "Tariff Revenue (таможенные поступления)",
  consumer_loss: "Consumer Loss (потери потребителей)",
  producer_gain: "Producer Gain (выигрыш производителей)",
  e: "e (внешние издержки на единицу)",
  p_market: "P_market (рыночная цена без налога)",
  q_market: "Q_market (рыночный объём без налога)",
  p_social: "P_social (социально оптимальная цена)",
  q_social: "Q_social (социально оптимальный объём)",
  pigouvian_tax: "Pigouvian Tax (налог Пигу)",
  external_damage: "External Damage (суммарный внешний ущерб)",
  dwl_without_tax: "DWL Without Tax (потери без налога)",
  delta_cs: "ΔCS (изменение излишка потребителя)",
  delta_ps: "ΔPS (изменение излишка производителя)",
  p_support: "P_support (цена поддержки)",
  qd: "Qd (спрос при цене поддержки)",
  qs: "Qs (предложение при цене поддержки)",
  gov_purchase: "Gov Purchase (объём госзакупок)",
  gov_expenditure: "Gov Expenditure (расходы государства)",
  p_current: "P_current (текущая цена)",
  p_optimal: "P_optimal (цена, максимизирующая выручку)",
  q_optimal: "Q_optimal (объём при оптимальной цене)",
  tr_max: "TR_max (максимальная выручка)",
  tr_current: "TR_current (текущая выручка)",
  revenue_gain: "Revenue Gain (прирост выручки)",
  ed_current: "Ed_current (эластичность при текущей цене)",
  cs_old: "CS_old (CS до улучшения)",
  cs_new: "CS_new (CS после улучшения)",
  ps_old: "PS_old (PS до улучшения)",
  ps_new: "PS_new (PS после улучшения)",
  delta_ts: "ΔTS (прирост общего излишка)",
  price_drop_pct: "Price Drop % (снижение цены в %)",
  current_tax: "Current Tax (текущий налог для сравнения)",
  t_opt: "T_opt (оптимальный налог)",
  q_at_opt: "Q at Opt (объём при оптимальном налоге)",
  revenue_max: "Revenue Max (максимальные поступления)",
  p_buyer_opt: "P_buyer Opt (цена покупателя при T_opt)",
  p_seller_opt: "P_seller Opt (цена продавца при T_opt)",
  t_prohibitive: "T_prohibitive (запретительный налог)",
  rev_current: "Rev Current (поступления при текущем налоге)",
};

const codeTemplates: Record<string, string> = {
  "equilibrium_linear_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "    mode = params['mode']",
    "    t = float(params.get('t', 0.0))",
    "",
    "    # Напишите решение",
    "    p_eq = 0.0",
    "    q_eq = 0.0",
    "",
    "    return {'p_eq': p_eq, 'q_eq': q_eq}",
  ].join("\n"),

  "surplus_calc_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "",
    "    # Напишите решение",
    "    cs = 0.0",
    "    ps = 0.0",
    "    total_surplus = 0.0",
    "",
    "    return {'cs': cs, 'ps': ps, 'total_surplus': total_surplus}",
  ].join("\n"),

  "dwl_tax_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "    t = float(params['t'])",
    "    mode = params['mode']",
    "",
    "    # Напишите решение",
    "    p_buyer = 0.0",
    "    p_seller = 0.0",
    "    q_new = 0.0",
    "    cs_after = 0.0",
    "    ps_after = 0.0",
    "    gov_balance = 0.0",
    "    dwl = 0.0",
    "    buyer_share = 0.0",
    "    seller_share = 0.0",
    "",
    "    return {",
    "        'p_buyer': p_buyer, 'p_seller': p_seller,",
    "        'q_new': q_new, 'cs_after': cs_after,",
    "        'ps_after': ps_after, 'gov_balance': gov_balance,",
    "        'dwl': dwl, 'buyer_share': buyer_share,",
    "        'seller_share': seller_share,",
    "    }",
  ].join("\n"),

  "elasticity_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    p = float(params['p'])",
    "",
    "    # Напишите решение",
    "    elasticity = 0.0",
    "    revenue = 0.0",
    "    elastic_type = 0.0",
    "",
    "    return {'elasticity': elasticity, 'revenue': revenue, 'elastic_type': elastic_type}",
  ].join("\n"),

  "price_ceiling_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "    p_ceil = float(params['p_ceil'])",
    "",
    "    # Напишите решение",
    "    p_actual = 0.0",
    "    q_demanded = 0.0",
    "    q_supplied = 0.0",
    "    q_traded = 0.0",
    "    shortage = 0.0",
    "    binding = 0",
    "",
    "    return {",
    "        'p_actual': p_actual, 'q_demanded': q_demanded,",
    "        'q_supplied': q_supplied, 'q_traded': q_traded,",
    "        'shortage': shortage, 'binding': binding,",
    "    }",
  ].join("\n"),

  "tax_revenue_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "    t = float(params['t'])",
    "",
    "    # Напишите решение",
    "    p_buyer = 0.0",
    "    p_seller = 0.0",
    "    q_tax = 0.0",
    "    tax_revenue = 0.0",
    "    price_increase = 0.0",
    "    quantity_decrease = 0.0",
    "",
    "    return {",
    "        'p_buyer': p_buyer, 'p_seller': p_seller,",
    "        'q_tax': q_tax, 'tax_revenue': tax_revenue,",
    "        'price_increase': price_increase,",
    "        'quantity_decrease': quantity_decrease,",
    "    }",
  ].join("\n"),

  "demand_shift_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "    a_new = float(params['a_new'])",
    "",
    "    # Напишите решение",
    "    p_old = 0.0",
    "    q_old = 0.0",
    "    p_new = 0.0",
    "    q_new = 0.0",
    "    delta_p = 0.0",
    "    delta_q = 0.0",
    "",
    "    return {",
    "        'p_old': p_old, 'q_old': q_old,",
    "        'p_new': p_new, 'q_new': q_new,",
    "        'delta_p': delta_p, 'delta_q': delta_q,",
    "    }",
  ].join("\n"),

  "price_floor_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "    p_floor = float(params['p_floor'])",
    "",
    "    # Напишите решение",
    "    p_actual = 0.0",
    "    q_demanded = 0.0",
    "    q_supplied = 0.0",
    "    q_traded = 0.0",
    "    surplus_qty = 0.0",
    "    binding = 0",
    "",
    "    return {",
    "        'p_actual': p_actual, 'q_demanded': q_demanded,",
    "        'q_supplied': q_supplied, 'q_traded': q_traded,",
    "        'surplus_qty': surplus_qty, 'binding': binding,",
    "    }",
  ].join("\n"),

  "supply_shift_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "    c_new = float(params['c_new'])",
    "",
    "    # Напишите решение",
    "    p_old = 0.0",
    "    q_old = 0.0",
    "    p_new = 0.0",
    "    q_new = 0.0",
    "    delta_p = 0.0",
    "    delta_q = 0.0",
    "",
    "    return {",
    "        'p_old': p_old, 'q_old': q_old,",
    "        'p_new': p_new, 'q_new': q_new,",
    "        'delta_p': delta_p, 'delta_q': delta_q,",
    "    }",
  ].join("\n"),

  "income_elasticity_v1": [
    "def solve(params):",
    "    q1 = float(params['q1'])",
    "    i1 = float(params['i1'])",
    "    q2 = float(params['q2'])",
    "    i2 = float(params['i2'])",
    "",
    "    # Напишите решение",
    "    income_elasticity = 0.0",
    "    is_normal = 0.0",
    "    is_luxury = 0.0",
    "",
    "    return {",
    "        'income_elasticity': income_elasticity,",
    "        'is_normal': is_normal,",
    "        'is_luxury': is_luxury,",
    "    }",
  ].join("\n"),

  "demand_aggregation_v1": [
    "def solve(params):",
    "    a1 = float(params['a1'])",
    "    b1 = float(params['b1'])",
    "    a2 = float(params['a2'])",
    "    b2 = float(params['b2'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "",
    "    # Напишите решение",
    "    p_eq = 0.0",
    "    q_eq = 0.0",
    "    q1_eq = 0.0",
    "    q2_eq = 0.0",
    "    cs1 = 0.0",
    "    cs2 = 0.0",
    "    ps = 0.0",
    "",
    "    return {",
    "        'p_eq': p_eq, 'q_eq': q_eq,",
    "        'q1_eq': q1_eq, 'q2_eq': q2_eq,",
    "        'cs1': cs1, 'cs2': cs2, 'ps': ps,",
    "    }",
  ].join("\n"),

  "monopoly_v1": [
    "def solve(params):",
    "    A = float(params['A'])",
    "    B = float(params['B'])",
    "    mc = float(params['mc'])",
    "",
    "    # Напишите решение",
    "    p_monopoly = 0.0",
    "    q_monopoly = 0.0",
    "    profit = 0.0",
    "    cs = 0.0",
    "    p_competitive = 0.0",
    "    q_competitive = 0.0",
    "    dwl = 0.0",
    "",
    "    return {",
    "        'p_monopoly': p_monopoly, 'q_monopoly': q_monopoly,",
    "        'profit': profit, 'cs': cs,",
    "        'p_competitive': p_competitive, 'q_competitive': q_competitive,",
    "        'dwl': dwl,",
    "    }",
  ].join("\n"),

  "ad_valorem_tax_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "    tau = float(params['tau'])",
    "",
    "    # Напишите решение",
    "    p_buyer = 0.0",
    "    p_seller = 0.0",
    "    q_new = 0.0",
    "    tax_revenue = 0.0",
    "    cs_after = 0.0",
    "    ps_after = 0.0",
    "    dwl = 0.0",
    "    buyer_share = 0.0",
    "    seller_share = 0.0",
    "",
    "    return {",
    "        'p_buyer': p_buyer, 'p_seller': p_seller,",
    "        'q_new': q_new, 'tax_revenue': tax_revenue,",
    "        'cs_after': cs_after, 'ps_after': ps_after,",
    "        'dwl': dwl, 'buyer_share': buyer_share,",
    "        'seller_share': seller_share,",
    "    }",
  ].join("\n"),

  "trade_tariff_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "    p_world = float(params['p_world'])",
    "    tariff = float(params['tariff'])",
    "",
    "    # Напишите решение",
    "    imports_free = 0.0",
    "    qs_tariff = 0.0",
    "    qd_tariff = 0.0",
    "    imports_tariff = 0.0",
    "    tariff_revenue = 0.0",
    "    consumer_loss = 0.0",
    "    producer_gain = 0.0",
    "    dwl = 0.0",
    "",
    "    return {",
    "        'imports_free': imports_free, 'qs_tariff': qs_tariff,",
    "        'qd_tariff': qd_tariff, 'imports_tariff': imports_tariff,",
    "        'tariff_revenue': tariff_revenue, 'consumer_loss': consumer_loss,",
    "        'producer_gain': producer_gain, 'dwl': dwl,",
    "    }",
  ].join("\n"),

  "pigouvian_tax_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "    e = float(params['e'])",
    "",
    "    # Напишите решение",
    "    p_market = 0.0",
    "    q_market = 0.0",
    "    p_social = 0.0",
    "    q_social = 0.0",
    "    pigouvian_tax = 0.0",
    "    external_damage = 0.0",
    "    dwl_without_tax = 0.0",
    "",
    "    return {",
    "        'p_market': p_market, 'q_market': q_market,",
    "        'p_social': p_social, 'q_social': q_social,",
    "        'pigouvian_tax': pigouvian_tax,",
    "        'external_damage': external_damage,",
    "        'dwl_without_tax': dwl_without_tax,",
    "    }",
  ].join("\n"),

  "simultaneous_shift_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "    a_new = float(params['a_new'])",
    "    c_new = float(params['c_new'])",
    "",
    "    # Напишите решение",
    "    p_old = 0.0",
    "    q_old = 0.0",
    "    p_new = 0.0",
    "    q_new = 0.0",
    "    delta_p = 0.0",
    "    delta_q = 0.0",
    "    delta_cs = 0.0",
    "    delta_ps = 0.0",
    "",
    "    return {",
    "        'p_old': p_old, 'q_old': q_old,",
    "        'p_new': p_new, 'q_new': q_new,",
    "        'delta_p': delta_p, 'delta_q': delta_q,",
    "        'delta_cs': delta_cs, 'delta_ps': delta_ps,",
    "    }",
  ].join("\n"),

  "gov_price_support_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "    p_support = float(params['p_support'])",
    "",
    "    # Напишите решение",
    "    qd = 0.0",
    "    qs = 0.0",
    "    gov_purchase = 0.0",
    "    gov_expenditure = 0.0",
    "    cs = 0.0",
    "    ps = 0.0",
    "    dwl = 0.0",
    "",
    "    return {",
    "        'qd': qd, 'qs': qs,",
    "        'gov_purchase': gov_purchase, 'gov_expenditure': gov_expenditure,",
    "        'cs': cs, 'ps': ps, 'dwl': dwl,",
    "    }",
  ].join("\n"),

  "revenue_max_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    p_current = float(params['p_current'])",
    "",
    "    # Напишите решение",
    "    p_optimal = 0.0",
    "    q_optimal = 0.0",
    "    tr_max = 0.0",
    "    tr_current = 0.0",
    "    revenue_gain = 0.0",
    "    ed_current = 0.0",
    "",
    "    return {",
    "        'p_optimal': p_optimal, 'q_optimal': q_optimal,",
    "        'tr_max': tr_max, 'tr_current': tr_current,",
    "        'revenue_gain': revenue_gain, 'ed_current': ed_current,",
    "    }",
  ].join("\n"),

  "welfare_supply_improvement_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "    c_new = float(params['c_new'])",
    "",
    "    # Напишите решение",
    "    p_old = 0.0",
    "    p_new = 0.0",
    "    cs_old = 0.0",
    "    cs_new = 0.0",
    "    ps_old = 0.0",
    "    ps_new = 0.0",
    "    delta_cs = 0.0",
    "    delta_ps = 0.0",
    "    delta_ts = 0.0",
    "    price_drop_pct = 0.0",
    "",
    "    return {",
    "        'p_old': p_old, 'p_new': p_new,",
    "        'cs_old': cs_old, 'cs_new': cs_new,",
    "        'ps_old': ps_old, 'ps_new': ps_new,",
    "        'delta_cs': delta_cs, 'delta_ps': delta_ps,",
    "        'delta_ts': delta_ts, 'price_drop_pct': price_drop_pct,",
    "    }",
  ].join("\n"),

  "laffer_commodity_v1": [
    "def solve(params):",
    "    a = float(params['a'])",
    "    b = float(params['b'])",
    "    c = float(params['c'])",
    "    d = float(params['d'])",
    "    current_tax = float(params['current_tax'])",
    "",
    "    # Напишите решение",
    "    t_opt = 0.0",
    "    q_at_opt = 0.0",
    "    revenue_max = 0.0",
    "    p_buyer_opt = 0.0",
    "    p_seller_opt = 0.0",
    "    t_prohibitive = 0.0",
    "    rev_current = 0.0",
    "",
    "    return {",
    "        't_opt': t_opt, 'q_at_opt': q_at_opt,",
    "        'revenue_max': revenue_max,",
    "        'p_buyer_opt': p_buyer_opt, 'p_seller_opt': p_seller_opt,",
    "        't_prohibitive': t_prohibitive, 'rev_current': rev_current,",
    "    }",
  ].join("\n"),
};


const taskDescriptions: Record<string, {
  title: string;
  difficulty: string;
  topic: string;
  condition: string;
  model: string;
  hint: string;
}> = {
  "equilibrium_linear_v1": {
    title: "Поиск равновесия на рынке яблок",
    difficulty: "Лёгкая",
    topic: "Равновесие",
    condition: "Каждую субботу на фермерском рынке посёлка Луговое продают яблоки. " +
        "Чем выше цена — тем меньше покупателей, но тем больше фермеров привозит товар. " +
        "Спрос и предложение описываются линейными функциями. " +
        "Рынок может работать в трёх режимах: свободный (none), с потоварным налогом (tax) " +
        "или с субсидией (subsidy). Параметр t задаёт размер налога или субсидии. " +
        "Найдите равновесную цену и количество, при которых спрос равен предложению.",
    model: "Qd(P) = a − b·P | Qs(P) = c + d·P | " +
        "Равновесие: a − b·P = c + d·P → P* = (a − c) / (b + d) | " +
        "При налоге: продавец получает (P − t), Qs = c + d·(P − t) | " +
        "При субсидии: продавец получает (P + t), Qs = c + d·(P + t)",
    hint: "Приравняйте Qd = Qs. Для режима none: P* = (a − c) / (b + d). " +
        "Для налога замените P в предложении на (P − t), для субсидии — на (P + t). " +
        "Затем подставьте P* обратно в Qd, чтобы найти Q*.",
  },

  "surplus_calc_v1": {
    title: "Излишки на рынке кофе",
    difficulty: "Средняя",
    topic: "Излишки",
    condition: "В университетском городке десятки кофеен борются за студентов-кофеманов. " +
        "Рынок достиг равновесия: цена устоялась, и каждый день продаётся одинаковое количество чашек. " +
        "Но часть покупателей была готова заплатить больше (потребительский излишек), " +
        "а часть продавцов могла продать дешевле (производственный излишек). " +
        "Посчитайте, сколько «лишнего» счастья получает каждая сторона, и найдите общий излишек рынка.",
    model: "Qd(P) = a − b·P | Qs(P) = c + d·P | " +
        "P* = (a − c) / (b + d), Q* = a − b·P* | " +
        "Pmax = a / b (цена, при которой спрос = 0) | " +
        "Pmin = −c / d (цена, при которой предложение = 0) | " +
        "CS = 0.5 · (Pmax − P*) · Q* | PS = 0.5 · (P* − Pmin) · Q*",
    hint: "Сначала найдите P* и Q*. Затем вычислите Pmax = a/b и Pmin = −c/d. " +
        "CS — это площадь треугольника над ценой равновесия под кривой спроса. " +
        "PS — площадь треугольника под ценой равновесия над кривой предложения.",
  },

  "dwl_tax_v1": {
    title: "Налог на импортную электронику",
    difficulty: "Сложная",
    topic: "Излишки",
    condition: "Правительство решило ввести потоварный налог на импортную электронику, " +
        "чтобы поддержать отечественных производителей. После введения налога цена для покупателя вырастет, " +
        "цена для продавца упадёт, а объём продаж сократится. Часть благосостояния перейдёт к государству " +
        "в виде налоговых поступлений, но часть будет безвозвратно потеряна (DWL). " +
        "Это самая содержательная задача: нужно посчитать 9 выходных параметров, " +
        "включая распределение налогового бремени между покупателями и продавцами.",
    model: "P0 = (a − c) / (b + d), Q0 = a − b·P0 | " +
        "С налогом: Pb = (a − c + d·t) / (b + d), Ps = Pb − t | " +
        "Q_new = a − b·Pb | " +
        "CS_after = 0.5 · (a/b − Pb) · Q_new | " +
        "PS_after = 0.5 · (Ps − (−c/d)) · Q_new | " +
        "Gov = t · Q_new | " +
        "DWL = (CS0 + PS0) − (CS_after + PS_after + Gov) | " +
        "Buyer share = (Pb − P0) / t, Seller share = (P0 − Ps) / t",
    hint: "Решайте по шагам: 1) равновесие без налога → P0, Q0; " +
        "2) излишки до вмешательства: CS0, PS0; 3) равновесие с налогом → Pb, Ps, Q_new; " +
        "4) излишки после + Gov; 5) DWL = разница. Для субсидии знак t меняется.",
  },

  "elasticity_v1": {
    title: "Цена билетов в кинотеатр",
    difficulty: "Средняя",
    topic: "Эластичность",
    condition: "Сеть кинотеатров «СтарСкрин» анализирует, как цена билета влияет на посещаемость. " +
        "Маркетологи хотят понять: если поднять цену на 10%, насколько упадёт число зрителей? " +
        "И что выгоднее — дешёвые билеты с полным залом или дорогие с пустыми рядами? " +
        "Вычислите точечную эластичность спроса, выручку и определите тип эластичности в заданной точке.",
    model: "Qd(P) = a − b·P | " +
        "Ed = (dQ/dP) · (P / Q) = −b · P / (a − b·P) | " +
        "TR = P · Q = P · (a − b·P) | " +
        "|Ed| > 1 → эластичный (elastic_type = 1) | " +
        "|Ed| < 1 → неэластичный (elastic_type = −1) | " +
        "|Ed| = 1 → единичная эластичность (elastic_type = 0)",
    hint: "Для линейного спроса dQ/dP = −b (константа). Подставьте P в Q = a − b·P, " +
        "затем в формулу эластичности. Выручка TR = P · Q. Сравните |Ed| с единицей.",
  },

  "price_ceiling_v1": {
    title: "Потолок цены на аренду жилья",
    difficulty: "Средняя",
    topic: "Равновесие",
    condition: "Мэрия крупного города обеспокоена ростом арендной платы и вводит потолок цены — " +
        "максимальную сумму, которую арендодатель может запросить. Если потолок ниже равновесной цены, " +
        "возникает дефицит: желающих снять квартиру больше, чем предложений. " +
        "Если потолок выше равновесия — он ни на что не влияет. " +
        "Определите, действует ли ограничение, и посчитайте фактическую цену, объёмы спроса и предложения, " +
        "реальный объём сделок и размер дефицита.",
    model: "P* = (a − c) / (b + d) | " +
        "Если p_ceil ≥ P*: потолок не действует (binding = 0), всё как без него | " +
        "Если p_ceil < P*: binding = 1, p_actual = p_ceil | " +
        "Qd(p_ceil) = a − b·p_ceil, Qs(p_ceil) = c + d·p_ceil | " +
        "q_traded = min(Qd, Qs) = Qs | shortage = Qd − Qs",
    hint: "Сначала найдите P*. Сравните p_ceil с P*. " +
        "Если потолок не действует — верните обычное равновесие (shortage = 0, binding = 0). " +
        "Если действует — подставьте p_ceil в обе функции и найдите дефицит.",
  },

  "tax_revenue_v1": {
    title: "Акциз на потребительский товар",
    difficulty: "Средняя",
    topic: "Излишки",
    condition: "Государство вводит акциз t на единицу товара на конкурентном рынке. " +
        "Нужно оценить эффект: налоговые поступления в бюджет, рост цены для покупателей, " +
        "снижение цены для продавцов и сокращение объёма продаж.",
    model: "P0 = (a − c) / (b + d), Q0 = a − b·P0 | " +
        "С налогом: Pb = (a − c + d·t) / (b + d), Ps = Pb − t | " +
        "Q_tax = a − b·Pb | " +
        "Tax Revenue = t · Q_tax | " +
        "Price Increase = Pb − P0 | " +
        "Quantity Decrease = Q0 − Q_tax",
    hint: "Формулы те же, что для равновесия с налогом. " +
        "Найдите P0 и Q0 без налога, затем Pb, Ps и Q_tax с налогом. " +
        "Разница цен — рост для покупателя, разница объёмов — снижение продаж.",
  },

  "demand_shift_v1": {
    title: "Мода на электросамокаты",
    difficulty: "Лёгкая",
    topic: "Равновесие",
    condition: "В городе построили сеть велодорожек, и спрос на электросамокаты резко вырос. " +
        "Кривая спроса сдвинулась вправо: параметр a увеличился до a_new. " +
        "Предложение осталось прежним. Найдите старое и новое равновесие, " +
        "а также на сколько изменились цена и объём продаж.",
    model: "Старое равновесие: P_old = (a − c) / (b + d), Q_old = a − b·P_old | " +
        "Новое равновесие: P_new = (a_new − c) / (b + d), Q_new = a_new − b·P_new | " +
        "ΔP = P_new − P_old | ΔQ = Q_new − Q_old",
    hint: "Решите задачу дважды — для старого a и для нового a_new. " +
        "Формула равновесия одна и та же, меняется только a. " +
        "Разности дадут delta_p и delta_q.",
  },

  "price_floor_v1": {
    title: "Ценовой пол на рынке труда",
    difficulty: "Средняя",
    topic: "Равновесие",
    condition: "Правительство устанавливает минимальный размер оплаты труда (МРОТ) — " +
        "ценовой пол, ниже которого работодатели не могут платить зарплату. " +
        "Если пол выше равновесной зарплаты, рабочих мест предлагается меньше, чем желающих работать — " +
        "возникает безработица (избыток предложения труда). " +
        "Если пол ниже равновесия — он не действует. " +
        "Определите, связывает ли ограничение рынок, и найдите все ключевые показатели.",
    model: "P* = (a − c) / (b + d) | " +
        "Если p_floor ≤ P*: пол не действует (binding = 0), p_actual = P* | " +
        "Если p_floor > P*: binding = 1, p_actual = p_floor | " +
        "Qd(p_floor) = a − b·p_floor, Qs(p_floor) = c + d·p_floor | " +
        "q_traded = min(Qd, Qs) = Qd | surplus_qty = Qs − Qd",
    hint: "Сначала найдите P*. Сравните p_floor с P*. " +
        "Если пол не действует — верните равновесие (surplus_qty = 0, binding = 0). " +
        "Если действует — подставьте p_floor в обе функции и найдите избыток.",
  },

  "supply_shift_v1": {
    title: "Новая нефтяная скважина: сдвиг предложения",
    difficulty: "Лёгкая",
    topic: "Равновесие",
    condition: "Нефтяная компания открыла новое месторождение и резко увеличила добычу. " +
        "Кривая предложения нефти сдвинулась вправо: параметр c вырос до c_new. " +
        "Спрос остался прежним. Найдите старое и новое равновесие, " +
        "а также на сколько изменились цена и объём.",
    model: "Старое равновесие: P_old = (a − c) / (b + d), Q_old = a − b·P_old | " +
        "Новое равновесие: P_new = (a − c_new) / (b + d), Q_new = a − b·P_new | " +
        "ΔP = P_new − P_old | ΔQ = Q_new − Q_old",
    hint: "Формула равновесия та же, что и для спроса — только теперь меняется c. " +
        "Рост c_new означает рост предложения → цена падает, объём растёт.",
  },

  "income_elasticity_v1": {
    title: "Эластичность спроса на авиабилеты по доходу",
    difficulty: "Средняя",
    topic: "Эластичность",
    condition: "Авиакомпания хочет понять, как рост доходов населения влияет на спрос на перелёты. " +
        "Известны объёмы спроса при двух уровнях дохода. " +
        "Рассчитайте дуговую эластичность спроса по доходу и определите тип блага: " +
        "нормальное (E > 0) или инфериорное (E < 0), " +
        "и является ли оно предметом роскоши (E > 1).",
    model: "E_I = (ΔQ / Q_avg) / (ΔI / I_avg) | " +
        "ΔQ = q2 − q1, Q_avg = (q1 + q2) / 2 | " +
        "ΔI = i2 − i1, I_avg = (i1 + i2) / 2 | " +
        "E_I > 0 → нормальное благо (is_normal = 1) | " +
        "E_I < 0 → инфериорное благо (is_normal = -1) | " +
        "E_I > 1 → предмет роскоши (is_luxury = 1)",
    hint: "Используйте дуговую формулу (через средние значения). " +
        "Знак E_I определяет тип блага, модуль — степень реакции. " +
        "is_luxury = 1 только если E_I строго больше 1.",
  },

  "demand_aggregation_v1": {
    title: "Агрегирование рыночного спроса двух потребителей",
    difficulty: "Сложная",
    topic: "Агрегирование",
    condition: "На небольшом рынке подержанных велосипедов есть два типа покупателей. " +
        "Каждый имеет свою линейную функцию спроса. " +
        "Рыночный (агрегированный) спрос — это горизонтальная сумма индивидуальных кривых. " +
        "Найдите равновесную цену и объём, распределение объёма между потребителями, " +
        "а также излишки каждой стороны.",
    model: "Qd_total(P) = (a1 − b1·P) + (a2 − b2·P) = (a1+a2) − (b1+b2)·P | " +
        "P* = (a1+a2 − c) / (b1+b2+d) | " +
        "q1_eq = a1 − b1·P*, q2_eq = a2 − b2·P* | " +
        "CS1 = 0.5·(a1/b1 − P*)·q1_eq | CS2 = 0.5·(a2/b2 − P*)·q2_eq | " +
        "PS = 0.5·(P* − (−c/d))·(q1_eq+q2_eq)",
    hint: "Сначала сложите параметры спросов: a_sum = a1+a2, b_sum = b1+b2. " +
        "Затем найдите равновесие как обычно. " +
        "Разделите Q* между потребителями, подставив P* в каждую функцию спроса.",
  },

  "monopoly_v1": {
    title: "Равновесие монополиста на фармацевтическом рынке",
    difficulty: "Сложная",
    topic: "Монополия",
    condition: "Фармацевтическая компания имеет патент на уникальный препарат и является монополистом. " +
        "Обратная функция спроса задана как P = A − B·Q. " +
        "Предельные издержки постоянны и равны mc. " +
        "Найдите монопольную цену и объём, прибыль, излишек потребителя, " +
        "а также сравните с конкурентным равновесием и найдите потери благосостояния.",
    model: "Обратный спрос: P = A − B·Q | " +
        "MR = A − 2B·Q | " +
        "Монополия: MR = MC → Q_m = (A − mc) / (2B), P_m = A − B·Q_m | " +
        "Profit = (P_m − mc)·Q_m | " +
        "CS = 0.5·(A − P_m)·Q_m | " +
        "Конкуренция: P_c = mc, Q_c = (A − mc) / B | " +
        "DWL = 0.5·(P_m − mc)·(Q_c − Q_m)",
    hint: "Монополист максимизирует прибыль при MR = MC. " +
        "MR для линейного спроса — вдвое круче: наклон = 2B. " +
        "DWL — треугольник между монопольным и конкурентным объёмами.",
  },

  "ad_valorem_tax_v1": {
    title: "НДС на рынке электроники",
    difficulty: "Сложная",
    topic: "Налоги и субсидии",
    condition: "Правительство вводит НДС по ставке τ (доля от цены покупателя) на бытовую электронику. " +
        "В отличие от потоварного налога, продавец получает P_buyer·(1 − τ). " +
        "Рассчитайте новые цены, объём, налоговые поступления, излишки и потери благосостояния.",
    model: "Без налога: P0 = (a − c) / (b + d), Q0 = a − b·P0 | " +
        "С НДС: продавец получает Ps = Pb·(1 − τ) | " +
        "Равновесие: a − b·Pb = c + d·Pb·(1 − τ) → Pb = (a − c) / (b + d·(1 − τ)) | " +
        "Ps = Pb·(1 − τ), Q_new = a − b·Pb | " +
        "Tax Revenue = (Pb − Ps)·Q_new | " +
        "Доли бремени: buyer_share = (Pb − P0) / (Pb − Ps)",
    hint: "Ключевое отличие от потоварного налога: ставка умножается на цену. " +
        "Подставьте Ps = Pb·(1−τ) в функцию предложения и найдите Pb из уравнения равновесия. " +
        "Затем все расчёты — как для обычного налога.",
  },

  "trade_tariff_v1": {
    title: "Импортный тариф на бытовую технику",
    difficulty: "Сложная",
    topic: "Международная торговля",
    condition: "Страна импортирует бытовую технику по мировой цене p_world (ниже внутреннего равновесия). " +
        "Правительство вводит удельный тариф, повышая внутреннюю цену до p_world + tariff. " +
        "Посчитайте объём импорта до и после тарифа, таможенные поступления, " +
        "потери потребителей, выигрыш отечественных производителей и чистые потери.",
    model: "Свободная торговля: внутренняя цена = p_world | " +
        "imports_free = Qd(p_world) − Qs(p_world) | " +
        "С тарифом: p_tariff = p_world + tariff | " +
        "qs_tariff = c + d·p_tariff, qd_tariff = a − b·p_tariff | " +
        "imports_tariff = qd_tariff − qs_tariff | " +
        "tariff_revenue = tariff·imports_tariff | " +
        "consumer_loss = ΔCS (площадь трапеции) | " +
        "producer_gain = ΔPS | DWL = consumer_loss − tariff_revenue − producer_gain",
    hint: "Подсчитайте CS и PS при p_world и при p_tariff. " +
        "consumer_loss = CS_free − CS_tariff. " +
        "producer_gain = PS_tariff − PS_free. " +
        "DWL = consumer_loss − producer_gain − tariff_revenue.",
  },

  "pigouvian_tax_v1": {
    title: "Экологический налог на химический завод",
    difficulty: "Сложная",
    topic: "Внешние эффекты",
    condition: "Химический завод производит продукцию, загрязняя реку. Каждая единица выпуска " +
        "наносит внешний ущерб e рублей жителям. Рынок не учитывает эти затраты, " +
        "поэтому производство избыточно. Государство планирует ввести налог Пигу. " +
        "Найдите рыночное и социально оптимальное равновесие, " +
        "размер оптимального налога и потери без него.",
    model: "Рыночное равновесие: P_market = (a − c) / (b + d), Q_market = a − b·P_market | " +
        "Социальные издержки: MSC = Qs_inverse + e, новое предложение: Qs_social = c + d·(P − e) | " +
        "Социальный оптимум: P_social = (a − c + d·e) / (b + d), Q_social = a − b·P_social | " +
        "Налог Пигу = e | External Damage = e·Q_market | " +
        "DWL = 0.5·e·(Q_market − Q_social)",
    hint: "Социально оптимальное предложение — это как ввести налог t = e. " +
        "Подставьте t = e в стандартную формулу равновесия с налогом. " +
        "DWL без налога — треугольник между Q_market и Q_social.",
  },

  "simultaneous_shift_v1": {
    title: "Рынок солнечных панелей: технологии и мода",
    difficulty: "Сложная",
    topic: "Равновесие",
    condition: "Одновременно произошли два события: появилась новая технология производства солнечных панелей " +
        "(предложение выросло, c → c_new) и климатическая кампания подняла спрос (a → a_new). " +
        "Найдите старое и новое равновесие, изменения цены и объёма, " +
        "а также как изменились излишки потребителей и производителей.",
    model: "P_old = (a − c) / (b + d), Q_old = a − b·P_old | " +
        "P_new = (a_new − c_new) / (b + d), Q_new = a_new − b·P_new | " +
        "ΔP = P_new − P_old, ΔQ = Q_new − Q_old | " +
        "CS = 0.5·(Pmax − P)·Q, ΔCS = CS_new − CS_old | " +
        "PS = 0.5·(P − Pmin)·Q, ΔPS = PS_new − PS_old",
    hint: "Найдите два равновесия по стандартной формуле, подставляя соответствующие a и c. " +
        "Для излишков нужны Pmax = a/b и Pmin = −c/d (используйте актуальные a и c для каждого периода).",
  },

  "gov_price_support_v1": {
    title: "Государственные закупки пшеницы",
    difficulty: "Сложная",
    topic: "Благосостояние",
    condition: "Государство хочет поддержать фермеров и устанавливает цену поддержки выше равновесия. " +
        "При этой цене предложение превышает спрос, и государство обязуется выкупить излишек. " +
        "Потребители проигрывают (высокая цена), фермеры выигрывают, " +
        "но государство тратит деньги на закупки. Посчитайте все показатели.",
    model: "P* = (a − c) / (b + d) | " +
        "qd = a − b·p_support, qs = c + d·p_support | " +
        "gov_purchase = qs − qd (закупает излишек) | " +
        "gov_expenditure = p_support·gov_purchase | " +
        "CS = 0.5·(a/b − p_support)·qd | " +
        "PS = 0.5·(p_support − (−c/d))·qs | " +
        "DWL = TS_before − (CS + PS − gov_expenditure)",
    hint: "Ключевой момент: государство выкупает весь излишек по цене поддержки. " +
        "PS считается от Pmin = −c/d до p_support по всему объёму qs (включая госзакупки). " +
        "DWL появляется из-за неэффективных сделок и перерасхода бюджета.",
  },

  "revenue_max_v1": {
    title: "Оптимальная цена авиабилетов",
    difficulty: "Средняя",
    topic: "Эластичность",
    condition: "Авиакомпания задаётся вопросом: при какой цене на билеты выручка будет максимальной? " +
        "Маркетолог знает, что выручка TR = P·Q максимальна при единичной эластичности спроса. " +
        "Текущая цена может быть слишком высокой или слишком низкой. " +
        "Найдите оптимальную цену, максимальную выручку и сравните с текущей.",
    model: "Qd(P) = a − b·P | TR(P) = P·(a − b·P) = a·P − b·P² | " +
        "dTR/dP = a − 2b·P = 0 → P_opt = a / (2b) | " +
        "Q_opt = a − b·P_opt = a/2 | TR_max = P_opt·Q_opt | " +
        "TR_current = p_current·(a − b·p_current) | " +
        "revenue_gain = TR_max − TR_current | " +
        "Ed_current = −b·p_current / (a − b·p_current)",
    hint: "Выручка максимальна в середине линейной кривой спроса: P_opt = a/(2b). " +
        "При этой цене эластичность = −1 (единичная). " +
        "Просто подставьте P_opt в Q и умножьте.",
  },

  "welfare_supply_improvement_v1": {
    title: "Технический прогресс в производстве смартфонов",
    difficulty: "Сложная",
    topic: "Благосостояние",
    condition: "Новая технология производства смартфонов снизила себестоимость. " +
        "Кривая предложения сдвинулась вправо (c → c_new), цена упала, объём вырос. " +
        "Потребители выиграли (CS вырос), но производители могут как выиграть, так и проиграть — " +
        "это зависит от эластичности. Посчитайте все изменения.",
    model: "P_old = (a − c) / (b + d), Q_old = a − b·P_old | " +
        "P_new = (a − c_new) / (b + d), Q_new = a − b·P_new | " +
        "CS = 0.5·(a/b − P)·Q | PS = 0.5·(P − (−c/d))·Q | " +
        "delta_cs = CS_new − CS_old | delta_ps = PS_new − PS_old | " +
        "delta_ts = delta_cs + delta_ps | " +
        "price_drop_pct = (P_old − P_new) / P_old · 100",
    hint: "Считайте CS и PS отдельно для старого и нового равновесия. " +
        "Для PS: Pmin = −c/d (используйте соответствующее c для каждого периода). " +
        "price_drop_pct — процент снижения цены, положительное число.",
  },

  "laffer_commodity_v1": {
    title: "Кривая Лаффера на рынке сахара",
    difficulty: "Сложная",
    topic: "Налоги и субсидии",
    condition: "Правительство анализирует налоговую политику на рынке сахара. " +
        "При нулевом налоге поступлений нет. При слишком высоком — рынок сужается до нуля, поступлений тоже нет. " +
        "Где-то посередине — максимум. Это кривая Лаффера для товарного налога. " +
        "Найдите оптимальный налог, максимальные поступления, запретительный налог и сравните с текущим.",
    model: "TR(t) = t·Q(t), где Q(t) = (a − c − (b·d·t)/(b+d)·... ) | " +
        "Упрощённо: Q(t) = Q0 − t·b·d/(b+d), где Q0 = (a−c)·d/(b+d) | " +
        "t_opt = (a − c) / (2·... ) → точная формула: t_opt = (a−c) / (b + d) · (b+d)/(2d) | " +
        "Или: максимум TR(t) = t·Q(t) → d(TR)/dt = 0 | " +
        "t_prohibitive: Q(t) = 0 → t_proh = (a − c) / d | " +
        "Pb(t) = (a − c + d·t) / (b+d), Ps = Pb − t",
    hint: "TR(t) = t·Q(t) — квадратичная функция от t. Найдите её максимум через производную. " +
        "t_opt = (a − c) / (2·b·d/(b+d)·... ) — проще всего взять dTR/dt = 0. " +
        "t_prohibitive — налог при котором Q = 0, то есть Pb = a/b, Ps = c/d, t = Pb − Ps = (a−c)/(b+d)·(b+d)/d.",
  },
};

// ============================================================
//  ПОСТРОЕНИЕ ТОЧЕК ДЛЯ ГРАФИКОВ
//  Каждая функция возвращает массив {p, qd, qs, ...} для Recharts.
//  Под каждый тип задачи (равновесие, монополия, сдвиг и т.д.) — свой набор кривых.
// ============================================================

function buildChartData(a: number, b: number, c: number, d: number) {
  const points = [];
  const maxP = Math.ceil((a / b) * 1.1);
  for (let p = 0; p <= maxP; p += 1) {
    const qd = a - b * p;
    const qs = c + d * p;
    points.push({
      price: p,
      demand: qd > 0 ? Math.round(qd * 100) / 100 : 0,
      supply: qs > 0 ? Math.round(qs * 100) / 100 : 0,
    });
  }
  return points;
}

function buildElasticityChart(a: number, b: number, p: number) {
  const points = [];
  const maxP = Math.ceil((a / b) * 1.1);
  for (let i = 0; i <= maxP; i += 1) {
    const qd = a - b * i;
    points.push({ price: i, demand: qd > 0 ? Math.round(qd * 100) / 100 : 0 });
  }
  return { points, pointQ: a - b * p };
}

function buildSupplyShiftChart(a: number, b: number, c: number, d: number, cNew: number) {
  const points = [];
  const maxP = Math.ceil((a / b) * 1.1);
  for (let p = 0; p <= maxP; p += 1) {
    const qd = a - b * p;
    const qsOld = c + d * p;
    const qsNew = cNew + d * p;
    points.push({
      price: p,
      demand: qd > 0 ? Math.round(qd * 100) / 100 : 0,
      supplyOld: qsOld > 0 ? Math.round(qsOld * 100) / 100 : 0,
      supplyNew: qsNew > 0 ? Math.round(qsNew * 100) / 100 : 0,
    });
  }
  return points;
}

function buildSimultaneousChart(a: number, b: number, c: number, d: number, aNew: number, cNew: number) {
  const points = [];
  const maxP = Math.ceil((Math.max(a, aNew) / b) * 1.1);
  for (let p = 0; p <= maxP; p += 1) {
    const qdOld = a - b * p;
    const qdNew = aNew - b * p;
    const qsOld = c + d * p;
    const qsNew = cNew + d * p;
    points.push({
      price: p,
      demandOld: qdOld > 0 ? Math.round(qdOld * 100) / 100 : 0,
      demandNew: qdNew > 0 ? Math.round(qdNew * 100) / 100 : 0,
      supplyOld: qsOld > 0 ? Math.round(qsOld * 100) / 100 : 0,
      supplyNew: qsNew > 0 ? Math.round(qsNew * 100) / 100 : 0,
    });
  }
  return points;
}

function buildMonopolyChart(A: number, B: number, mc: number) {
  const qMax = Math.ceil((A / B) * 1.1);
  const step = qMax / 80;
  const points = [];
  for (let q = 0; q <= qMax; q += step) {
    const p = A - B * q;
    const mr = A - 2 * B * q;
    points.push({
      qty: Math.round(q * 10) / 10,
      demand: p > 0 ? Math.round(p * 100) / 100 : 0,
      mr: Math.round(mr * 100) / 100,
      mc: mc,
    });
  }
  return points;
}

function buildRevenueChart(a: number, b: number) {
  const maxP = Math.ceil(a / b);
  const points = [];
  for (let p = 0; p <= maxP; p += 1) {
    const q = a - b * p;
    const tr = q > 0 ? p * q : 0;
    points.push({ price: p, tr: Math.round(tr * 100) / 100 });
  }
  return points;
}

function buildDemandAggChart(a1: number, b1: number, a2: number, b2: number, c: number, d: number) {
  const maxP = Math.ceil(Math.max(a1 / b1, a2 / b2) * 1.1);
  const points = [];
  for (let p = 0; p <= maxP; p += 1) {
    const qd1 = a1 - b1 * p;
    const qd2 = a2 - b2 * p;
    const qdT = (qd1 > 0 ? qd1 : 0) + (qd2 > 0 ? qd2 : 0);
    const qs = c + d * p;
    points.push({
      price: p,
      demand1: qd1 > 0 ? Math.round(qd1 * 100) / 100 : 0,
      demand2: qd2 > 0 ? Math.round(qd2 * 100) / 100 : 0,
      demandTotal: Math.round(qdT * 100) / 100,
      supply: qs > 0 ? Math.round(qs * 100) / 100 : 0,
    });
  }
  return points;
}

function buildLafferChart(a: number, b: number, c: number, d: number) {
  const q0 = (a * d + b * c) / (b + d);
  const slope = (b * d) / (b + d);
  const tProhibitive = q0 / slope;
  const points = [];
  const steps = 60;
  for (let i = 0; i <= steps; i++) {
    const t = (tProhibitive * i) / steps;
    const q = q0 - slope * t;
    const tr = q > 0 ? t * q : 0;
    points.push({ tax: Math.round(t * 100) / 100, revenue: Math.round(tr * 100) / 100 });
  }
  return { points, tProhibitive, tOpt: q0 / (2 * slope), revMax: (q0 * q0) / (4 * slope) };
}

function buildDemandShiftChart(a: number, b: number, c: number, d: number, aNew: number) {
  const points = [];
  const maxP = Math.ceil((Math.max(a, aNew) / b) * 1.1);
  for (let p = 0; p <= maxP; p += 1) {
    const qdOld = a - b * p;
    const qdNew = aNew - b * p;
    const qs = c + d * p;
    points.push({
      price: p,
      demandOld: qdOld > 0 ? Math.round(qdOld * 100) / 100 : 0,
      demandNew: qdNew > 0 ? Math.round(qdNew * 100) / 100 : 0,
      supply: qs > 0 ? Math.round(qs * 100) / 100 : 0,
    });
  }
  return points;
}

// Ключи выходных полей, которые дают точку (P, Q) для наложения на график спроса/предложения
const graphEqPQ: Record<string, [string, string]> = {
  "equilibrium_linear_v1": ["p_eq", "q_eq"],
  "dwl_tax_v1": ["p_buyer", "q_new"],
  "price_ceiling_v1": ["p_actual", "q_traded"],
  "tax_revenue_v1": ["p_buyer", "q_tax"],
  "price_floor_v1": ["p_actual", "q_traded"],
  "ad_valorem_tax_v1": ["p_buyer", "q_new"],
  "demand_shift_v1": ["p_new", "q_new"],
  "supply_shift_v1": ["p_new", "q_new"],
  "simultaneous_shift_v1": ["p_new", "q_new"],
  "demand_aggregation_v1": ["p_eq", "q_eq"],
  "pigouvian_tax_v1": ["p_social", "q_social"],
};

// ============================================================
//  ГЛАВНЫЙ КОМПОНЕНТ СТРАНИЦЫ
//  Состояние: код пользователя, текущий вердикт, разбор провалившегося теста,
//  публичный тест и его ответ, список прошлых сабмитов.
//  При смене задачи (taskId) всё сбрасывается, подгружается публичный тест.
// ============================================================

export default function SolvePage() {
  const { taskId } = useParams();
  const [activeTab, setActiveTab] = useState("condition");
  const [code, setCode] = useState("");
  const [verdict, setVerdict] = useState<string | null>(null);
  const [passed, setPassed] = useState(0);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [failMessage, setFailMessage] = useState("");
  const [failTestIndex, setFailTestIndex] = useState<number | null>(null);
  const [failInput, setFailInput] = useState<Record<string, any> | null>(null);
  const [failExpected, setFailExpected] = useState<Record<string, number> | null>(null);
  const [failGot, setFailGot] = useState<Record<string, number> | null>(null);
  const [showHint, setShowHint] = useState(false);
  const [showEq, setShowEq] = useState(true);
  const [showLabels, setShowLabels] = useState(true);
  const [publicTest, setPublicTest] = useState<Record<string, any> | null>(null);
  const [publicTestOutput, setPublicTestOutput] = useState<Record<string, any> | null>(null);
  const [submissions, setSubmissions] = useState<Array<{id: string; verdict: string; passed: number; total: number; created_at: string}>>([]);
  const [showHistory, setShowHistory] = useState(false);

  const info = taskDescriptions[taskId || ""];
  const fallback = taskDescriptions["equilibrium_linear_v1"];
  const desc = info || fallback;

  const inputKeys = taskInputKeys[taskId || ""] || [];
  const outputKeys = taskOutputKeys[taskId || ""] || [];

  function fetchSubmissions() {
    if (!taskId) return;
    const token = localStorage.getItem("token");
    const headers: Record<string, string> = {};
    if (token) headers["Authorization"] = "Bearer " + token;
    fetch("/api/v1/submissions?task_id=" + encodeURIComponent(taskId), { headers })
        .then((r) => r.ok ? r.json() : [])
        .then((data: Array<{id: string; verdict: string; passed: number; total: number; created_at: string}>) => {
          setSubmissions(data.slice(0, 20));
        })
        .catch(() => {});
  }

  useEffect(() => {
    setCode(codeTemplates[taskId || ""] || "def solve(params):\n    pass");
    setVerdict(null);
    setFailMessage("");
    setFailTestIndex(null);
    setFailInput(null);
    setFailExpected(null);
    setFailGot(null);
    setShowHint(false);
    setPublicTest(null);
    setPublicTestOutput(null);
    setSubmissions([]);
    setShowHistory(false);
    if (!taskId) return;
    fetch("/api/v1/tasks/" + encodeURIComponent(taskId))
        .then((res) => {
          if (!res.ok) throw new Error("Task not found");
          return res.json();
        })
        .then((data) => {
          if (data.public_test) setPublicTest(data.public_test);
          if (data.public_test_output) setPublicTestOutput(data.public_test_output);
        })
        .catch(() => {
          setPublicTest(null);
          setPublicTestOutput(null);
        });
    fetchSubmissions();
  }, [taskId]);

  // Автопереключение на вкладку графика при вердикте WA
  useEffect(() => {
    if (verdict === "WA") {
      setActiveTab("graph");
    }
  }, [verdict]);

  async function handleSubmit() {
    if (!taskId) {
      setVerdict("ERROR");
      setFailMessage("Задача не выбрана");
      return;
    }
    setLoading(true);
    setVerdict(null);
    try {
      const token = localStorage.getItem("token");
      const headers: Record<string, string> = { "Content-Type": "application/json" };
      if (token) headers["Authorization"] = "Bearer " + token;
      const res = await fetch("/api/v1/submissions", {
        method: "POST",
        headers: headers,
        body: JSON.stringify({ task_id: taskId, user_code: code }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => null);
        const detail = body && (body.detail || body.message);
        setVerdict("ERROR");
        setFailMessage(detail || `HTTP ${res.status} ${res.statusText}`);
        setLoading(false);
        return;
      }
      const data = await res.json();
      if (data.verdict) {
        setVerdict(data.verdict);
        setPassed(data.passed);
        setTotal(data.total);
        setFailMessage(data.message || "");
        setFailTestIndex(data.failed_test_index ?? null);
        setFailInput(data.failed_input ?? null);
        setFailExpected(data.failed_expected ?? null);
        setFailGot(data.failed_got ?? null);
      } else {
        setVerdict("ERROR");
        setFailMessage("Сервер вернул некорректный ответ");
      }
    } catch (e) {
      setVerdict("ERROR");
      setFailMessage(e instanceof Error ? e.message : "Сетевая ошибка");
    }
    setLoading(false);
    fetchSubmissions();
  }

  function handleReset() {
    setCode(codeTemplates[taskId || ""] || "def solve(params):\n    pass");
    setVerdict(null);
    setFailMessage("");
    setFailTestIndex(null);
    setFailInput(null);
    setFailExpected(null);
    setFailGot(null);
  }

  function getVerdictStyle(v: string) {
    if (v === "AC") return "text-green-600 bg-green-50 border-green-200";
    if (v === "WA") return "text-red-600 bg-red-50 border-red-200";
    if (v === "TLE") return "text-yellow-600 bg-yellow-50 border-yellow-200";
    return "text-red-600 bg-red-50 border-red-200";
  }

  function getVerdictText(v: string) {
    if (v === "AC") return "Accepted!";
    if (v === "WA") return "Wrong Answer";
    if (v === "TLE") return "Time Limit Exceeded";
    if (v === "RE") return "Runtime Error";
    return "Ошибка";
  }


  function renderPublicTest() {
    if (!publicTest) return null;

    const inputData = inputKeys
        .filter((k) => k in publicTest)
        .map((k) => ({ key: k, value: publicTest[k] }));

    const outputData = publicTestOutput
        ? outputKeys
            .filter((k) => k in publicTestOutput)
            .map((k) => ({ key: k, value: publicTestOutput[k] }))
        : [];

    return (
        <div className="mt-6 space-y-4">
          <div className="bg-blue-50 rounded-lg p-4 border border-blue-100">
            <div className="text-sm font-semibold text-blue-700 mb-3">Входные данные</div>
            <div className="grid grid-cols-2 gap-x-6 gap-y-2">
              {inputData.map((item) => (
                  <div key={item.key} className="flex justify-between items-center py-1 border-b border-blue-100 last:border-0">
                    <span className="text-sm text-blue-600 font-mono">{item.key}</span>
                    <span className="text-sm font-semibold text-blue-900">{String(item.value)}</span>
                  </div>
              ))}
            </div>
          </div>

          {outputData.length > 0 && (
              <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-100">
                <div className="text-sm font-semibold text-emerald-700 mb-3">Ожидаемый результат</div>
                <div className="grid grid-cols-2 gap-x-6 gap-y-2">
                  {outputData.map((item) => (
                      <div key={item.key} className="flex justify-between items-center py-1 border-b border-emerald-100 last:border-0">
                        <span className="text-sm text-emerald-600">{fieldLabels[item.key] || item.key}</span>
                        <span className="text-sm font-semibold text-emerald-900">{String(item.value)}</span>
                      </div>
                  ))}
                </div>
              </div>
          )}
        </div>
    );
  }


  function renderGraph() {
    if (!publicTest) return <p className="text-gray-400">Загрузка данных...</p>;

    const tid = taskId || "";

    // Правильная точка из publicTestOutput; ошибочная точка студента из failGot (только на публичном тесте)
    const eqKeys = graphEqPQ[tid];
    const correctDot = eqKeys && publicTestOutput
        ? { p: Number(publicTestOutput[eqKeys[0]]), q: Number(publicTestOutput[eqKeys[1]]) }
        : null;
    const studentDot = eqKeys && verdict === "WA" && failTestIndex === 0 && failGot
        ? { p: Number(failGot[eqKeys[0]]), q: Number(failGot[eqKeys[1]]) }
        : null;

    // Легенда для точек (показывается под графиком)
    function dotLegend(label: string) {
      return (
          <div className="mt-2 flex flex-wrap gap-4 text-sm text-gray-600">
            {correctDot && showEq && showLabels && (
                <span className="flex items-center gap-1">
                  <span className="inline-block w-3 h-3 rounded-full bg-green-500" />
                  {"Верно: P = " + correctDot.p.toFixed(2) + ", Q = " + correctDot.q.toFixed(2)}
                </span>
            )}
            {studentDot && showEq && showLabels && (
                <span className="flex items-center gap-1">
                  <span className="inline-block w-3 h-3 rounded-full bg-orange-500" />
                  {"Ваш ответ: P = " + studentDot.p.toFixed(2) + ", Q = " + studentDot.q.toFixed(2)}
                </span>
            )}
            {!correctDot && showLabels && label && (
                <span>{label}</span>
            )}
          </div>
      );
    }

    // ── income_elasticity: scatter Q vs I ──────────────────────────────────
    if (tid === "income_elasticity_v1") {
      const pts = [
        { income: publicTest.i1, quantity: publicTest.q1, name: "Точка 1" },
        { income: publicTest.i2, quantity: publicTest.q2, name: "Точка 2" },
      ];
      return (
          <div>
            <LineChart width={580} height={350} data={pts}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="income" label={{ value: "Доход (I)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Количество (Q)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip formatter={(v: any) => [v, ""]} labelFormatter={(l) => "I = " + l} />
              <Line type="monotone" dataKey="quantity" stroke="#6366f1" strokeWidth={2} dot={{ r: 6, fill: "#6366f1" }} name="Q(I)" />
            </LineChart>
            {showLabels && (
                <div className="mt-2 text-sm text-gray-600">
                  {"(I1=" + publicTest.i1 + ", Q1=" + publicTest.q1 + ") → (I2=" + publicTest.i2 + ", Q2=" + publicTest.q2 + ")"}
                </div>
            )}
          </div>
      );
    }

    // ── monopoly: inverse demand (x=Q, y=P) with MR and MC ────────────────
    if (tid === "monopoly_v1") {
      const A = Number(publicTest.A);
      const B = Number(publicTest.B);
      const mc = Number(publicTest.mc);
      const chartData = buildMonopolyChart(A, B, mc);
      const qM = (A - mc) / (2 * B);
      const pM = A - B * qM;
      const qC = (A - mc) / B;
      const cDot = publicTestOutput
          ? { q: Number(publicTestOutput.q_monopoly), p: Number(publicTestOutput.p_monopoly) }
          : { q: qM, p: pM };
      const sDot = verdict === "WA" && failTestIndex === 0 && failGot
          ? { q: Number(failGot.q_monopoly), p: Number(failGot.p_monopoly) }
          : null;
      return (
          <div>
            <LineChart width={580} height={350} data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="qty" label={{ value: "Количество (Q)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Цена (P)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip labelFormatter={(l) => "Q = " + l} />
              <Legend />
              <Line type="monotone" dataKey="demand" stroke="#6366f1" strokeWidth={2} dot={false} name="Спрос (P=A−BQ)" />
              <Line type="monotone" dataKey="mr" stroke="#a855f7" strokeWidth={2} dot={false} name="MR" strokeDasharray="6 3" />
              <Line type="monotone" dataKey="mc" stroke="#f97316" strokeWidth={2} dot={false} name="MC" />
              {showEq && <ReferenceDot x={Math.round(cDot.q * 10) / 10} y={Math.round(cDot.p * 10) / 10} r={7} fill="#22c55e" stroke="#fff" strokeWidth={2} label={{ value: "M", position: "top", fontSize: 11 }} />}
              {showEq && <ReferenceDot x={Math.round(qC * 10) / 10} y={Math.round(mc * 10) / 10} r={5} fill="#6366f1" stroke="#fff" strokeWidth={2} label={{ value: "C", position: "top", fontSize: 11 }} />}
              {showEq && sDot && <ReferenceDot x={Math.round(sDot.q * 10) / 10} y={Math.round(sDot.p * 10) / 10} r={7} fill="#f97316" stroke="#fff" strokeWidth={2} />}
            </LineChart>
            <div className="mt-2 flex flex-wrap gap-4 text-sm text-gray-600">
              {showEq && showLabels && <span className="flex items-center gap-1"><span className="inline-block w-3 h-3 rounded-full bg-green-500"/>{"Монополия: Q=" + cDot.q.toFixed(1) + ", P=" + cDot.p.toFixed(1)}</span>}
              {showEq && showLabels && <span className="flex items-center gap-1"><span className="inline-block w-3 h-3 rounded-full bg-indigo-500"/>{"Конкуренция: Q=" + qC.toFixed(1) + ", P=" + mc}</span>}
              {showEq && showLabels && sDot && <span className="flex items-center gap-1"><span className="inline-block w-3 h-3 rounded-full bg-orange-500"/>{"Ваш ответ: Q=" + sDot.q.toFixed(1) + ", P=" + sDot.p.toFixed(1)}</span>}
            </div>
          </div>
      );
    }

    // ── revenue_max: TR(P) quadratic curve ────────────────────────────────
    if (tid === "revenue_max_v1") {
      const a = publicTest.a;
      const b = publicTest.b;
      const pCur = publicTest.p_current;
      const chartData = buildRevenueChart(a, b);
      const pOpt = a / (2 * b);
      const trMax = pOpt * (a - b * pOpt);
      const trCur = pCur * (a - b * pCur);
      const cOptDot = publicTestOutput ? Number(publicTestOutput.p_optimal) : pOpt;
      const sDotP = verdict === "WA" && failTestIndex === 0 && failGot ? Number(failGot.p_optimal) : null;
      return (
          <div>
            <LineChart width={580} height={350} data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="price" label={{ value: "Цена (P)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "TR (выручка)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip labelFormatter={(l) => "P = " + l} />
              <Legend />
              <Line type="monotone" dataKey="tr" stroke="#6366f1" strokeWidth={2} dot={false} name="TR(P)" />
              {showEq && <ReferenceDot x={Math.round(cOptDot)} y={Math.round(trMax)} r={7} fill="#22c55e" stroke="#fff" strokeWidth={2} />}
              {showEq && <ReferenceDot x={Math.round(pCur)} y={Math.round(trCur)} r={5} fill="#94a3b8" stroke="#fff" strokeWidth={2} />}
              {showEq && sDotP !== null && <ReferenceDot x={Math.round(sDotP)} y={Math.round(sDotP * (a - b * sDotP))} r={7} fill="#f97316" stroke="#fff" strokeWidth={2} />}
            </LineChart>
            <div className="mt-2 flex flex-wrap gap-4 text-sm text-gray-600">
              {showEq && showLabels && <span className="flex items-center gap-1"><span className="inline-block w-3 h-3 rounded-full bg-green-500"/>{"P_opt=" + cOptDot.toFixed(1) + ", TR_max=" + trMax.toFixed(0)}</span>}
              {showEq && showLabels && <span className="flex items-center gap-1"><span className="inline-block w-3 h-3 rounded-full bg-slate-400"/>{"Текущая: P=" + pCur + ", TR=" + trCur.toFixed(0)}</span>}
              {showEq && showLabels && sDotP !== null && <span className="flex items-center gap-1"><span className="inline-block w-3 h-3 rounded-full bg-orange-500"/>{"Ваш P_opt=" + sDotP.toFixed(1)}</span>}
            </div>
          </div>
      );
    }

    // ── demand_aggregation: two demands + aggregate + supply ───────────────
    if (tid === "demand_aggregation_v1") {
      const a1 = publicTest.a1, b1 = publicTest.b1;
      const a2 = publicTest.a2, b2 = publicTest.b2;
      const c = publicTest.c, d = publicTest.d;
      const chartData = buildDemandAggChart(a1, b1, a2, b2, c, d);
      return (
          <div>
            <LineChart width={580} height={350} data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="price" label={{ value: "Цена (P)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Количество (Q)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip labelFormatter={(l) => "P = " + l} />
              <Legend />
              <Line type="monotone" dataKey="supply" stroke="#22c55e" strokeWidth={2} dot={false} name="Предложение" />
              <Line type="monotone" dataKey="demand1" stroke="#93c5fd" strokeWidth={1.5} dot={false} name="Спрос 1" strokeDasharray="4 3" />
              <Line type="monotone" dataKey="demand2" stroke="#c4b5fd" strokeWidth={1.5} dot={false} name="Спрос 2" strokeDasharray="4 3" />
              <Line type="monotone" dataKey="demandTotal" stroke="#6366f1" strokeWidth={2.5} dot={false} name="Совокупный спрос" />
              {showEq && correctDot && <ReferenceDot x={Math.round(correctDot.p)} y={Math.round(correctDot.q)} r={7} fill="#22c55e" stroke="#fff" strokeWidth={2} />}
              {showEq && studentDot && <ReferenceDot x={Math.round(studentDot.p)} y={Math.round(studentDot.q)} r={7} fill="#f97316" stroke="#fff" strokeWidth={2} />}
            </LineChart>
            {dotLegend("")}
          </div>
      );
    }

    // ── elasticity: demand curve only with point ───────────────────────────
    if (tid === "elasticity_v1") {
      const a = publicTest.a;
      const b = publicTest.b;
      const p = publicTest.p;
      const { points, pointQ } = buildElasticityChart(a, b, p);
      const ed = -b * p / pointQ;
      return (
          <div>
            <LineChart width={580} height={350} data={points}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="price" label={{ value: "Цена (P)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Количество (Q)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend formatter={() => "Спрос"} />
              <Line type="monotone" dataKey="demand" stroke="#6366f1" strokeWidth={2} dot={false} />
              {showEq && <ReferenceDot x={Math.round(p)} y={Math.round(pointQ)} r={6} fill="#22c55e" stroke="#fff" strokeWidth={2} />}
            </LineChart>
            {showEq && showLabels && (
                <div className="mt-2 text-sm text-gray-600">
                  {"Точка: P = " + p + ", Q = " + pointQ.toFixed(1) + ", Ed = " + ed.toFixed(2)}
                </div>
            )}
          </div>
      );
    }

    // ── demand_shift: two demand curves + supply ───────────────────────────
    if (tid === "demand_shift_v1") {
      const a = publicTest.a;
      const b = publicTest.b;
      const c = publicTest.c;
      const d = publicTest.d;
      const aNew = publicTest.a_new;
      const chartData = buildDemandShiftChart(a, b, c, d, aNew);
      const pOld = (a - c) / (b + d);
      const qOld = a - b * pOld;
      const cP = correctDot ? correctDot.p : (aNew - c) / (b + d);
      const cQ = correctDot ? correctDot.q : aNew - b * cP;
      return (
          <div>
            <LineChart width={580} height={350} data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="price" label={{ value: "Цена (P)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Количество (Q)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="supply" stroke="#22c55e" strokeWidth={2} dot={false} name="Предложение" />
              <Line type="monotone" dataKey="demandOld" stroke="#6366f1" strokeWidth={2} dot={false} name="Спрос (старый)" strokeDasharray="6 4" />
              <Line type="monotone" dataKey="demandNew" stroke="#3b82f6" strokeWidth={2} dot={false} name="Спрос (новый)" />
              {showEq && <ReferenceDot x={Math.round(pOld)} y={Math.round(qOld)} r={5} fill="#6366f1" stroke="#fff" strokeWidth={2} />}
              {showEq && <ReferenceDot x={Math.round(cP)} y={Math.round(cQ)} r={7} fill="#22c55e" stroke="#fff" strokeWidth={2} />}
              {showEq && studentDot && <ReferenceDot x={Math.round(studentDot.p)} y={Math.round(studentDot.q)} r={7} fill="#f97316" stroke="#fff" strokeWidth={2} />}
            </LineChart>
            {dotLegend("Старое: P=" + pOld.toFixed(1) + ", Q=" + qOld.toFixed(1) + " | Новое: P=" + cP.toFixed(1) + ", Q=" + cQ.toFixed(1))}
          </div>
      );
    }

    // ── supply_shift: two supply curves + demand ───────────────────────────
    if (tid === "supply_shift_v1") {
      const a = publicTest.a;
      const b = publicTest.b;
      const c = publicTest.c;
      const d = publicTest.d;
      const cNew = publicTest.c_new;
      const chartData = buildSupplyShiftChart(a, b, c, d, cNew);
      const pOld = (a - c) / (b + d);
      const qOld = a - b * pOld;
      const cP = correctDot ? correctDot.p : (a - cNew) / (b + d);
      const cQ = correctDot ? correctDot.q : a - b * cP;
      return (
          <div>
            <LineChart width={580} height={350} data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="price" label={{ value: "Цена (P)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Количество (Q)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="demand" stroke="#6366f1" strokeWidth={2} dot={false} name="Спрос" />
              <Line type="monotone" dataKey="supplyOld" stroke="#86efac" strokeWidth={2} dot={false} name="Предложение (старое)" strokeDasharray="6 4" />
              <Line type="monotone" dataKey="supplyNew" stroke="#22c55e" strokeWidth={2} dot={false} name="Предложение (новое)" />
              {showEq && <ReferenceDot x={Math.round(pOld)} y={Math.round(qOld)} r={5} fill="#86efac" stroke="#fff" strokeWidth={2} />}
              {showEq && <ReferenceDot x={Math.round(cP)} y={Math.round(cQ)} r={7} fill="#22c55e" stroke="#fff" strokeWidth={2} />}
              {showEq && studentDot && <ReferenceDot x={Math.round(studentDot.p)} y={Math.round(studentDot.q)} r={7} fill="#f97316" stroke="#fff" strokeWidth={2} />}
            </LineChart>
            {dotLegend("Старое: P=" + pOld.toFixed(1) + " | Новое: P=" + cP.toFixed(1))}
          </div>
      );
    }

    // ── simultaneous_shift: two D + two S curves ───────────────────────────
    if (tid === "simultaneous_shift_v1") {
      const a = publicTest.a;
      const b = publicTest.b;
      const c = publicTest.c;
      const d = publicTest.d;
      const aNew = publicTest.a_new;
      const cNew = publicTest.c_new;
      const chartData = buildSimultaneousChart(a, b, c, d, aNew, cNew);
      const pOld = (a - c) / (b + d);
      const qOld = a - b * pOld;
      const cP = correctDot ? correctDot.p : (aNew - cNew) / (b + d);
      const cQ = correctDot ? correctDot.q : aNew - b * cP;
      return (
          <div>
            <LineChart width={580} height={350} data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="price" label={{ value: "Цена (P)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Количество (Q)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="supplyOld" stroke="#86efac" strokeWidth={1.5} dot={false} name="Предл. (стар.)" strokeDasharray="6 4" />
              <Line type="monotone" dataKey="supplyNew" stroke="#22c55e" strokeWidth={2} dot={false} name="Предл. (нов.)" />
              <Line type="monotone" dataKey="demandOld" stroke="#c7d2fe" strokeWidth={1.5} dot={false} name="Спрос (стар.)" strokeDasharray="6 4" />
              <Line type="monotone" dataKey="demandNew" stroke="#6366f1" strokeWidth={2} dot={false} name="Спрос (нов.)" />
              {showEq && <ReferenceDot x={Math.round(pOld)} y={Math.round(qOld)} r={5} fill="#94a3b8" stroke="#fff" strokeWidth={2} />}
              {showEq && <ReferenceDot x={Math.round(cP)} y={Math.round(cQ)} r={7} fill="#22c55e" stroke="#fff" strokeWidth={2} />}
              {showEq && studentDot && <ReferenceDot x={Math.round(studentDot.p)} y={Math.round(studentDot.q)} r={7} fill="#f97316" stroke="#fff" strokeWidth={2} />}
            </LineChart>
            {dotLegend("Старое: P=" + pOld.toFixed(1) + " | Новое: P=" + cP.toFixed(1))}
          </div>
      );
    }

    // ── All remaining tasks: standard supply/demand graph ──────────────────
    const a = publicTest.a;
    const b = publicTest.b;
    const c = publicTest.c;
    const dd = publicTest.d;
    const chartData = buildChartData(a, b, c, dd);
    const eqP = (a - c) / (b + dd);
    const eqQ = a - b * eqP;

    // price_ceiling: горизонтальная линия ценового потолка
    if (tid === "price_ceiling_v1") {
      const pCeil = publicTest.p_ceil;
      const cP = correctDot ? correctDot.p : (pCeil < eqP ? pCeil : eqP);
      const cQ = correctDot ? correctDot.q : (pCeil < eqP ? c + dd * pCeil : eqQ);
      return (
          <div>
            <LineChart width={580} height={350} data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="price" label={{ value: "Цена (P)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Количество (Q)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip formatter={(v: any, n: any) => [typeof v === "number" ? v.toFixed(1) : String(v ?? ""), n === "demand" ? "Спрос" : "Предложение"]} labelFormatter={(l) => "P = " + l} />
              <Legend formatter={(v) => (v === "demand" ? "Спрос" : "Предложение")} />
              <Line type="monotone" dataKey="supply" stroke="#22c55e" strokeWidth={2} dot={false} name="supply" />
              <Line type="monotone" dataKey="demand" stroke="#6366f1" strokeWidth={2} dot={false} name="demand" />
              <ReferenceLine x={pCeil} stroke="#f97316" strokeDasharray="8 4" strokeWidth={2} label={{ value: "Потолок P=" + pCeil, position: "insideTopRight", fill: "#f97316", fontSize: 12 }} />
              {showEq && <ReferenceDot x={Math.round(eqP)} y={Math.round(eqQ)} r={5} fill="#94a3b8" stroke="#fff" strokeWidth={2} />}
              {showEq && <ReferenceDot x={Math.round(cP)} y={Math.round(cQ)} r={7} fill="#22c55e" stroke="#fff" strokeWidth={2} />}
              {showEq && studentDot && <ReferenceDot x={Math.round(studentDot.p)} y={Math.round(studentDot.q)} r={7} fill="#f97316" stroke="#fff" strokeWidth={2} />}
            </LineChart>
            {dotLegend("P*=" + eqP.toFixed(1) + " | Потолок=" + pCeil + (pCeil < eqP ? " (действует)" : " (не действует)"))}
          </div>
      );
    }

    // price_floor: горизонтальная линия ценового пола
    if (tid === "price_floor_v1") {
      const pFloor = publicTest.p_floor;
      const cP = correctDot ? correctDot.p : (pFloor > eqP ? pFloor : eqP);
      const cQ = correctDot ? correctDot.q : (pFloor > eqP ? a - b * pFloor : eqQ);
      return (
          <div>
            <LineChart width={580} height={350} data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="price" label={{ value: "Цена (P)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Количество (Q)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip formatter={(v: any, n: any) => [typeof v === "number" ? v.toFixed(1) : String(v ?? ""), n === "demand" ? "Спрос" : "Предложение"]} labelFormatter={(l) => "P = " + l} />
              <Legend formatter={(v) => (v === "demand" ? "Спрос" : "Предложение")} />
              <Line type="monotone" dataKey="supply" stroke="#22c55e" strokeWidth={2} dot={false} name="supply" />
              <Line type="monotone" dataKey="demand" stroke="#6366f1" strokeWidth={2} dot={false} name="demand" />
              <ReferenceLine x={pFloor} stroke="#f97316" strokeDasharray="8 4" strokeWidth={2} label={{ value: "Пол P=" + pFloor, position: "insideTopRight", fill: "#f97316", fontSize: 12 }} />
              {showEq && <ReferenceDot x={Math.round(eqP)} y={Math.round(eqQ)} r={5} fill="#94a3b8" stroke="#fff" strokeWidth={2} />}
              {showEq && <ReferenceDot x={Math.round(cP)} y={Math.round(cQ)} r={7} fill="#22c55e" stroke="#fff" strokeWidth={2} />}
              {showEq && studentDot && <ReferenceDot x={Math.round(studentDot.p)} y={Math.round(studentDot.q)} r={7} fill="#f97316" stroke="#fff" strokeWidth={2} />}
            </LineChart>
            {dotLegend("P*=" + eqP.toFixed(1) + " | Пол=" + pFloor + (pFloor > eqP ? " (действует)" : " (не действует)"))}
          </div>
      );
    }

    // trade_tariff: вертикальные линии — мировая цена и цена с тарифом
    if (tid === "trade_tariff_v1") {
      const pWorld = publicTest.p_world;
      const tariff = publicTest.tariff;
      const pTariff = pWorld + tariff;
      return (
          <div>
            <LineChart width={580} height={350} data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="price" label={{ value: "Цена (P)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Количество (Q)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip formatter={(v: any, n: any) => [typeof v === "number" ? v.toFixed(1) : String(v ?? ""), n === "demand" ? "Спрос" : "Предложение"]} labelFormatter={(l) => "P = " + l} />
              <Legend formatter={(v) => (v === "demand" ? "Спрос" : "Предложение")} />
              <Line type="monotone" dataKey="supply" stroke="#22c55e" strokeWidth={2} dot={false} name="supply" />
              <Line type="monotone" dataKey="demand" stroke="#6366f1" strokeWidth={2} dot={false} name="demand" />
              <ReferenceLine x={pWorld} stroke="#3b82f6" strokeDasharray="8 4" strokeWidth={2} label={{ value: "Мир P=" + pWorld, position: "insideTopLeft", fill: "#3b82f6", fontSize: 11 }} />
              <ReferenceLine x={pTariff} stroke="#f97316" strokeDasharray="8 4" strokeWidth={2} label={{ value: "Тариф P=" + pTariff, position: "insideTopRight", fill: "#f97316", fontSize: 11 }} />
              {showEq && <ReferenceDot x={Math.round(eqP)} y={Math.round(eqQ)} r={5} fill="#94a3b8" stroke="#fff" strokeWidth={2} />}
            </LineChart>
            {showEq && showLabels && <div className="mt-2 text-sm text-gray-600">{"Авт. равновесие: P*=" + eqP.toFixed(1) + " | Мировая: " + pWorld + " | С тарифом: " + pTariff}</div>}
          </div>
      );
    }

    // pigouvian: оба равновесия — рыночное и социальное
    if (tid === "pigouvian_tax_v1") {
      const mktP = correctDot ? (a - c) / (b + dd) : eqP;
      const mktQ = correctDot ? a - b * mktP : eqQ;
      const socP = correctDot ? correctDot.p : null;
      const socQ = correctDot ? correctDot.q : null;
      return (
          <div>
            <LineChart width={580} height={350} data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="price" label={{ value: "Цена (P)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Количество (Q)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip formatter={(v: any, n: any) => [typeof v === "number" ? v.toFixed(1) : String(v ?? ""), n === "demand" ? "Спрос" : "Предложение"]} labelFormatter={(l) => "P = " + l} />
              <Legend formatter={(v) => (v === "demand" ? "Спрос" : "Предложение")} />
              <Line type="monotone" dataKey="supply" stroke="#22c55e" strokeWidth={2} dot={false} name="supply" />
              <Line type="monotone" dataKey="demand" stroke="#6366f1" strokeWidth={2} dot={false} name="demand" />
              {showEq && <ReferenceDot x={Math.round(mktP)} y={Math.round(mktQ)} r={6} fill="#ef4444" stroke="#fff" strokeWidth={2} />}
              {showEq && socP !== null && socQ !== null && <ReferenceDot x={Math.round(socP)} y={Math.round(socQ)} r={7} fill="#22c55e" stroke="#fff" strokeWidth={2} />}
              {showEq && studentDot && <ReferenceDot x={Math.round(studentDot.p)} y={Math.round(studentDot.q)} r={7} fill="#f97316" stroke="#fff" strokeWidth={2} />}
            </LineChart>
            <div className="mt-2 flex flex-wrap gap-4 text-sm text-gray-600">
              {showEq && showLabels && <span className="flex items-center gap-1"><span className="inline-block w-3 h-3 rounded-full bg-red-500"/>{"Рынок: P=" + mktP.toFixed(1) + ", Q=" + mktQ.toFixed(1)}</span>}
              {showEq && showLabels && socP !== null && <span className="flex items-center gap-1"><span className="inline-block w-3 h-3 rounded-full bg-green-500"/>{"Оптимум: P=" + socP.toFixed(1) + ", Q=" + (socQ ?? 0).toFixed(1)}</span>}
              {showEq && showLabels && studentDot && <span className="flex items-center gap-1"><span className="inline-block w-3 h-3 rounded-full bg-orange-500"/>{"Ваш оптимум: P=" + studentDot.p.toFixed(1) + ", Q=" + studentDot.q.toFixed(1)}</span>}
            </div>
          </div>
      );
    }

    // gov_price_support: вертикальная линия цены государственной поддержки
    if (tid === "gov_price_support_v1") {
      const pSup = publicTest.p_support;
      return (
          <div>
            <LineChart width={580} height={350} data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="price" label={{ value: "Цена (P)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Количество (Q)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip formatter={(v: any, n: any) => [typeof v === "number" ? v.toFixed(1) : String(v ?? ""), n === "demand" ? "Спрос" : "Предложение"]} labelFormatter={(l) => "P = " + l} />
              <Legend formatter={(v) => (v === "demand" ? "Спрос" : "Предложение")} />
              <Line type="monotone" dataKey="supply" stroke="#22c55e" strokeWidth={2} dot={false} name="supply" />
              <Line type="monotone" dataKey="demand" stroke="#6366f1" strokeWidth={2} dot={false} name="demand" />
              <ReferenceLine x={pSup} stroke="#f97316" strokeDasharray="8 4" strokeWidth={2} label={{ value: "Поддержка P=" + pSup, position: "insideTopRight", fill: "#f97316", fontSize: 12 }} />
              {showEq && <ReferenceDot x={Math.round(eqP)} y={Math.round(eqQ)} r={5} fill="#94a3b8" stroke="#fff" strokeWidth={2} />}
            </LineChart>
            {showEq && showLabels && <div className="mt-2 text-sm text-gray-600">{"Равновесие: P*=" + eqP.toFixed(1) + ", Q*=" + eqQ.toFixed(1) + " | Поддержка: " + pSup}</div>}
          </div>
      );
    }

    // ── welfare_supply_improvement: two supply curves + demand (like supply_shift) ──
    if (tid === "welfare_supply_improvement_v1") {
      const cNew = publicTest.c_new;
      const chartData = buildSupplyShiftChart(a, b, c, dd, cNew);
      const pOld = (a - c) / (b + dd);
      const qOld = a - b * pOld;
      const cP = correctDot ? correctDot.p : (a - cNew) / (b + dd);
      const cQ = correctDot ? correctDot.q ?? (a - b * cP) : a - b * cP;
      return (
          <div>
            <LineChart width={580} height={350} data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="price" label={{ value: "Цена (P)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Количество (Q)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="demand" stroke="#6366f1" strokeWidth={2} dot={false} name="Спрос" />
              <Line type="monotone" dataKey="supplyOld" stroke="#86efac" strokeWidth={2} dot={false} name="Предложение (до)" strokeDasharray="6 4" />
              <Line type="monotone" dataKey="supplyNew" stroke="#22c55e" strokeWidth={2} dot={false} name="Предложение (после)" />
              {showEq && <ReferenceDot x={Math.round(pOld)} y={Math.round(qOld)} r={5} fill="#86efac" stroke="#fff" strokeWidth={2} />}
              {showEq && <ReferenceDot x={Math.round(cP)} y={Math.round(cQ)} r={7} fill="#22c55e" stroke="#fff" strokeWidth={2} />}
              {showEq && studentDot && <ReferenceDot x={Math.round(studentDot.p)} y={Math.round(studentDot.q)} r={7} fill="#f97316" stroke="#fff" strokeWidth={2} />}
            </LineChart>
            {dotLegend("До: P=" + pOld.toFixed(1) + " | После: P=" + cP.toFixed(1))}
          </div>
      );
    }

    // ── laffer_commodity: tax revenue curve (parabola) ────────────────────
    if (tid === "laffer_commodity_v1") {
      const { points, tOpt, revMax } = buildLafferChart(a, b, c, dd);
      const curTax = publicTest.current_tax;
      const q0 = (a * dd + b * c) / (b + dd);
      const sl = (b * dd) / (b + dd);
      const revCur = curTax * Math.max(0, q0 - sl * curTax);
      const cTopt = correctDot ? Number(publicTestOutput?.t_opt ?? tOpt) : tOpt;
      const cRevMax = correctDot ? Number(publicTestOutput?.revenue_max ?? revMax) : revMax;
      const sDotTax = verdict === "WA" && failTestIndex === 0 && failGot ? Number(failGot.t_opt) : null;
      return (
          <div>
            <LineChart width={580} height={350} data={points}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="tax" label={{ value: "Налог (t)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Tax Revenue", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip labelFormatter={(l) => "t = " + l} />
              <Legend />
              <Line type="monotone" dataKey="revenue" stroke="#6366f1" strokeWidth={2} dot={false} name="TR(t)" />
              {showEq && <ReferenceDot x={Math.round(cTopt * 10) / 10} y={Math.round(cRevMax)} r={7} fill="#22c55e" stroke="#fff" strokeWidth={2} />}
              {showEq && <ReferenceDot x={Math.round(curTax * 10) / 10} y={Math.round(revCur)} r={5} fill="#94a3b8" stroke="#fff" strokeWidth={2} />}
              {showEq && sDotTax !== null && <ReferenceDot x={Math.round(sDotTax * 10) / 10} y={Math.round(sDotTax * Math.max(0, q0 - sl * sDotTax))} r={7} fill="#f97316" stroke="#fff" strokeWidth={2} />}
            </LineChart>
            <div className="mt-2 flex flex-wrap gap-4 text-sm text-gray-600">
              {showEq && showLabels && <span className="flex items-center gap-1"><span className="inline-block w-3 h-3 rounded-full bg-green-500"/>{"T_opt=" + cTopt.toFixed(2) + ", Rev_max=" + cRevMax.toFixed(0)}</span>}
              {showEq && showLabels && <span className="flex items-center gap-1"><span className="inline-block w-3 h-3 rounded-full bg-slate-400"/>{"Текущий t=" + curTax + ", Rev=" + revCur.toFixed(0)}</span>}
              {showEq && showLabels && sDotTax !== null && <span className="flex items-center gap-1"><span className="inline-block w-3 h-3 rounded-full bg-orange-500"/>{"Ваш T_opt=" + sDotTax.toFixed(2)}</span>}
            </div>
          </div>
      );
    }

    // Стандартный график спроса/предложения (равновесие, излишки, DWL, налоги, эластичность)
    return (
        <div>
          <LineChart width={580} height={350} data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="price" label={{ value: "Цена (P)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
            <YAxis label={{ value: "Количество (Q)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
            <Tooltip formatter={(v: any, n: any) => [typeof v === "number" ? v.toFixed(1) : String(v ?? ""), n === "demand" ? "Спрос" : "Предложение"]} labelFormatter={(l) => "P = " + l} />
            <Legend formatter={(v) => (v === "demand" ? "Спрос" : "Предложение")} />
            <Line type="monotone" dataKey="supply" stroke="#22c55e" strokeWidth={2} dot={false} name="supply" />
            <Line type="monotone" dataKey="demand" stroke="#6366f1" strokeWidth={2} dot={false} name="demand" />
            {showEq && <ReferenceDot x={Math.round(eqP)} y={Math.round(eqQ)} r={5} fill="#94a3b8" stroke="#fff" strokeWidth={2} />}
            {showEq && correctDot && <ReferenceDot x={Math.round(correctDot.p)} y={Math.round(correctDot.q)} r={7} fill="#22c55e" stroke="#fff" strokeWidth={2} />}
            {showEq && studentDot && <ReferenceDot x={Math.round(studentDot.p)} y={Math.round(studentDot.q)} r={7} fill="#f97316" stroke="#fff" strokeWidth={2} />}
          </LineChart>
          {dotLegend("Равновесие: P*=" + eqP.toFixed(1) + ", Q*=" + eqQ.toFixed(1))}
        </div>
    );
  }


  const tabClass = (tab: string) =>
      "px-6 py-3 text-sm font-medium border-b-2 transition-colors " +
      (activeTab === tab
          ? "border-blue-600 text-blue-600"
          : "border-transparent text-gray-500 hover:text-gray-900");

  const diffColors: Record<string, string> = {
    "Лёгкая": "bg-green-100 text-green-700",
    "Средняя": "bg-yellow-100 text-yellow-700",
    "Сложная": "bg-red-100 text-red-700",
  };


  const isAnonymous = !localStorage.getItem("token");

  return (
      <div className="max-w-7xl mx-auto px-6 py-6">
        <div className="mb-4">
          <Link to="/tasks" className="text-sm text-gray-500 hover:text-gray-900 flex items-center gap-1 mb-3">
            <ArrowLeft size={16} /> Назад к задачам
          </Link>
          <h1 className="text-xl font-bold text-gray-900 mb-2">{desc.title}</h1>
          <div className="flex gap-2">
          <span className={"px-3 py-1 rounded-full text-xs font-medium " + (diffColors[desc.difficulty] || "bg-gray-100 text-gray-700")}>
            {desc.difficulty}
          </span>
            <span className="px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-700">
            {desc.topic}
          </span>
          </div>
        </div>

        {isAnonymous && (
          <div className="mb-4 bg-amber-50 border border-amber-200 rounded-lg px-4 py-3 text-sm text-amber-800">
            Вы не вошли в систему — отправки не сохранятся в личном прогрессе.{" "}
            <Link to="/login" className="font-medium underline hover:text-amber-900">Войти</Link>.
          </div>
        )}

        <div className="flex gap-6">
          {/* ─── Левая панель: условие / модель / график ─── */}
          <div className="flex-1 bg-white rounded-xl border border-gray-200">
            <div className="flex border-b border-gray-200">
              <button onClick={() => setActiveTab("condition")} className={tabClass("condition")}>Условие</button>
              <button onClick={() => setActiveTab("model")} className={tabClass("model")}>Модель</button>
              <button onClick={() => setActiveTab("graph")} className={tabClass("graph")}>График</button>
            </div>

            <div className="p-6">
              {activeTab === "condition" && (
                  <div className="text-gray-700 leading-relaxed">
                    <p className="mb-4">{desc.condition}</p>
                    {renderPublicTest()}
                  </div>
              )}

              {activeTab === "model" && (
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Формальное описание</h3>
                    <div className="bg-gray-50 rounded-lg p-4 mb-6 font-mono text-sm leading-relaxed">
                      {desc.model.split(" | ").map((line, i) => (
                          <p key={i} className="mb-1">{line}</p>
                      ))}
                    </div>

                    {publicTest && (
                        <div>
                          <h3 className="text-lg font-semibold mb-4">Параметры публичного теста</h3>
                          <div className="grid grid-cols-2 gap-4 mb-6">
                            {inputKeys
                                .filter((k) => k in publicTest)
                                .map((key) => (
                                    <div key={key} className="bg-gray-50 rounded-lg p-4">
                                      <div className="text-xs text-gray-500 mb-1">{fieldLabels[key] || key}</div>
                                      <div className="text-xl font-bold">{String(publicTest[key])}</div>
                                    </div>
                                ))}
                          </div>
                        </div>
                    )}
                  </div>
              )}

              {activeTab === "graph" && (
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Визуализация</h3>
                    {renderGraph()}
                    <div className="mt-4 flex gap-6">
                      <label className="flex items-center gap-2 text-sm text-gray-600">
                        <input type="checkbox" checked={showEq} onChange={(e) => setShowEq(e.target.checked)} className="rounded" />
                        Показывать равновесие
                      </label>
                      <label className="flex items-center gap-2 text-sm text-gray-600">
                        <input type="checkbox" checked={showLabels} onChange={(e) => setShowLabels(e.target.checked)} className="rounded" />
                        Показывать подписи
                      </label>
                    </div>
                  </div>
              )}
            </div>
          </div>

          {/* ─── Правая панель: редактор + кнопки ─── */}
          <div className="w-[480px] flex-shrink-0">
            <div className="bg-white rounded-xl border border-gray-200">
              <div className="px-4 py-3 border-b border-gray-200">
                <span className="text-sm font-medium text-gray-700">Ваше решение (Python)</span>
              </div>
              <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  spellCheck={false}
                  className="h-[350px] w-full resize-none rounded-b-xl border-0 bg-gray-950 px-4 py-3 font-mono text-sm leading-6 text-gray-100 outline-none"
              />
            </div>

            <div className="flex gap-3 mt-4">
              <button
                  onClick={handleSubmit}
                  disabled={loading}
                  className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
              >
                <Play size={16} />
                {loading ? "Проверяем..." : "Запустить и проверить"}
              </button>
              <button
                  onClick={handleReset}
                  className="flex items-center gap-2 px-4 py-2.5 border border-gray-300 text-gray-700 rounded-lg text-sm hover:bg-gray-50"
              >
                <RotateCcw size={16} /> Сбросить
              </button>
              <button
                  onClick={() => setShowHint(!showHint)}
                  className="flex items-center gap-2 px-4 py-2.5 border border-gray-300 text-gray-700 rounded-lg text-sm hover:bg-gray-50"
              >
                <Lightbulb size={16} /> Подсказка
              </button>
            </div>

            {showHint && (
                <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-sm text-yellow-800">
                  {desc.hint}
                </div>
            )}

            {verdict && (
                <div className={"mt-4 border rounded-lg p-4 " + getVerdictStyle(verdict)}>
                  <div className="font-semibold">{getVerdictText(verdict)}</div>
                  {verdict !== "ERROR" && (
                    <div className="text-sm mt-1">{"Пройдено тестов: " + passed + " из " + total}</div>
                  )}

                  {verdict === "ERROR" && failMessage && (
                      <div className="text-sm mt-2">{failMessage}</div>
                  )}

                  {verdict !== "AC" && verdict !== "ERROR" && failTestIndex !== null && (
                      <div className="mt-3 pt-3 border-t border-current/10 text-sm space-y-3">
                        <div className="font-medium">{"Первый провал: тест #" + (failTestIndex + 1)}</div>

                        {failInput && (
                            <div className="bg-white/60 rounded p-3">
                              <div className="text-xs font-semibold mb-2 uppercase tracking-wide opacity-70">Входные данные</div>
                              <div className="grid grid-cols-2 gap-x-4 gap-y-1 font-mono text-xs">
                                {Object.entries(failInput).map(([k, v]) => (
                                    <div key={k} className="flex justify-between">
                                      <span className="opacity-70">{k}:</span>
                                      <span className="font-semibold">{String(v)}</span>
                                    </div>
                                ))}
                              </div>
                            </div>
                        )}

                        {failExpected && failGot && (
                            <div className="bg-white/60 rounded p-3">
                              <div className="text-xs font-semibold mb-2 uppercase tracking-wide opacity-70">Результат</div>
                              <table className="w-full text-xs font-mono">
                                <thead>
                                <tr className="opacity-70">
                                  <td className="pb-1">Поле</td>
                                  <td className="pb-1 text-right">Ожидалось</td>
                                  <td className="pb-1 text-right">Получено</td>
                                </tr>
                                </thead>
                                <tbody>
                                {Object.keys(failExpected).map((key) => {
                                  const exp = failExpected[key];
                                  const got = failGot[key];
                                  const match = exp !== undefined && got !== undefined && Math.abs(exp - got) < 1e-4;
                                  return (
                                      <tr key={key} className={match ? "" : "font-bold"}>
                                        <td className="py-0.5">{key}</td>
                                        <td className="py-0.5 text-right">{exp !== undefined ? exp.toFixed(4) : "—"}</td>
                                        <td className={"py-0.5 text-right " + (match ? "" : "text-red-700")}>{got !== undefined ? got.toFixed(4) : "—"}</td>
                                      </tr>
                                  );
                                })}
                                </tbody>
                              </table>
                            </div>
                        )}

                        {!failExpected && failMessage && (
                            <div>{"Причина: " + failMessage}</div>
                        )}
                      </div>
                  )}
                </div>
            )}

            {/* ── Submission history ── */}
            {submissions.length > 0 && (
                <div className="mt-4">
                  <button
                      onClick={() => setShowHistory(!showHistory)}
                      className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900"
                  >
                    <span className={"transition-transform " + (showHistory ? "rotate-90" : "")}>▶</span>
                    {"История попыток (" + submissions.length + ")"}
                  </button>
                  {showHistory && (
                      <div className="mt-2 rounded-lg border border-gray-200 overflow-hidden">
                        <table className="w-full text-xs">
                          <thead className="bg-gray-50 text-gray-500 uppercase tracking-wide">
                          <tr>
                            <th className="px-3 py-2 text-left">Вердикт</th>
                            <th className="px-3 py-2 text-right">Тесты</th>
                            <th className="px-3 py-2 text-right">Время</th>
                          </tr>
                          </thead>
                          <tbody>
                          {submissions.map((s) => (
                              <tr key={s.id} className="border-t border-gray-100">
                                <td className={"px-3 py-1.5 font-semibold " +
                                    (s.verdict === "AC" ? "text-green-600" :
                                        s.verdict === "WA" ? "text-red-600" :
                                            s.verdict === "TLE" ? "text-yellow-600" : "text-gray-600")}>
                                  {s.verdict}
                                </td>
                                <td className="px-3 py-1.5 text-right text-gray-600">{s.passed + "/" + s.total}</td>
                                <td className="px-3 py-1.5 text-right text-gray-400">
                                  {s.created_at ? new Date(s.created_at).toLocaleString("ru", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }) : "—"}
                                </td>
                              </tr>
                          ))}
                          </tbody>
                        </table>
                      </div>
                  )}
                </div>
            )}
          </div>
        </div>
      </div>
  );
}

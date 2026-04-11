import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { ArrowLeft, Play, RotateCcw, Lightbulb } from "lucide-react";
import Editor from "@monaco-editor/react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ReferenceDot, ReferenceLine
} from "recharts";


const taskInputKeys: Record<string, string[]> = {
  "equilibrium_linear_v1": ["a", "b", "c", "d", "mode", "t"],
  "surplus_calc_v1": ["a", "b", "c", "d"],
  "dwl_tax_v1": ["a", "b", "c", "d", "t", "mode"],
  "elasticity_v1": ["a", "b", "p"],
  "price_ceiling_v1": ["a", "b", "c", "d", "p_ceil"],
  "tax_revenue_v1": ["a", "b", "c", "d", "t"],
  "demand_shift_v1": ["a", "b", "c", "d", "a_new"],
};

const taskOutputKeys: Record<string, string[]> = {
  "equilibrium_linear_v1": ["p_eq", "q_eq"],
  "surplus_calc_v1": ["cs", "ps", "total_surplus"],
  "dwl_tax_v1": ["p_buyer", "p_seller", "q_new", "cs_after", "ps_after", "gov_revenue", "dwl", "buyer_share", "seller_share"],
  "elasticity_v1": ["elasticity", "revenue", "elastic_type"],
  "price_ceiling_v1": ["p_actual", "q_demanded", "q_supplied", "q_traded", "shortage", "binding"],
  "tax_revenue_v1": ["p_buyer", "p_seller", "q_tax", "tax_revenue", "price_increase", "quantity_decrease"],
  "demand_shift_v1": ["p_old", "q_old", "p_new", "q_new", "delta_p", "delta_q"],
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
  gov_revenue: "Gov Revenue (налоговые поступления)",
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
    "    # Napishite reshenie",
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
    "    # Napishite reshenie",
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
    "    # Napishite reshenie",
    "    p_buyer = 0.0",
    "    p_seller = 0.0",
    "    q_new = 0.0",
    "    cs_after = 0.0",
    "    ps_after = 0.0",
    "    gov_revenue = 0.0",
    "    dwl = 0.0",
    "    buyer_share = 0.0",
    "    seller_share = 0.0",
    "",
    "    return {",
    "        'p_buyer': p_buyer, 'p_seller': p_seller,",
    "        'q_new': q_new, 'cs_after': cs_after,",
    "        'ps_after': ps_after, 'gov_revenue': gov_revenue,",
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
    "    # Napishite reshenie",
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
    "    # Napishite reshenie",
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
    "    # Napishite reshenie",
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
    "    # Napishite reshenie",
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
    title: "Налог на сладкие напитки",
    difficulty: "Средняя",
    topic: "Излишки",
    condition: "Минздрав предлагает ввести налог на сладкие газированные напитки, " +
        "чтобы снизить потребление сахара. Минфин хочет знать, сколько денег принесёт этот налог в бюджет. " +
        "Производители боятся падения продаж. Посчитайте, как изменится цена для покупателей и продавцов, " +
        "насколько сократится объём продаж, и какую сумму получит государство.",
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
};

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
  const [failField, setFailField] = useState<string | null>(null);
  const [failInput, setFailInput] = useState<Record<string, any> | null>(null);
  const [failExpected, setFailExpected] = useState<Record<string, number> | null>(null);
  const [failGot, setFailGot] = useState<Record<string, number> | null>(null);
  const [showHint, setShowHint] = useState(false);
  const [showEq, setShowEq] = useState(true);
  const [showLabels, setShowLabels] = useState(true);
  const [publicTest, setPublicTest] = useState<Record<string, any> | null>(null);

  const info = taskDescriptions[taskId || ""];
  const fallback = taskDescriptions["equilibrium_linear_v1"];
  const desc = info || fallback;

  const inputKeys = taskInputKeys[taskId || ""] || [];
  const outputKeys = taskOutputKeys[taskId || ""] || [];

  useEffect(() => {
    setCode(codeTemplates[taskId || ""] || "def solve(params):\n    pass");
    setVerdict(null);
    setFailMessage("");
    setFailTestIndex(null);
    setFailField(null);
    setFailInput(null);
    setFailExpected(null);
    setFailGot(null);
    setShowHint(false);
    setPublicTest(null);
    fetch("/api/v1/tasks/" + taskId)
        .then((res) => res.json())
        .then((data) => {
          if (data.public_test) setPublicTest(data.public_test);
        })
        .catch(() => {});
  }, [taskId]);

  async function handleSubmit() {
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
      const data = await res.json();
      if (data.verdict) {
        setVerdict(data.verdict);
        setPassed(data.passed);
        setTotal(data.total);
        setFailMessage(data.message || "");
        setFailTestIndex(data.failed_test_index ?? null);
        setFailField(data.failed_field ?? null);
        setFailInput(data.failed_input ?? null);
        setFailExpected(data.failed_expected ?? null);
        setFailGot(data.failed_got ?? null);
      } else {
        setVerdict("ERROR");
      }
    } catch {
      setVerdict("ERROR");
    }
    setLoading(false);
  }

  function handleReset() {
    setCode(codeTemplates[taskId || ""] || "def solve(params):\n    pass");
    setVerdict(null);
    setFailMessage("");
    setFailTestIndex(null);
    setFailField(null);
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

    const outputData = outputKeys
        .filter((k) => k in publicTest)
        .map((k) => ({ key: k, value: publicTest[k] }));

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

    const a = publicTest.a;
    const b = publicTest.b;
    if (taskId === "elasticity_v1") {
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
              {showEq && (
                  <ReferenceDot x={Math.round(p)} y={Math.round(pointQ)} r={6} fill="#ef4444" stroke="#fff" strokeWidth={2} />
              )}
            </LineChart>
            {showEq && showLabels && (
                <div className="mt-2 text-sm text-gray-600">
                  {"Точка: P = " + p + ", Q = " + pointQ.toFixed(1) + ", Ed = " + ed.toFixed(2)}
                </div>
            )}
          </div>
      );
    }

    if (taskId === "demand_shift_v1") {
      const c = publicTest.c;
      const d = publicTest.d;
      const aNew = publicTest.a_new;
      const chartData = buildDemandShiftChart(a, b, c, d, aNew);
      const pOld = (a - c) / (b + d);
      const qOld = a - b * pOld;
      const pNew = (aNew - c) / (b + d);
      const qNew = aNew - b * pNew;
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
              {showEq && (
                  <ReferenceDot x={Math.round(pOld)} y={Math.round(qOld)} r={5} fill="#6366f1" stroke="#fff" strokeWidth={2} />
              )}
              {showEq && (
                  <ReferenceDot x={Math.round(pNew)} y={Math.round(qNew)} r={5} fill="#3b82f6" stroke="#fff" strokeWidth={2} />
              )}
            </LineChart>
            {showEq && showLabels && (
                <div className="mt-2 text-sm text-gray-600">
                  {"Старое: P = " + pOld.toFixed(1) + ", Q = " + qOld.toFixed(1) +
                      " | Новое: P = " + pNew.toFixed(1) + ", Q = " + qNew.toFixed(1)}
                </div>
            )}
          </div>
      );
    }

    const c = publicTest.c;
    const dd = publicTest.d;
    const chartData = buildChartData(a, b, c, dd);
    const eqP = (a - c) / (b + dd);
    const eqQ = a - b * eqP;

    if (taskId === "price_ceiling_v1") {
      const pCeil = publicTest.p_ceil;
      return (
          <div>
            <LineChart width={580} height={350} data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="price" label={{ value: "Цена (P)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
              <YAxis label={{ value: "Количество (Q)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
              <Tooltip
                  formatter={(value: number, name: string) => [
                    value.toFixed(1),
                    name === "demand" ? "Спрос" : "Предложение",
                  ]}
                  labelFormatter={(label) => "P = " + label}
              />
              <Legend formatter={(value) => (value === "demand" ? "Спрос" : "Предложение")} />
              <Line type="monotone" dataKey="supply" stroke="#22c55e" strokeWidth={2} dot={false} name="supply" />
              <Line type="monotone" dataKey="demand" stroke="#6366f1" strokeWidth={2} dot={false} name="demand" />
              <ReferenceLine y={0} x={pCeil} stroke="#f97316" strokeDasharray="8 4" strokeWidth={2} label={{ value: "Потолок P=" + pCeil, position: "top", fill: "#f97316", fontSize: 12 }} />
              {showEq && (
                  <ReferenceDot x={Math.round(eqP)} y={Math.round(eqQ)} r={6} fill="#ef4444" stroke="#fff" strokeWidth={2} />
              )}
            </LineChart>
            {showEq && showLabels && (
                <div className="mt-2 text-sm text-gray-600">
                  {"Равновесие: P* = " + eqP.toFixed(1) + ", Q* = " + eqQ.toFixed(1) +
                      " | Потолок: " + pCeil + (pCeil < eqP ? " (действует, дефицит)" : " (не действует)")}
                </div>
            )}
          </div>
      );
    }

    return (
        <div>
          <LineChart width={580} height={350} data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="price" label={{ value: "Цена (P)", position: "insideBottom", offset: -5 }} tick={{ fontSize: 12 }} />
            <YAxis label={{ value: "Количество (Q)", angle: -90, position: "insideLeft", offset: 10 }} tick={{ fontSize: 12 }} />
            <Tooltip
                formatter={(value: number, name: string) => [
                  value.toFixed(1),
                  name === "demand" ? "Спрос" : "Предложение",
                ]}
                labelFormatter={(label) => "P = " + label}
            />
            <Legend formatter={(value) => (value === "demand" ? "Спрос" : "Предложение")} />
            <Line type="monotone" dataKey="supply" stroke="#22c55e" strokeWidth={2} dot={false} name="supply" />
            <Line type="monotone" dataKey="demand" stroke="#6366f1" strokeWidth={2} dot={false} name="demand" />
            {showEq && (
                <ReferenceDot x={Math.round(eqP)} y={Math.round(eqQ)} r={6} fill="#ef4444" stroke="#fff" strokeWidth={2} />
            )}
          </LineChart>
          {showEq && showLabels && (
              <div className="mt-2 text-sm text-gray-600">
                {"Равновесие: P* = " + eqP.toFixed(1) + ", Q* = " + eqQ.toFixed(1)}
              </div>
          )}
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
              <Editor
                  height="350px"
                  defaultLanguage="python"
                  value={code}
                  onChange={(val) => setCode(val || "")}
                  theme="vs-light"
                  options={{
                    minimap: { enabled: false },
                    fontSize: 14,
                    scrollBeyondLastLine: false,
                    lineNumbers: "on",
                    renderLineHighlight: "none",
                    padding: { top: 12 },
                  }}
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
                  <div className="text-sm mt-1">{"Пройдено тестов: " + passed + " из " + total}</div>

                  {verdict !== "AC" && failTestIndex !== null && (
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
          </div>
        </div>
      </div>
  );
}

import { useState, useRef, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { ArrowLeft, Play, RotateCcw, Lightbulb } from "lucide-react";

const defaultCode = `def solve(params):
    a = float(params["a"])
    b = float(params["b"])
    c = float(params["c"])
    d = float(params["d"])
    mode = params["mode"]
    t = float(params.get("t", 0.0))

    # Напишите решение здесь
    p_eq = 0.0
    q_eq = 0.0

    return {"p_eq": p_eq, "q_eq": q_eq}`;

export default function SolvePage() {
  const { taskId } = useParams();
  const [activeTab, setActiveTab] = useState("condition");
  const [code, setCode] = useState(defaultCode);
  const [verdict, setVerdict] = useState<string | null>(null);
  const [passed, setPassed] = useState(0);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const editorRef = useRef<any>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Загрузка Monaco Editor
  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs/loader.js";
    script.onload = () => {
      (window as any).require.config({
        paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs" }
      });
      (window as any).require(["vs/editor/editor.main"], () => {
        if (containerRef.current && !editorRef.current) {
          editorRef.current = (window as any).monaco.editor.create(containerRef.current, {
            value: code,
            language: "python",
            theme: "vs",
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: "on",
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
          });
          editorRef.current.onDidChangeModelContent(() => {
            setCode(editorRef.current.getValue());
          });
        }
      });
    };
    document.head.appendChild(script);
    return () => { if (editorRef.current) editorRef.current.dispose(); };
  }, []);

  async function handleSubmit() {
    setLoading(true);
    setVerdict(null);
    try {
      const res = await fetch("/api/v1/submissions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task_id: taskId, user_code: code }),
      });
      const data = await res.json();
      setVerdict(data.verdict);
      setPassed(data.passed);
      setTotal(data.total);
    } catch {
      setVerdict("ERROR");
    }
    setLoading(false);
  }

  function handleReset() {
    setCode(defaultCode);
    if (editorRef.current) editorRef.current.setValue(defaultCode);
    setVerdict(null);
  }

  function verdictColor(v: string) {
    if (v === "AC") return "text-green-600 bg-green-50 border-green-200";
    if (v === "WA") return "text-red-600 bg-red-50 border-red-200";
    if (v === "TLE") return "text-yellow-600 bg-yellow-50 border-yellow-200";
    return "text-red-600 bg-red-50 border-red-200";
  }

  function verdictText(v: string) {
    if (v === "AC") return "Accepted!";
    if (v === "WA") return "Wrong Answer";
    if (v === "TLE") return "Time Limit Exceeded";
    if (v === "RE") return "Runtime Error";
    return "Connection Error";
  }

  const tabClass = (tab: string) =>
    "px-6 py-3 text-sm font-medium border-b-2 " +
    (activeTab === tab ? "border-blue-600 text-blue-600" : "border-transparent text-gray-500 hover:text-gray-900");

  return (
    <div className="max-w-7xl mx-auto px-6 py-6">
      {/* Назад + теги */}
      <div className="mb-4">
        <Link to="/tasks" className="text-sm text-gray-500 hover:text-gray-900 flex items-center gap-1 mb-3">
          <ArrowLeft size={16} /> Назад к задачам
        </Link>
        <div className="flex gap-2">
          <span className="px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">Lёгкая</span>
          <span className="px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-700">Равновесие</span>
        </div>
      </div>

      {/* Две колонки */}
      <div className="flex gap-6">

        {/* Левая колонка */}
        <div className="flex-1 bg-white rounded-xl border border-gray-200">
          <div className="flex border-b border-gray-200">
            <button onClick={() => setActiveTab("condition")} className={tabClass("condition")}>Условие</button>
            <button onClick={() => setActiveTab("model")} className={tabClass("model")}>Модель</button>
            <button onClick={() => setActiveTab("graph")} className={tabClass("graph")}>График</button>
          </div>

          <div className="p-6">
            {activeTab === "condition" && (
              <div className="text-gray-700 leading-relaxed">
                <p className="mb-4">
                  На местном рынке продаются яблоки. Спрос на яблоки описывается линейной
                  функцией: чем выше цена, тем меньше покупатели готовы купить. Предложение
                  также линейно: чем выше цена, тем больше фермеры готовы продать.
                </p>
                <p className="mb-4">
                  Исследования показали, что при нулевой цене покупатели готовы взять 100 кг
                  яблок, а каждое увеличение цены на 1 рубль снижает спрос на 2 кг. Фермеры
                  готовы предложить 20 кг при нулевой цене, и каждый дополнительный рубль
                  мотивирует их увеличить предложение на 1 кг.
                </p>
                <p className="mb-4">
                  <strong>Задача:</strong> Напишите функцию, которая найдёт равновесную цену
                  и количество на этом рынке по заданным параметрам функций спроса и предложения.
                </p>
                <p className="mb-4">
                  Функция должна возвращать словарь с двумя значениями:
                  <code className="bg-gray-100 px-2 py-0.5 rounded text-sm mx-1">(p_eq, q_eq)</code>,
                  где p_eq — равновесная цена, q_eq — равновесное количество.
                </p>
                <p className="text-sm text-gray-500">
                  Рынок может работать в трёх режимах: без вмешательства (none),
                  с налогом (tax), с субсидией (subsidy). Параметр t задает размер налога/субсидии.
                </p>
              </div>
            )}

            {activeTab === "model" && (
              <div>
                <h3 className="text-lg font-semibold mb-4">Формальное описание</h3>
                <div className="bg-gray-50 rounded-lg p-4 mb-6 font-mono text-sm">
                  <p>Спрос: Qᵈ(P) = a − b·P</p>
                  <p>Предложение: Qₛ(P) = c + d·P</p>
                </div>

                <h3 className="text-lg font-semibold mb-4">Параметры для текущей задачи</h3>
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="border border-gray-200 rounded-lg p-4">
                    <div className="text-xs text-gray-500 mb-1">a (спрос при P=0)</div>
                    <div className="text-xl font-semibold">100</div>
                  </div>
                  <div className="border border-gray-200 rounded-lg p-4">
                    <div className="text-xs text-gray-500 mb-1">b (наклон спроса)</div>
                    <div className="text-xl font-semibold">2</div>
                  </div>
                  <div className="border border-gray-200 rounded-lg p-4">
                    <div className="text-xs text-gray-500 mb-1">c (предложение при P=0)</div>
                    <div className="text-xl font-semibold">20</div>
                  </div>
                  <div className="border border-gray-200 rounded-lg p-4">
                    <div className="text-xs text-gray-500 mb-1">d (наклон предложения)</div>
                    <div className="text-xl font-semibold">1</div>
                  </div>
                </div>

                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <p className="text-sm">
                    <strong>Подсказка:</strong> В равновесии спрос равен предложению:
                    Qᵈ(P*) = Qₛ(P*)
                  </p>
                </div>
              </div>
            )}

            {activeTab === "graph" && (
              <div>
                <h3 className="text-lg font-semibold mb-4">Визуализация</h3>
                <p className="text-gray-500 text-sm">График будет доступен после отправки решения</p>
              </div>
            )}
          </div>
        </div>

        {/* Правая колонка — редактор */}
        <div className="w-[480px] flex-shrink-0">
          <div className="bg-white rounded-xl border border-gray-200">
            <div className="px-4 py-3 border-b border-gray-200 text-sm font-medium text-gray-700">
              Ваше решение (Python)
            </div>
            <div ref={containerRef} className="h-[400px]"></div>
          </div>

          {/* Кнопки */}
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
              className="flex items-center gap-2 px-4 py-2.5 border border-gray-300 rounded-lg text-sm hover:bg-gray-50"
            >
              <RotateCcw size={16} /> Сбросить
            </button>
            <button
              onClick={() => setShowHint(!showHint)}
              className="flex items-center gap-2 px-4 py-2.5 border border-gray-300 rounded-lg text-sm hover:bg-gray-50"
            >
              <Lightbulb size={16} /> Подсказки
            </button>
          </div>

          {/* Подсказка */}
          {showHint && (
            <div className="mt-3 bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-sm">
              <p className="mb-2">В равновесии спрос равен предложению: a − b·P = c + d·P</p>
              <p>Решите относительно P: P* = (a − c) / (b + d)</p>
            </div>
          )}

          {/* Вердикт */}
          {verdict && (
            <div className={"mt-3 border rounded-lg p-4 " + verdictColor(verdict)}>
              <div className="font-semibold">{verdictText(verdict)}</div>
              {verdict !== "ERROR" && (
                <div className="text-sm mt-1">Пройдено тестов: {passed} из {total}</div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

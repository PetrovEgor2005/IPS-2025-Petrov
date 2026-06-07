// Каталог задач. Тут грузим список с бекенда, показываем фильтры и карточки.
// Если пользователь залогинен — параллельно подтягиваем его прогресс и красим иконки.

import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { CheckCircle2, Clock, Circle } from "lucide-react";

// подписи тем — приходят с бекенда в техническом виде ("equilibrium"), а на UI показываем по-русски
const TOPIC_LABELS: Record<string, string> = {
  equilibrium: "Равновесие",
  welfare: "Благосостояние",
  elasticity: "Эластичность",
  taxes_subsidies: "Налоги/субсидии",
  aggregation: "Агрегирование",
  inverse: "Обратные функции",
  monopoly: "Монополия",
  trade: "Международная торговля",
  externality: "Внешние эффекты",
};

const DIFF_LABELS: Record<number, string> = { 1: "Лёгкая", 2: "Средняя", 3: "Сложная" };

type ApiTask = { id: string; title: string; topic: string; difficulty: number };

function StatusIcon({ status }: { status: string }) {
  if (status === "solved") return <CheckCircle2 size={20} className="text-green-500" />;
  if (status === "in_progress") return <Clock size={20} className="text-yellow-500" />;
  return <Circle size={20} className="text-gray-300" />;
}

function DifficultyBadge({ difficulty }: { difficulty: number }) {
  const label = DIFF_LABELS[difficulty] ?? "Средняя";
  let c = "bg-green-100 text-green-700";
  if (difficulty === 2) c = "bg-yellow-100 text-yellow-700";
  if (difficulty === 3) c = "bg-red-100 text-red-700";
  return <span className={"px-3 py-1 rounded-full text-xs font-medium " + c}>{label}</span>;
}

export default function TaskCatalog() {
  const [tasks, setTasks] = useState<ApiTask[]>([]);
  const [topicFilter, setTopicFilter] = useState("all");
  const [difficultyFilter, setDifficultyFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");
  const [taskStatuses, setTaskStatuses] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retry, setRetry] = useState(0);

  // подгружаем список задач при открытии страницы и при нажатии "повторить"
  // cancelled нужен на случай, если пользователь ушёл со страницы во время запроса
  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    fetch("/api/v1/tasks")
      .then(r => {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then((data: ApiTask[]) => {
        if (!cancelled) setTasks(data);
      })
      .catch(err => {
        if (!cancelled) setError(err.message || "Ошибка загрузки");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, [retry]);

  // отдельный запрос за прогрессом — только если залогинены, иначе показываем все задачи как не начатые
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setTaskStatuses({});
      return;
    }
    fetch("/api/v1/submissions/my-progress", { headers: { Authorization: "Bearer " + token } })
      .then(r => r.ok ? r.json() : {})
      .then(data => setTaskStatuses(data))
      .catch(() => setTaskStatuses({}));
  }, [retry]);

  function getStatus(id: string) { return taskStatuses[id] || "not_started"; }

  const tw = tasks.map(t => ({ ...t, status: getStatus(t.id) }));
  const solved = tw.filter(t => t.status === "solved").length;
  const inProg = tw.filter(t => t.status === "in_progress").length;
  const notStart = tw.filter(t => t.status === "not_started").length;
  const total = tw.length;
  const pct = total > 0 ? Math.round((solved / total) * 100) : 0;

  const topics = [...new Set(tasks.map(t => t.topic))];

  let filtered = tw;
  if (topicFilter !== "all") filtered = filtered.filter(t => t.topic === topicFilter);
  if (difficultyFilter !== "all") filtered = filtered.filter(t => String(t.difficulty) === difficultyFilter);
  if (statusFilter !== "all") filtered = filtered.filter(t => t.status === statusFilter);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-6 py-10">
        <h1 className="text-3xl font-bold mb-8">Задачи</h1>
        <div className="bg-white rounded-xl border border-gray-200 p-12 text-center text-gray-500">
          Загрузка…
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-6 py-10">
        <h1 className="text-3xl font-bold mb-8">Задачи</h1>
        <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-red-700">
          <p className="font-medium mb-2">Не удалось загрузить список задач</p>
          <p className="text-sm mb-4">{error}</p>
          <button
            onClick={() => setRetry(r => r + 1)}
            className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700"
          >
            Повторить
          </button>
        </div>
      </div>
    );
  }

  return (
      <div className="max-w-7xl mx-auto px-6 py-10">
        <h1 className="text-3xl font-bold mb-8">Задачи</h1>

        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-sm text-gray-600">Решено {solved} из {total}</span>
            <span className="text-sm font-medium">{pct}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5 mb-4">
            <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: pct + "%" }} />
          </div>
          <div className="text-sm text-gray-500">
            В работе: <strong>{inProg}</strong> &nbsp; Не начато: <strong>{notStart}</strong>
          </div>
        </div>

        <div className="flex gap-8">
          <div className="w-56 flex-shrink-0">
            <div className="bg-white rounded-xl border border-gray-200 p-5">
              <h3 className="font-semibold mb-4">Фильтры</h3>

              <label className="block text-sm text-gray-600 mb-1">Тема</label>
              <select value={topicFilter} onChange={e => setTopicFilter(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm mb-4">
                <option value="all">Все темы</option>
                {topics.map(t => (
                    <option key={t} value={t}>{TOPIC_LABELS[t] ?? t}</option>
                ))}
              </select>

              <label className="block text-sm text-gray-600 mb-1">Сложность</label>
              <select value={difficultyFilter} onChange={e => setDifficultyFilter(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm mb-4">
                <option value="all">Любая</option>
                <option value="1">Лёгкая</option>
                <option value="2">Средняя</option>
                <option value="3">Сложная</option>
              </select>

              <label className="block text-sm text-gray-600 mb-1">Статус</label>
              <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm">
                <option value="all">Все</option>
                <option value="solved">Решено</option>
                <option value="in_progress">В работе</option>
                <option value="not_started">Не начато</option>
              </select>
            </div>
          </div>

          <div className="flex-1">
            <table className="w-full">
              <thead>
                <tr className="text-left text-xs text-gray-500 uppercase">
                  <th className="pb-3 w-16">Статус</th>
                  <th className="pb-3">Название</th>
                  <th className="pb-3">Тема</th>
                  <th className="pb-3">Сложность</th>
                  <th className="pb-3 w-24">Действие</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map(task => (
                    <tr key={task.id} className="border-t border-gray-100">
                      <td className="py-4"><StatusIcon status={task.status} /></td>
                      <td className="py-4 font-medium">{task.title}</td>
                      <td className="py-4 text-sm text-gray-500">{TOPIC_LABELS[task.topic] ?? task.topic}</td>
                      <td className="py-4"><DifficultyBadge difficulty={task.difficulty} /></td>
                      <td className="py-4">
                        <Link to={"/tasks/" + task.id}
                          className="px-4 py-1.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700">
                          Решать
                        </Link>
                      </td>
                    </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
  );
}

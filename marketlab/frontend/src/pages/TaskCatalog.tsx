import { useState } from "react";
import { Link } from "react-router-dom";
import { CheckCircle2, Clock, Circle } from "lucide-react";

const tasks = [
  { id: "equilibrium_linear_v1", title: "Поиск равновесия на рынке яблок", topic: "Равновесие", difficulty: "Лёгкая", status: "not_started" },
];

function StatusIcon({ status }: { status: string }) {
  if (status === "solved") return <CheckCircle2 size={20} className="text-green-500" />;
  if (status === "in_progress") return <Clock size={20} className="text-yellow-500" />;
  return <Circle size={20} className="text-gray-300" />;
}

function DifficultyBadge({ difficulty }: { difficulty: string }) {
  let colors = "bg-green-100 text-green-700";
  if (difficulty === "Средняя") colors = "bg-yellow-100 text-yellow-700";
  if (difficulty === "Сложная") colors = "bg-red-100 text-red-700";
  return <span className={"px-3 py-1 rounded-full text-xs font-medium " + colors}>{difficulty}</span>;
}

export default function TaskCatalog() {
  const [topicFilter, setTopicFilter] = useState("all");
  const [difficultyFilter, setDifficultyFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");

  const solved = tasks.filter(t => t.status === "solved").length;
  const inProgress = tasks.filter(t => t.status === "in_progress").length;
  const notStarted = tasks.filter(t => t.status === "not_started").length;
  const total = tasks.length;
  const percent = total > 0 ? Math.round((solved / total) * 100) : 0;

  let filtered = tasks;
  if (topicFilter !== "all") filtered = filtered.filter(t => t.topic === topicFilter);
  if (difficultyFilter !== "all") filtered = filtered.filter(t => t.difficulty === difficultyFilter);
  if (statusFilter !== "all") filtered = filtered.filter(t => t.status === statusFilter);

  const topics = [...new Set(tasks.map(t => t.topic))];

  return (
    <div className="max-w-7xl mx-auto px-6 py-10">
      <h1 className="text-3xl font-bold mb-8">Задачи</h1>

      {/* Прогресс */}
      <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
        <div className="flex justify-between mb-2">
          <span className="text-sm text-gray-600">Решено {solved} из {total}</span>
          <span className="text-sm font-medium">{percent}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2.5 mb-4">
          <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: percent + "%" }}></div>
        </div>
        <div className="text-sm text-gray-500">
          В работе: <strong>{inProgress}</strong> &nbsp; Не начато: <strong>{notStarted}</strong>
        </div>
      </div>

      {/* Фильтры + таблица */}
      <div className="flex gap-8">
        <div className="w-56 flex-shrink-0">
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h3 className="font-semibold mb-4">Фильтры</h3>

            <label className="block text-sm text-gray-600 mb-1">Тема</label>
            <select
              value={topicFilter}
              onChange={e => setTopicFilter(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm mb-4"
            >
              <option value="all">Все темы</option>
              {topics.map(t => <option key={t} value={t}>{t}</option>)}
            </select>

            <label className="block text-sm text-gray-600 mb-1">Сложность</label>
            <select
              value={difficultyFilter}
              onChange={e => setDifficultyFilter(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm mb-4"
            >
              <option value="all">Любая</option>
              <option value="Лёгкая">Лёгкая</option>
              <option value="Средняя">Средняя</option>
              <option value="Сложная">Сложная</option>
            </select>

            <label className="block text-sm text-gray-600 mb-1">Статус</label>
            <select
              value={statusFilter}
              onChange={e => setStatusFilter(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
            >
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
                  <td className="py-4 text-sm text-gray-500">{task.topic}</td>
                  <td className="py-4"><DifficultyBadge difficulty={task.difficulty} /></td>
                  <td className="py-4">
                    <Link
                      to={"/tasks/" + task.id}
                      className="px-4 py-1.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700"
                    >
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

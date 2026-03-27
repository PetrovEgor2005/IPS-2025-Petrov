import { Link } from "react-router-dom";
import { Sparkles, Code2, CheckCircle2, BarChart3, Globe2, BookOpen } from "lucide-react";

export default function LandingPage() {
  return (
    <div>
      {/* Главный блок */}
      <section className="bg-white">
        <div className="max-w-4xl mx-auto px-6 py-24 text-center">
          <h1 className="text-5xl font-extrabold text-gray-900 mb-4">МаркетЛаб</h1>
          <p className="text-lg text-gray-500 mb-10">
            Учись анализировать конкурентный рынок, решая задачи на Python
          </p>
          <div className="flex justify-center gap-4">
            <Link
              to="/tasks"
              className="px-8 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700"
            >
              Начать решать
            </Link>
            <a
              href="#how"
              className="px-8 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50"
            >
              Как это работает
            </a>
          </div>
        </div>
      </section>

      {/* Функционал */}
      <section className="max-w-7xl mx-auto px-6 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Функционал</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <Sparkles className="text-blue-600 mb-4" size={28} />
            <h3 className="text-lg font-semibold mb-2">Автогенерация задач</h3>
            <p className="text-gray-500 text-sm">Уникальные задачи с разными параметрами для каждого решения</p>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <Code2 className="text-blue-600 mb-4" size={28} />
            <h3 className="text-lg font-semibold mb-2">Python-код прямо в браузере</h3>
            <p className="text-gray-500 text-sm">Встроенный редактор кода с подсветкой синтаксиса</p>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <CheckCircle2 className="text-blue-600 mb-4" size={28} />
            <h3 className="text-lg font-semibold mb-2">Автопроверка через тесты</h3>
            <p className="text-gray-500 text-sm">Мгновенная проверка решений через систему Judge</p>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <BarChart3 className="text-blue-600 mb-4" size={28} />
            <h3 className="text-lg font-semibold mb-2">Интерактивные графики</h3>
            <p className="text-gray-500 text-sm">Визуализация спроса, предложения и равновесия</p>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <Globe2 className="text-blue-600 mb-4" size={28} />
            <h3 className="text-lg font-semibold mb-2">Жизненные условия задач</h3>
            <p className="text-gray-500 text-sm">Реалистичные экономические сценарии через нейросеть</p>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <BookOpen className="text-blue-600 mb-4" size={28} />
            <h3 className="text-lg font-semibold mb-2">Теория и практика</h3>
            <p className="text-gray-500 text-sm">Каждая задача включает формальную модель и описание</p>
          </div>

        </div>
      </section>

      {/* Как проходит решение */}
      <section id="how" className="bg-white">
        <div className="max-w-5xl mx-auto px-6 py-16">
          <h2 className="text-3xl font-bold text-center mb-12">Как проходит решение</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-center">

            <div>
              <div className="w-16 h-16 rounded-full bg-blue-100 text-blue-600 text-2xl font-bold flex items-center justify-center mx-auto mb-4">1</div>
              <h3 className="text-lg font-semibold mb-2">Выбери задачу</h3>
              <p className="text-gray-500 text-sm">Из каталога по темам и сложности</p>
            </div>

            <div>
              <div className="w-16 h-16 rounded-full bg-blue-100 text-blue-600 text-2xl font-bold flex items-center justify-center mx-auto mb-4">2</div>
              <h3 className="text-lg font-semibold mb-2">Напиши решение на Python</h3>
              <p className="text-gray-500 text-sm">Используй встроенный редактор кода</p>
            </div>

            <div>
              <div className="w-16 h-16 rounded-full bg-blue-100 text-blue-600 text-2xl font-bold flex items-center justify-center mx-auto mb-4">3</div>
              <h3 className="text-lg font-semibold mb-2">Получи проверку и графики</h3>
              <p className="text-gray-500 text-sm">Мгновенный фидбек и визуализация</p>
            </div>

          </div>
        </div>
      </section>

      {/* Футер */}
      <footer className="border-t border-gray-200 bg-white">
        <div className="max-w-7xl mx-auto px-6 py-8 flex justify-center gap-8 text-sm text-gray-500">
          <a href="#" className="hover:text-gray-900">Документация</a>
          <a href="#" className="hover:text-gray-900">GitHub</a>
          <a href="#" className="hover:text-gray-900">Контакты</a>
        </div>
      </footer>
    </div>
  );
}

// Шапка сайта + контейнер для страниц. Тут логотип, ссылки, и кнопка войти/выйти.
// Внутри Outlet — это место, куда React Router подставит текущую страницу.

import { Link, Outlet, useLocation, useNavigate } from "react-router-dom";
import { LogOut } from "lucide-react";
import { useState, useEffect } from "react";

export default function Layout() {
  const location = useLocation();
  const navigate = useNavigate();
  const [userEmail, setUserEmail] = useState<string | null>(null);

  // обновляем email из локального хранилища при смене страницы (после логина/регистрации)
  useEffect(() => {
    setUserEmail(localStorage.getItem("userEmail"));
  }, [location]);

  // если пользователь зашёл/вышел в другой вкладке — синхронизируем эту тоже
  useEffect(() => {
    function onStorage(e: StorageEvent) {
      if (e.key === "userEmail" || e.key === "token" || e.key === null) {
        setUserEmail(localStorage.getItem("userEmail"));
      }
    }
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  // при выходе вычищаем всё что сохранили и кидаем на главную
  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("userEmail");
    localStorage.removeItem("userId");
    setUserEmail(null);
    navigate("/");
  }

  const isActive = (path: string) =>
    location.pathname === path
      ? "text-gray-900 font-semibold"
      : "text-gray-500 hover:text-gray-900";

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link to="/" className="text-xl font-bold text-gray-900">
            МаркетЛаб
          </Link>
          <nav className="flex items-center gap-8">
            <Link to="/" className={isActive("/")}>Главная</Link>
            <Link to="/tasks" className={isActive("/tasks")}>Задачи</Link>

            {userEmail ? (
              <div className="flex items-center gap-3">
                <span className="text-sm text-gray-600">{userEmail}</span>
                <button
                  onClick={handleLogout}
                  className="text-gray-400 hover:text-red-500"
                  title="Выйти"
                >
                  <LogOut size={20} />
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                className="px-4 py-1.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700"
              >
                Войти
              </Link>
            )}
          </nav>
        </div>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  );
}

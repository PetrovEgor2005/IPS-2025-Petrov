import { Link, Outlet, useLocation } from "react-router-dom";
import { HelpCircle, User } from "lucide-react";

export default function Layout() {
  const location = useLocation();
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
            <button className="text-gray-400 hover:text-gray-600">
              <HelpCircle size={20} />
            </button>
            <button className="text-gray-400 hover:text-gray-600">
              <User size={20} />
            </button>
          </nav>
        </div>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  );
}

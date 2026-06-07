// Карта маршрутов всего приложения. По адресу в браузере выбираем нужную страницу.
// Все страницы оборачиваются в Layout — это шапка сайта, она всегда сверху.

import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import LandingPage from "./pages/LandingPage";
import TaskCatalog from "./pages/TaskCatalog";
import SolvePage from "./pages/SolvePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<LandingPage />} />         {/* главная */}
        <Route path="/tasks" element={<TaskCatalog />} />     {/* список задач */}
        <Route path="/tasks/:taskId" element={<SolvePage />} /> {/* страница решения */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Route>
    </Routes>
  );
}

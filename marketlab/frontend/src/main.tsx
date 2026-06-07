// Точка входа фронтенда. Тут вставляем приложение в элемент <div id="root"> в index.html.
// BrowserRouter оборачиваем сверху, чтобы внутри App можно было использовать роуты.

import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);

# Образ бекенда. Берём официальный slim-образ питона, ставим зависимости из pyproject.toml.
FROM python:3.12-slim

WORKDIR /app

# Переменные питона: не плодим .pyc, не буферизуем вывод (логи сразу пишутся), не кешируем pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY pyproject.toml /app/pyproject.toml
COPY src /app/src

# -e . устанавливает пакет в editable-режиме, чтобы импорты marketlab.* работали
RUN pip install --no-cache-dir -e .

EXPOSE 8000

# для прода — без --reload, иначе один лишний воркер на каждое изменение файла
CMD ["uvicorn", "marketlab.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

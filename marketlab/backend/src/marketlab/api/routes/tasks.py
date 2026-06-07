"""
Тут два эндпоинта по задачам: список для каталога и детали по одной задаче.
Сам реестр задач лежит в registry.py, здесь только HTTP-обёртка.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from marketlab.api.schemas import FieldOut, TaskDetail, TaskShort
from marketlab.domain.generator import generate_tests
from marketlab.usecases.registry import TASK_REGISTRY

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


#список задач для каталога на фронте — короткий вид без полей ввода/вывода
@router.get("", response_model=list[TaskShort])
def list_tasks() -> list[TaskShort]:
    out: list[TaskShort] = []
    for _task_id, (spec, _solver) in TASK_REGISTRY.items():
        out.append(
            TaskShort(
                id=spec.id,
                title=spec.title,
                topic=spec.topic,
                difficulty=spec.difficulty,
            )
        )
    return out


#полные детали задачи + один публичный тест с правильным ответом (для UI)
@router.get("/{task_id}", response_model=TaskDetail)
def get_task(task_id: str) -> TaskDetail:
    entry = TASK_REGISTRY.get(task_id)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")

    spec, oracle = entry

    #генерим один тест с фиксированным seed=0, чтобы у всех пользователей публичный тест был одинаковый
    tests = generate_tests(task_id, n=1, seed=0)
    public_test = tests[0] if tests else {}

    public_test_output: dict = {}
    if public_test:
        try:
            public_test_output = oracle(public_test)
        except Exception:
            pass

    return TaskDetail(
        id=spec.id,
        title=spec.title,
        topic=spec.topic,
        input_fields=[
            FieldOut(name=f.name, type=f.type, description=f.description) for f in spec.input_fields
        ],
        output_fields=[
            FieldOut(name=f.name, type=f.type, description=f.description)
            for f in spec.output_fields
        ],
        public_test=public_test,
        public_test_output=public_test_output,
    )

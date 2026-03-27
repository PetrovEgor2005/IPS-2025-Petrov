from __future__ import annotations

from fastapi import APIRouter, HTTPException

from marketlab.api.schemas import FieldOut, TaskDetail, TaskShort
from marketlab.domain.generator import generate_tests
from marketlab.usecases.registry import TASK_REGISTRY

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskShort])
def list_tasks() -> list[TaskShort]:
    """Return the catalogue of all available tasks."""
    out: list[TaskShort] = []
    for task_id, (spec, _solver) in TASK_REGISTRY.items():
        out.append(
            TaskShort(
                id=spec.id,
                title=spec.title,
                topic=spec.topic,
            )
        )
    return out


@router.get("/{task_id}", response_model=TaskDetail)
def get_task(task_id: str) -> TaskDetail:
    """Return full task specification + one public test."""
    entry = TASK_REGISTRY.get(task_id)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")

    spec, _solver = entry

    tests = generate_tests(task_id, n=1, seed=0)
    public_test = tests[0] if tests else {}

    return TaskDetail(
        id=spec.id,
        title=spec.title,
        topic=spec.topic,
        input_fields=[
            FieldOut(name=f.name, type=f.type, description=f.description)
            for f in spec.input_fields
        ],
        output_fields=[
            FieldOut(name=f.name, type=f.type, description=f.description)
            for f in spec.output_fields
        ],
        public_test=public_test,
    )

"""
Данный файл выполненяет задачу синхронизации каталога задач в одноимённую БД, 
необходим для стабильности id задачи, а также для реализации плана доработки по окончанию проекта создание аналитики
по задачам для преподавателей, чтобы удобнее было делать оценку знаний
"""


from __future__ import annotations
from sqlalchemy.orm import Session
from marketlab.infra.db.models import TaskRow
from marketlab.infra.db.repos import TaskRepo
from marketlab.usecases.registry import TASK_REGISTRY


def sync_tasks_to_db(db: Session) -> None:
    repo = TaskRepo(db)
    for _task_id, (spec, _solver) in TASK_REGISTRY.items():
        row = TaskRow(
            id=spec.id,
            title=spec.title,
            topic=spec.topic,
            difficulty=spec.difficulty,
            description="",
        )
        repo.upsert(row)
    db.commit()

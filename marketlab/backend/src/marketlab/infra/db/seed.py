from __future__ import annotations
from sqlalchemy.orm import Session
from marketlab.infra.db.models import TaskRow
from marketlab.infra.db.repos import TaskRepo
from marketlab.usecases.registry import TASK_REGISTRY

def sync_tasks_to_db(db: Session) -> None:
    repo = TaskRepo(db)
    for task_id, (spec, _solver) in TASK_REGISTRY.items():
        row = TaskRow(
            id=spec.id,
            title=spec.title,
            topic=spec.topic,
            difficulty=1,
            description="",
        )
        repo.upsert(row)
    db.commit()

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from marketlab.infra.db.models import TaskRow


class TaskRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_all(self) -> list[TaskRow]:
        stmt = select(TaskRow).order_by(TaskRow.difficulty, TaskRow.id)
        return list(self._db.scalars(stmt).all())

    def get_by_id(self, task_id: str) -> TaskRow | None:
        return self._db.get(TaskRow, task_id)

    def upsert(self, row: TaskRow) -> TaskRow:
        """Insert or update a task (used to sync registry → DB on startup)."""
        existing = self.get_by_id(row.id)
        if existing is None:
            self._db.add(row)
        else:
            existing.title = row.title
            existing.topic = row.topic
            existing.difficulty = row.difficulty
            existing.description = row.description
        self._db.flush()
        return row

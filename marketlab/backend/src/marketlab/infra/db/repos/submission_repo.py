from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from marketlab.infra.db.models import SubmissionRow


class SubmissionRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, row: SubmissionRow) -> SubmissionRow:
        self._db.add(row)
        self._db.flush()
        return row

    def get_by_id(self, submission_id: str) -> SubmissionRow | None:
        return self._db.get(SubmissionRow, submission_id)

    def list_by_task(self, task_id: str, *, limit: int = 50) -> list[SubmissionRow]:
        stmt = (
            select(SubmissionRow)
            .where(SubmissionRow.task_id == task_id)
            .order_by(SubmissionRow.created_at.desc())
            .limit(limit)
        )
        return list(self._db.scalars(stmt).all())

    def list_recent(self, *, limit: int = 50) -> list[SubmissionRow]:
        stmt = (
            select(SubmissionRow)
            .order_by(SubmissionRow.created_at.desc())
            .limit(limit)
        )
        return list(self._db.scalars(stmt).all())

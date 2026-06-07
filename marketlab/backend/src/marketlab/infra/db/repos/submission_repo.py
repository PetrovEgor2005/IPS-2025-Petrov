"""
Этот класс является также, как и user_repo, посредником между стилем питона и языком SQL
"""


from sqlalchemy import select
from sqlalchemy.orm import Session
from marketlab.infra.db.models import SubmissionRow


class SubmissionRepo:
    def __init__(self, db: Session) -> None:
        self._db = db
    #запись сабмитта
    def create(self, row: SubmissionRow) -> SubmissionRow:
        self._db.add(row)
        self._db.flush()
        return row

    def get_by_id(self, submission_id: str) -> SubmissionRow | None:
        return self._db.get(SubmissionRow, submission_id)
    #все сабмиты по задаче
    def list_by_task(self, task_id: str, limit: int = 50) -> list[SubmissionRow]:
        stmt = (
            select(SubmissionRow)
            .where(SubmissionRow.task_id == task_id)
            .order_by(SubmissionRow.created_at.desc())
            .limit(limit)
        )
        return list(self._db.execute(stmt).scalars().all())
    #все конкретного пользователя
    def list_by_user(self, user_id: str, limit: int = 50) -> list[SubmissionRow]:
        stmt = (
            select(SubmissionRow)
            .where(SubmissionRow.user_id == user_id)
            .order_by(SubmissionRow.created_at.desc())
            .limit(limit)
        )
        return list(self._db.execute(stmt).scalars().all())
    #сабмиты пользователя по задаче
    def list_by_task_and_user(
        self, task_id: str, user_id: str, limit: int = 50
    ) -> list[SubmissionRow]:
        stmt = (
            select(SubmissionRow)
            .where(SubmissionRow.task_id == task_id)
            .where(SubmissionRow.user_id == user_id)
            .order_by(SubmissionRow.created_at.desc())
            .limit(limit)
        )
        return list(self._db.execute(stmt).scalars().all())
    #получение последних запросов без фильтров
    def list_recent(self, limit: int = 50) -> list[SubmissionRow]:
        stmt = select(SubmissionRow).order_by(SubmissionRow.created_at.desc()).limit(limit)
        return list(self._db.execute(stmt).scalars().all())

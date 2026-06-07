"""
Данный класс выступает посредником между тем, как пишутся обращения к таблице в стиле питона 
на язык SQL
"""


from sqlalchemy import select
from sqlalchemy.orm import Session
from marketlab.infra.db.models import UserRow


class UserRepo:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, row: UserRow) -> UserRow:
        self._db.add(row)
        self._db.flush()
        return row

    def get_by_email(self, email: str) -> UserRow | None:
        stmt = select(UserRow).where(UserRow.email == email)
        return self._db.execute(stmt).scalar_one_or_none()

    def get_by_id(self, user_id: str) -> UserRow | None:
        return self._db.get(UserRow, user_id)

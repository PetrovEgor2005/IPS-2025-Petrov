"""
Зависимости FastAPI для аутентификации.
get_current_user — строгая (без токена 401), get_current_user_optional — мягкая (без токена None).
Подключаются в роутах через Depends(...).
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from marketlab.infra.auth.jwt import decode_access_token
from marketlab.infra.db.models import UserRow
from marketlab.infra.db.repos.user_repo import UserRepo
from marketlab.infra.db.session import get_db

security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)  #не падать при отсутствии заголовка


#строгая версия: без валидного токена сразу 401
def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> UserRow:
    token = creds.credentials
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    repo = UserRepo(db)
    user = repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


#мягкая версия для анонимных сабмитов: нет токена / битый / удалённый юзер -> None, без падения
def get_current_user_optional(
    creds: HTTPAuthorizationCredentials | None = Depends(optional_security),
    db: Session = Depends(get_db),
) -> UserRow | None:
    if creds is None:
        return None

    token = creds.credentials
    user_id = decode_access_token(token)
    if user_id is None:
        return None

    repo = UserRepo(db)
    return repo.get_by_id(user_id)

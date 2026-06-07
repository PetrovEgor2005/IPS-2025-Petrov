"""
В данном файле происходит настройка подключения к базе данных и открытие сессии, через которую будут записываться
изменения при активности пользователя
"""


from __future__ import annotations
from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from marketlab.infra.settings import settings
#установление первоначального соединения
engine = create_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
)
#фабрика сессий 
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

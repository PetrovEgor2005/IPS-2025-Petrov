"""
Точка входа в FastAPI: создаём app, навешиваем middleware (CORS, rate-limit),
подключаем 4 роутера. lifespan при старте создаёт таблицы и заливает каталог задач в БД.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from marketlab.api.limiter import limiter
from marketlab.api.routes.auth import router as auth_router
from marketlab.api.routes.health import router as health_router
from marketlab.api.routes.submissions import router as submissions_router
from marketlab.api.routes.tasks import router as tasks_router
from marketlab.infra.db.models import Base
from marketlab.infra.db.seed import sync_tasks_to_db
from marketlab.infra.db.session import SessionLocal, engine
from marketlab.infra.settings import settings


#lifespan — это код, который выполняется один раз при старте (до yield) и при остановке (после yield)
@asynccontextmanager
async def lifespan(app: FastAPI):
    #создаём таблицы если их ещё нет (вместо отдельных миграций alembic — для курсача хватает)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        sync_tasks_to_db(db)  #перезаливаем 20 задач из registry.py в БД
    finally:
        db.close()
    yield


#фабрика приложения — отдельная функция, чтобы можно было создавать app в тестах с другими настройками
def create_app() -> FastAPI:
    app = FastAPI(
        title="MarketLab API",
        description="Interactive microeconomics trainer — backend",
        version="0.3.0",
        lifespan=lifespan,
    )

    #slowapi требует именно app.state.limiter — через это middleware находит лимитер
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    #CORS: список доменов парсим из CSV-строки вручную, потому что pydantic-settings
    #пытается JSON-парсить list[str] и падает на простой строке "a,b,c"
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[s.strip() for s in settings.cors_origins.split(",") if s.strip()],
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(tasks_router)
    app.include_router(submissions_router)
    app.include_router(auth_router)
    return app


app = create_app()

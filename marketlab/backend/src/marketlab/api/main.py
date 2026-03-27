from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from marketlab.api.routes.health import router as health_router
from marketlab.api.routes.tasks import router as tasks_router
from marketlab.api.routes.submissions import router as submissions_router
from marketlab.infra.db.models import Base
from marketlab.infra.db.seed import sync_tasks_to_db
from marketlab.infra.db.session import engine, SessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs once on startup: create tables & sync tasks to DB."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        sync_tasks_to_db(db)
    finally:
        db.close()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="MarketLab API",
        description="Interactive microeconomics trainer — backend",
        version="0.3.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(tasks_router)
    app.include_router(submissions_router)

    return app


app = create_app()

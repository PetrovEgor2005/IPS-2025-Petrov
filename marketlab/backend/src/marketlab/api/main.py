from fastapi import FastAPI
from marketlab.api.routes.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title="MarketLab API")
    app.include_router(health_router)
    return app


app = create_app()

"""
Данный файл выступает связующим звеном в конфигурации приложения, так как здесь собраны все окружения, 
необходимые бекенду, благодаря pydantic settings подтягиваются значения из env и переменные окружения
"""

from __future__ import annotations
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://marketlab:marketlab@localhost:5432/marketlab"
    secret_key: str = "change-me-in-production-to-random-string"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    environment: str = "development"
    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()

if settings.environment == "production" and settings.secret_key.startswith("change-me"):
    raise RuntimeError(
        "SECRET_KEY must be set to a real value in production "
        "(currently using the placeholder). Set the SECRET_KEY env var."
    )

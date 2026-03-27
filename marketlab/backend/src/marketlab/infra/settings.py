"""
Application settings loaded from environment variables / .env file.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://marketlab:marketlab@localhost:5432/marketlab"

    model_config = {"env_file": ".env", "extra": "ignore"}



settings = Settings()

"""
Самый простой эндпоинт - проверка, жив ли сервер. Используется на проде, чтобы понять, что бекенд поднялся.
"""

from fastapi import APIRouter

router = APIRouter(tags=["system"])


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}

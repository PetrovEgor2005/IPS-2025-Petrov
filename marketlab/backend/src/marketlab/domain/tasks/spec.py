"""
В данном классе прописывается спецификация задачи, какие поля должны 
быть у каждой из задач, какие типы данных, всё это важно для согласованности с API
"""

from __future__ import annotations
from dataclasses import dataclass
from .types import FieldSpec, TaskTopic


@dataclass(frozen=True, slots=True)
class TaskSpec:
    id: str
    title: str
    topic: TaskTopic
    input_fields: tuple[FieldSpec, ...]
    output_fields: tuple[FieldSpec, ...]
    difficulty: int = 1  # 1=Лёгкая, 2=Средняя, 3=Сложная(Это необходимо для фильтров)

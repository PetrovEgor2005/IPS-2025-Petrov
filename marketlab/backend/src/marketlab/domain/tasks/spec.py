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

from __future__ import annotations

from dataclasses import dataclass

from .types import FieldSpec, TaskTopic


@dataclass(frozen=True, slots=True)
class TaskSpec:
    """
    Pure metadata of a task template:
    - what it is about
    - what it expects as input
    - what it must output

    No business logic here.
    """
    id: str
    title: str
    topic: TaskTopic
    input_fields: tuple[FieldSpec, ...]
    output_fields: tuple[FieldSpec, ...]

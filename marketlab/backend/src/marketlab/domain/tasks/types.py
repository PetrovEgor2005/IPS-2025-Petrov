from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

TaskTopic = Literal[
    "equilibrium",
    "taxes_subsidies",
    "welfare",
    "aggregation",
    "inverse",
]

ValueType = Literal["int", "float", "str"]

@dataclass(frozen=True, slots=True)
class FieldSpec:
    """
    Describes a single input/output field.
    """
    name: str
    type: ValueType
    description: str


Params = dict[str, Any]
Result = dict[str, float]

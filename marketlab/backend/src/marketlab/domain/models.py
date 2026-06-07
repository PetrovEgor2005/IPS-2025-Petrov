"""
В данном файле определяются модели для функции спроса, функции предложения и рыночной политики.
- LinearDemand: Модель линейной функции спроса, Qd(P) = a - bP, где a > 0 и b > 0.
- LinearSupply: Модель линейной функции предложения, Qs(P) = c + dP, где d > 0.
- MarketPolicy: Модель рыночной политики, которая может быть налогом, субсидией или отсутствием вмешательства.
Все они в дальнейшем используются для расчёта равновесия, в солвере и генераторе тестов
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from .errors import InvalidParameterError
Mode = Literal["none", "tax", "subsidy"]

@dataclass(frozen=True, slots=True)
class LinearDemand:
    a: float
    b: float

    def __post_init__(self) -> None:
        if self.a <= 0:
            raise InvalidParameterError("Demand parameter 'a' must be > 0.")
        if self.b <= 0:
            raise InvalidParameterError("Demand parameter 'b' must be > 0.")

    def quantity(self, price: float) -> float:
        return self.a - self.b * price


@dataclass(frozen=True, slots=True)
class LinearSupply:
    c: float
    d: float

    def __post_init__(self) -> None:
        if self.d <= 0:
            raise InvalidParameterError("Supply parameter 'd' must be > 0.")

    def quantity(self, price: float) -> float:
        return self.c + self.d * price


@dataclass(frozen=True, slots=True)
class MarketPolicy:
    mode: Mode
    t: float = 0.0

    def __post_init__(self) -> None:
        if self.mode not in ("none", "tax", "subsidy"):
            raise InvalidParameterError("Policy mode must be 'none', 'tax', or 'subsidy'.")
        if self.t < 0:
            raise InvalidParameterError("Policy parameter 't' must be >= 0.")
        if self.mode == "none" and self.t != 0:
            raise InvalidParameterError("For mode='none', parameter 't' must be 0.")

    def producer_price(self, consumer_price: float) -> float:
        if self.mode == "none":
            return consumer_price
        if self.mode == "tax":
            return consumer_price - self.t
        return consumer_price + self.t

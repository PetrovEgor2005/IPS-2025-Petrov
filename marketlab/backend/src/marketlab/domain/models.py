from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .errors import InvalidParameterError

Mode = Literal["none", "tax", "subsidy"]


@dataclass(frozen=True, slots=True)
class LinearDemand:
    """
    Qd(P) = a - bP
    a > 0, b > 0
    """

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
    """
    Qs(P) = c + dP
    d > 0 (c may be negative)
    """

    c: float
    d: float

    def __post_init__(self) -> None:
        if self.d <= 0:
            raise InvalidParameterError("Supply parameter 'd' must be > 0.")

    def quantity(self, price: float) -> float:
        return self.c + self.d * price


@dataclass(frozen=True, slots=True)
class MarketPolicy:
    """
    Policy introduces a per-unit wedge on producers:
    - none: producer price = consumer price
    - tax: producer price = consumer price - t
    - subsidy: producer price = consumer price + t
    """

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
        # subsidy
        return consumer_price + self.t

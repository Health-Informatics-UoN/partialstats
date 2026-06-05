from math import hypot
from typing import Self
from dataclasses import dataclass
from .protocol import (
    AddsProtocol,
    SumSumSqCountPartialProtocol,
    VariancePartialProtocol,
)


@dataclass
class SumSumSqCountPartial(SumSumSqCountPartialProtocol, AddsProtocol):
    """Partial result carrying a running sum, sum of squares, and count."""

    sum: float
    sum_of_squares: float
    count: int

    def __add__(self, other: Self) -> Self:
        return type(self)(
            self.sum + other.sum,
            self.sum_of_squares + other.sum_of_squares,
            self.count + other.count,
        )


@dataclass
class VariancePartial(VariancePartialProtocol, AddsProtocol):
    """Partial result carrying the running pythagorean sum of variance"""

    variance: float

    def __add__(self, other: Self) -> Self:
        return type(self)(hypot(self.variance, other.variance))

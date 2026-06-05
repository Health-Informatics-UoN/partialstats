from typing import Self
from dataclasses import dataclass
from .protocol import AddsProtocol, VariancePartialProtocol


@dataclass
class VariancePartial(VariancePartialProtocol, AddsProtocol):
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

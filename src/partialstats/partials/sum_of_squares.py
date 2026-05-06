from typing import Self
from dataclasses import dataclass
from .protocol import Partial


@dataclass
class SumOfSquaresPartial(Partial):
    """Partial result carrying a running sum, sum of squares, and count."""

    sum: float
    sumsq: float
    count: int

    def __add__(self, other: Self) -> Self:
        return type(self)(
            self.sum + other.sum, self.sumsq + other.sumsq, self.count + other.count
        )

    @classmethod
    def identity(cls) -> Self:
        return cls(0, 0, 0)

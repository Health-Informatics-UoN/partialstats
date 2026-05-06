from typing import Self
from dataclasses import dataclass
from .protocol import Partial


@dataclass
class SumPartial(Partial):
    """Partial result carrying a running sum and count."""

    sum: float
    count: int

    def __add__(self, other: Self) -> Self:
        return type(self)(self.sum + other.sum, self.count + other.count)

    @classmethod
    def identity(cls) -> Self:
        return cls(0, 0)

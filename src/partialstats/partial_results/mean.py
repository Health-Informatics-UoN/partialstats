from typing import Self
from dataclasses import dataclass
from .protocol import AddsProtocol, MeanPartialProtocol


@dataclass
class MeanPartial(MeanPartialProtocol, AddsProtocol):
    """Partial result carrying a running sum and count."""

    sum: float
    count: int

    def __add__(self, other: Self) -> Self:
        return type(self)(self.sum + other.sum, self.count + other.count)

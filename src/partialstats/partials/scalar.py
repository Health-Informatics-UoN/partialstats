from typing import Self
from dataclasses import dataclass
from math import inf
from .protocol import Partial

@dataclass
class MaxPartial(Partial):
    value: float

    def __add__(self, other: Self) -> Self:
        return type(self)(self.value if self.value > other.value else other.value)

    @classmethod
    def identity(cls) -> Self:
        return cls(-inf)

@dataclass
class MinPartial(Partial):
    value: float

    def __add__(self, other: Self) -> Self:
        return type(self)(self.value if self.value < other.value else other.value)

    @classmethod
    def identity(cls) -> Self:
        return cls(inf)

@dataclass
class CountPartial(Partial):
    value: int

    def __add__(self, other: Self) -> Self:
        return type(self)(self.value + other.value)
    
    @classmethod
    def identity(cls) -> Self:
        return cls(0)

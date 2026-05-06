from typing import Protocol, Self


class Partial(Protocol):
    def __add__(self, other: Self) -> Self: ...

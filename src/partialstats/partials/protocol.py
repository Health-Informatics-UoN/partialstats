from typing import Protocol, TypeVar

S = TypeVar("S")


class Partial(Protocol):
    def __add__(self: S, other: S) -> S: ...

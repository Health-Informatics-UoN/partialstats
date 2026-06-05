from typing import Protocol, Self


class AddsProtocol(Protocol):
    def __add__(self, other: Self) -> Self: ...


class CountPartialProtocol(AddsProtocol, Protocol):
    count: int


class SumPartialProtocol(AddsProtocol, Protocol):
    sum: float


class SumCountPartialProtocol(CountPartialProtocol, SumPartialProtocol, Protocol): ...


class SumOfSquaresPartialProtocol(AddsProtocol, Protocol):
    sum_of_squares: float


class SumSumSqCountPartialProtocol(
    SumCountPartialProtocol, SumOfSquaresPartialProtocol, Protocol
): ...


class VariancePartialProtocol(Protocol):
    variance: float

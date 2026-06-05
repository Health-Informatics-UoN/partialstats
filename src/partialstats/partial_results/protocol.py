from typing import Protocol, Self


class AddsProtocol(Protocol):
    def __add__(self, other: Self) -> Self: ...


class CountPartialProtocol(AddsProtocol, Protocol):
    count: int


class SumPartialProtocol(AddsProtocol, Protocol):
    sum: float


class MeanPartialProtocol(CountPartialProtocol, SumPartialProtocol, Protocol): ...


class SumOfSquaresPartialProtocol(AddsProtocol, Protocol):
    sum_of_squares: float


class VariancePartialProtocol(
    MeanPartialProtocol, SumOfSquaresPartialProtocol, Protocol
): ...

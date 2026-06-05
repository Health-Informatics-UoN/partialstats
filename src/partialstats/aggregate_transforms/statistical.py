from math import sqrt
from typing import Iterable

from ..partial_results.protocol import (
    CountPartialProtocol,
    SumPartialProtocol,
    MeanPartialProtocol,
    VariancePartialProtocol,
)
from .core import sum_and_transform


def count(partials: Iterable[CountPartialProtocol]) -> int:
    """Combines count partial results into a global count"""
    return sum_and_transform(lambda x: x.count, partials)


def sum(partials: Iterable[SumPartialProtocol]) -> float:
    """Combines sum partial results into a global sum"""
    return sum_and_transform(lambda x: x.sum, partials)


def mean(partials: Iterable[MeanPartialProtocol]) -> float:
    """Combines partial results into a global mean."""
    return sum_and_transform(lambda x: x.sum / x.count, partials)


def variance(partials: Iterable[VariancePartialProtocol]) -> float:
    """Combines partial results into a global population variance."""
    return sum_and_transform(
        lambda x: x.sum_of_squares / x.count - (x.sum / x.count) ** 2, partials
    )


def std(partials: Iterable[VariancePartialProtocol]) -> float:
    """Combines partial results into a global population standard deviation."""
    return sum_and_transform(
        lambda x: sqrt(x.sum_of_squares / x.count - (x.sum / x.count) ** 2), partials
    )

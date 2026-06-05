from math import sqrt
from typing import Iterable, overload

from ..partial_results.protocol import (
    CountPartialProtocol,
    SumCountPartialProtocol,
    SumPartialProtocol,
    SumSumSqCountPartialProtocol,
    VariancePartialProtocol,
)
from .core import sum_and_transform


def count(partials: Iterable[CountPartialProtocol]) -> int:
    """Combines count partial results into a global count"""
    return sum_and_transform(lambda x: x.count, partials)


def sum(partials: Iterable[SumPartialProtocol]) -> float:
    """Combines sum partial results into a global sum"""
    return sum_and_transform(lambda x: x.sum, partials)


def mean(partials: Iterable[SumCountPartialProtocol]) -> float:
    """Combines partial results into a global mean."""
    return sum_and_transform(lambda x: x.sum / x.count, partials)


@overload
def variance(partials: Iterable[VariancePartialProtocol]) -> float: ...


@overload
def variance(partials: Iterable[SumSumSqCountPartialProtocol]) -> float: ...


def variance(partials) -> float:
    """Combines partial results into a global population variance."""
    probe = list(partials)[0]
    if (
        hasattr(probe, "sum")
        & hasattr(probe, "sum_of_squares")
        & hasattr(probe, "count")
    ):
        return sum_and_transform(
            lambda x: x.sum_of_squares / x.count - (x.sum / x.count) ** 2, partials
        )
    else:
        return sum_and_transform(lambda x: x.variance, partials)


def std(partials: Iterable[SumSumSqCountPartialProtocol]) -> float:
    """Combines partial results into a global population standard deviation."""
    return sum_and_transform(
        lambda x: sqrt(x.sum_of_squares / x.count - (x.sum / x.count) ** 2), partials
    )

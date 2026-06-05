from typing import TypeVar, Iterable, Callable
from functools import reduce

from partialstats.partial_results.protocol import AddsProtocol

S = TypeVar("S")
R = TypeVar("R")


def aggregate_transform(
    aggregate: Callable[[S, S], S],
    finalise: Callable[[S], R],
    partials: Iterable[S],
) -> R:
    """
    Given functions for aggregating partial results and producing a final result, returns the final result

    Parameters
    ----------
    aggregate: Callable[[S,S],S]
        A function for aggregation of partial results
    finalise: Callable[[S], R]
        A function for calculating the final desired result
    partials: Iterable[S]
        An iterable of type S to be transformed
    """

    return finalise(reduce(aggregate, partials))


Adds = TypeVar("Adds", bound=AddsProtocol)


def sum_and_transform(finalise: Callable[[Adds], R], partials: Iterable[Adds]) -> R:
    return finalise(reduce(lambda a, b: a + b, partials))

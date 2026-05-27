from typing import TypeVar, Generic, Iterable, Callable
from dataclasses import dataclass
from functools import reduce

from ..partials.protocol import S

R = TypeVar("R")


def build_combine_function(
    aggregate: Callable[[S, S], S],
    finalise: Callable[[S], R],
):
    """
    Given functions for aggregating partial results and producing a final result, returns a function for calculating the final result.

    Parameters
    ----------
    aggregate: Callable[[S,S],S]
        A function for aggregation of partial results
    finalise: Callable[[S], R]
        A function for calculating the final desired result
    """

    def combine(partials: Iterable[S]):
        first, *rest = partials
        return finalise(reduce(aggregate, rest, first))

    return combine


@dataclass
class Combiner(Generic[S, R]):
    """
    Runs on the aggregator to combine partial results from all nodes into
    the final statistic.

    Type parameters:
        S: the type of the partial results produced by a PartialReducer
        R: the type of the final result
    """

    finalise: Callable[[S], R]
    aggregate: Callable[[S, S], S] = lambda a, b: a + b

    def combine(self, partials: Iterable[S]) -> R:
        """
        Folds the partial results together using `aggregate`, then calls `finalise`.
        """
        first, *rest = partials
        return self.finalise(reduce(self.aggregate, rest, first))

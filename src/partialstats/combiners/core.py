from typing import TypeVar, Generic, Iterable, Callable
from dataclasses import dataclass
from functools import reduce

S = TypeVar("S")
R = TypeVar("R")


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

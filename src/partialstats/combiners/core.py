from typing import TypeVar, Generic, Iterable, Callable
from dataclasses import dataclass
from functools import reduce

from ..partials import Partial

S = TypeVar("S", bound=Partial)
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

    def combine(self, partials: Iterable[S]) -> R:
        """
        Folds the partial results together using `aggregate`, then calls `finalise`.
        """
        first, *rest = partials
        return self.finalise(reduce(lambda a, b: a + b, rest, first))

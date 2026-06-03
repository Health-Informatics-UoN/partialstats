from typing import TypeVar, Generic, Iterable, Callable, Protocol, final
from dataclasses import dataclass
from functools import reduce

from partialstats.partials.protocol import AddsProtocol

S = TypeVar("S")
S_contra = TypeVar("S_contra", contravariant=True)
R = TypeVar("R")
R_co = TypeVar("R_co", covariant=True)


def aggregate_transform(
    aggregate: Callable[[S, S], S],
    finalise: Callable[[S], R],
    partials: Iterable[S],
):
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



class CombinerProtocol(Protocol[S_contra, R_co]):
    def combine(self, partials: Iterable[S_contra]) -> R_co: ...


@final
@dataclass(frozen=True)
class Combiner(Generic[S, R]):
    """
    Runs on the aggregator to combine partial results from all nodes into
    the final statistic.

    Type parameters:
        S: the type of the partial results produced by a PartialReducer
        R: the type of the final result
    """

    finalise: Callable[[S], R]
    aggregate: Callable[[S, S], S]

    def combine(self, partials: Iterable[S]) -> R:
        """
        Folds the partial results together using `aggregate`, then calls `finalise`.
        """
        return aggregate_transform(self.aggregate, self.finalise, partials)


Adds = TypeVar("Adds", bound=AddsProtocol)


@final
@dataclass(frozen=True)
class SumCombiner(Generic[Adds, R]):
    """
    Runs on the aggregator to combine partial results from all nodes into
    the final statistic.

    Type parameters:
        Adds: the type of the partial results produced by a PartialReducer. Must implement the __add__ special method.
        R: the type of the final result
    """

    finalise: Callable[[Adds], R]

    def combine(self, partials: Iterable[Adds]) -> R:
        return aggregate_transform(lambda a, b: a + b, self.finalise, partials)

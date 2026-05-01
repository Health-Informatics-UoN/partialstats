from typing import Callable, Iterable, Generic, TypeVar
from dataclasses import dataclass
from functools import reduce

T = TypeVar("T")
S = TypeVar("S")
R = TypeVar("R")


@dataclass
class PartialReducer(Generic[T, S]):
    """
    Runs at each node (partition) to reduce its rows into a partial result.

    Type parameters:
        T: the type of each input row
        S: the type of the partial result (must form a commutative monoid under `merge`)
    """

    apply: Callable[[T], S]
    merge: Callable[[S, S], S]
    identity: S

    def reduce(self, rows: Iterable[T]) -> S:
        """
        Applies `apply` to each row, then folds the results together using `merge`.
        """
        return reduce(self.merge, map(self.apply, rows), self.identity)


@dataclass
class Combiner(Generic[S, R]):
    """
    Runs on the aggregator to combine partial results from all nodes into
    the final statistic.

    Type parameters:
        S: the type of the partial results produced by a PartialReducer
        R: the type of the final result
    """

    aggregate: Callable[[S, S], S]
    identity: S
    finalise: Callable[[S], R]

    def combine(self, partials: Iterable[S]) -> R:
        """
        Folds the partial results together using `aggregate`, then calls `finalise`.
        """
        return self.finalise(reduce(self.aggregate, partials, self.identity))


@dataclass
class DistributedStat(Generic[T, S, R]):
    """
    A fully specified distributed statistic: a PartialReducer paired with a Combiner.

    Each partition runs the reducer; the aggregator runs the combiner.

    Type parameters:
        T: input row type
        S: partial result type
        R: final result type
    """

    reducer: PartialReducer[T, S]
    combiner: Combiner[S, R]

    def compute(self, partitions: Iterable[Iterable[T]]) -> R:
        """
        Computes the statistic over partitioned data.

        Args:
            partitions: an iterable of partitions, each partition being an iterable of rows.

        Returns:
            The final aggregated statistic.
        """
        partials: Iterable[S] = map(self.reducer.reduce, partitions)
        return self.combiner.combine(partials)

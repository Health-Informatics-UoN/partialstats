from typing import Callable, Iterable, Generic, TypeVar
from dataclasses import dataclass
from functools import reduce

from ..partials import MeanPartial, VariancePartial
from ..combiners import CombinerProtocol

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

    def reduce(self, rows: Iterable[T]) -> S:
        """
        Applies `apply` to each row, then folds the results together using `merge`.
        """
        first, *rest = map(self.apply, rows)
        return reduce(self.merge, rest, first)

# Reducer implementations for reference

count_reducer = PartialReducer[object, int](
    merge=lambda a, b: a+b,
    apply=lambda _: 1,
)
"""Counts the number of rows in each partition."""

sum_reducer = PartialReducer[float, MeanPartial](
    merge=lambda a, b: a+b,
    apply=lambda x: MeanPartial(sum=x, count=1),
)
"""Accumulates the sum and count of values — sufficient to compute mean."""

sum_of_squares_reducer = PartialReducer[float, VariancePartial](
    merge=lambda a, b: a+b,
    apply=lambda x: VariancePartial(sum=x, sum_of_squares=x * x, count=1),
)
"""Accumulates sum, sum of squares, and count — sufficient to compute variance and std dev."""

max_reducer = PartialReducer[float, float](
    apply=lambda x: x,
    merge=lambda a, b: a if a > b else b,
)
"""Tracks the running maximum value."""

min_reducer = PartialReducer[float, float](
    apply=lambda x: x,
    merge=lambda a, b: a if a < b else b,
)
"""Tracks the running minimum value."""


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
    combiner: CombinerProtocol[S, R]

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

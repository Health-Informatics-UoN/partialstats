from typing import Callable, Iterable, Generic, TypeVar
from dataclasses import dataclass
from functools import reduce

T = TypeVar("T")
S = TypeVar("S")
R = TypeVar("R")


@dataclass
class InnerFunction(Generic[T, S]):
    """
    The function that runs at a node for an algebraic aggregate function
    """

    apply: Callable[[T], S]
    merge: Callable[[S, S], S]
    identity: S

    def run(self, rows: Iterable[T]) -> S:
        """
        Calls the `apply` function on the rows of the data, then uses the `merge` function to produce an intermediate
        """
        return reduce(self.merge, map(self.apply, rows), self.identity)


@dataclass
class OuterFunction(Generic[S, R]):
    """
    The function running on an aggregator that aggregates intermediate values to produce the final result of an algebraic aggregate function
    """

    aggregate: Callable[[S, S], S]
    identity: S
    finalise: Callable[[S], R]

    def run(self, intermediates: Iterable[S]) -> R:
        """
        Calls the `aggregate` function on the intermediates, then uses `finalise` to produce the final result
        """
        return self.finalise(reduce(self.aggregate, intermediates))


@dataclass
class AlgebraicAggregate(Generic[T, S, R]):
    """
    Applies an algebraic aggregate function to nodes to aggregate some statistic
    """

    inner_function: InnerFunction[T, S]
    outer_function: OuterFunction[S, R]

    def run(self, data: Iterable[Iterable[T]]) -> R:
        """
        Computes the aggregate function
        """
        intermediates: Iterable[S] = map(self.inner_function.run, data)
        return self.outer_function.run(intermediates)

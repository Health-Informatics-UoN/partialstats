from dataclasses import dataclass
from typing import TypeVar, Generic

from partialstats.partial_results.protocol import (
    CountPartialProtocol,
    SumCountPartialProtocol,
    SumPartialProtocol,
    SumSumSqCountPartialProtocol,
)
from ..aggregate_transforms.statistical import (
    count,
    sum,
    mean,
    variance,
    std,
)

P = TypeVar("P")


@dataclass
class StatAggregator(Generic[P]):
    """
    Generic class for aggregators
    """

    data: list[P]

    def __len__(self):
        return len(self.data)


class CountAggregator(StatAggregator[CountPartialProtocol]):
    """
    Class that can hold data compatible with the CountPartialProtocol (containing count data), and can calculate an aggregated count.
    """

    @property
    def count(self) -> int:
        return count(self.data)


class SumAggregator(StatAggregator[SumPartialProtocol]):
    """
    Class that can hold data compatible with the SumPartialProtocol (containing sum data), and can calculate an aggregated sum.
    """

    @property
    def sum(self) -> float:
        return sum(self.data)


class MeanAggregator(StatAggregator[SumCountPartialProtocol]):
    """
    Class that can:
    - Hold data compatible with the MeanPartialProtocol
        - count
        - sum
    - Calculate aggregated values
        - count
        - sum
        - mean
    """

    @property
    def count(self) -> int:
        return count(self.data)

    @property
    def sum(self) -> float:
        return sum(self.data)

    @property
    def mean(self) -> float:
        return mean(self.data)


class VarianceAggregator(StatAggregator[SumSumSqCountPartialProtocol]):
    """
    Class that can:
    - Hold data compatible with the SumSumSqCountPartialProtocol
        - count
        - sum
        - sum_of_squares
    - Calculate aggregated values
        - count
        - sum
        - mean
        - variance
        - standard deviation
    """

    @property
    def count(self) -> int:
        return count(self.data)

    @property
    def sum(self) -> float:
        return sum(self.data)

    @property
    def mean(self) -> float:
        return mean(self.data)

    @property
    def variance(self) -> float:
        return variance(self.data)

    @property
    def std(self) -> float:
        return std(self.data)

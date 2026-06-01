from dataclasses import dataclass
from typing import TypeVar, Generic

from partialstats.partials.protocol import (
    CountPartialProtocol,
    MeanPartialProtocol,
    SumPartialProtocol,
    VariancePartialProtocol,
)
from ..combiners.statistical import (
    count_combiner,
    sum_combiner,
    mean_combiner,
    variance_combiner,
    std_combiner,
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
        return count_combiner.combine(self.data)


class SumAggregator(StatAggregator[SumPartialProtocol]):
    """
    Class that can hold data compatible with the SumPartialProtocol (containing sum data), and can calculate an aggregated sum.
    """

    @property
    def sum(self) -> float:
        return sum_combiner.combine(self.data)


class MeanAggregator(StatAggregator[MeanPartialProtocol]):
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
        return count_combiner.combine(self.data)

    @property
    def sum(self) -> float:
        return sum_combiner.combine(self.data)

    @property
    def mean(self) -> float:
        return mean_combiner.combine(self.data)


class VarianceAggregator(StatAggregator[VariancePartialProtocol]):
    """
    Class that can:
    - Hold data compatible with the VariancePartialProtocol
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
        return count_combiner.combine(self.data)

    @property
    def sum(self) -> float:
        return sum_combiner.combine(self.data)

    @property
    def mean(self) -> float:
        return mean_combiner.combine(self.data)

    @property
    def variance(self) -> float:
        return variance_combiner.combine(self.data)

    @property
    def std(self) -> float:
        return std_combiner.combine(self.data)

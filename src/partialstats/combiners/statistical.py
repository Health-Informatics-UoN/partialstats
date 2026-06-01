from math import sqrt

from ..partials.protocol import (
    CountPartialProtocol,
    SumPartialProtocol,
    MeanPartialProtocol,
    VariancePartialProtocol,
)
from .core import SumCombiner

count_combiner = SumCombiner[CountPartialProtocol, int](
    finalise=lambda x: x.count,
)
"""Combines count partial results into a global count"""

sum_combiner = SumCombiner[SumPartialProtocol, float](
    finalise=lambda x: x.sum,
)
"""Combines sum partial results into a global sum"""

mean_combiner = SumCombiner[MeanPartialProtocol, float](
    finalise=lambda x: x.sum / x.count,
)
"""Combines partial results into a global mean."""

variance_combiner = SumCombiner[VariancePartialProtocol, float](
    finalise=lambda x: x.sum_of_squares / x.count - (x.sum / x.count) ** 2,
)
"""Combines partial results into a global population variance."""

std_combiner = SumCombiner[VariancePartialProtocol, float](
    finalise=lambda x: sqrt(x.sum_of_squares / x.count - (x.sum / x.count) ** 2),
)
"""Combines partial results into a global population standard deviation."""

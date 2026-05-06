from math import sqrt

from ..partials import SumPartial, SumOfSquaresPartial
from .core import Combiner

mean_combiner = Combiner[SumPartial, float](
    finalise=lambda x: x.sum / x.count,
)
"""Combines SumPartials into a global mean."""

variance_combiner = Combiner[SumOfSquaresPartial, float](
    finalise=lambda x: x.sumsq / x.count - (x.sum / x.count) ** 2,
)
"""Combines SumOfSquaresPartials into a global population variance."""

std_combiner = Combiner[SumOfSquaresPartial, float](
    finalise=lambda x: sqrt(x.sumsq / x.count - (x.sum / x.count) ** 2),
)
"""Combines SumOfSquaresPartials into a global population standard deviation."""

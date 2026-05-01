from math import inf, sqrt

from .core import Combiner
from .partials import SumPartial, SumOfSquaresPartial


sum_combiner = Combiner[float, float](
    aggregate=lambda a, b: a + b,
    identity=0,
    finalise=lambda x: x,
)
"""Combines partial sums into a total sum."""

mean_combiner = Combiner[SumPartial, float](
    aggregate=lambda a, b: SumPartial(sum=a.sum + b.sum, count=a.count + b.count),
    identity=SumPartial(0, 0),
    finalise=lambda x: x.sum / x.count,
)
"""Combines SumPartials into a global mean."""

variance_combiner = Combiner[SumOfSquaresPartial, float](
    aggregate=lambda a, b: SumOfSquaresPartial(
        sum=a.sum + b.sum,
        sumsq=a.sumsq + b.sumsq,
        count=a.count + b.count,
    ),
    identity=SumOfSquaresPartial(0, 0, 0),
    finalise=lambda x: x.sumsq / x.count - (x.sum / x.count) ** 2,
)
"""Combines SumOfSquaresPartials into a global population variance."""

std_combiner = Combiner[SumOfSquaresPartial, float](
    aggregate=variance_combiner.aggregate,
    identity=SumOfSquaresPartial(0, 0, 0),
    finalise=lambda x: sqrt(x.sumsq / x.count - (x.sum / x.count) ** 2),
)
"""Combines SumOfSquaresPartials into a global population standard deviation."""

max_combiner = Combiner[float, float](
    aggregate=lambda a, b: a if a > b else b,
    identity=-inf,
    finalise=lambda x: x,
)
"""Combines partition maxima into a global maximum."""

min_combiner = Combiner[float, float](
    aggregate=lambda a, b: a if a < b else b,
    identity=inf,
    finalise=lambda x: x,
)
"""Combines partition minima into a global minimum."""

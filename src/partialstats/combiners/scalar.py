from ..partials import SumPartial
from .core import Combiner

sum_combiner = Combiner[SumPartial, float](
    finalise=lambda x: x.sum,
)
"""Combines partial sums into a total sum."""

count_combiner = Combiner[float, float](finalise=lambda x: x)

max_combiner = Combiner[float, float](
    aggregate=lambda a, b: a if a > b else b, finalise=lambda x: x
)
"""Combines partition maxima into a global maximum."""

min_combiner = Combiner[float, float](
    aggregate=lambda a, b: a if a < b else b, finalise=lambda x: x
)
"""Combines partition minima into a global minimum."""

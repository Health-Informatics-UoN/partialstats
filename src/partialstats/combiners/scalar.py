from ..partials import numeric, SumPartial
from .core import Combiner

sum_combiner = Combiner[SumPartial, float](
    finalise=lambda x: x.sum,
)
"""Combines partial sums into a total sum."""

count_combiner = Combiner[numeric.CountPartial, float](
        finalise=lambda x: x.value
        )

max_combiner = Combiner[numeric.MaxPartial, float](
    finalise=lambda x: x.value,
)
"""Combines partition maxima into a global maximum."""

min_combiner = Combiner[numeric.MinPartial, float](
    finalise=lambda x: x.value,
)
"""Combines partition minima into a global minimum."""

from ..partials import scalar, SumPartial
from .core import Combiner

sum_combiner = Combiner[SumPartial, float](
    finalise=lambda x: x.sum,
)
"""Combines partial sums into a total sum."""

count_combiner = Combiner[scalar.CountPartial, float](
        finalise=lambda x: x.value
        )

max_combiner = Combiner[scalar.MaxPartial, float](
    finalise=lambda x: x.value,
)
"""Combines partition maxima into a global maximum."""

min_combiner = Combiner[scalar.MinPartial, float](
    finalise=lambda x: x.value,
)
"""Combines partition minima into a global minimum."""

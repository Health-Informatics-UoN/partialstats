from .core import Combiner

sum_combiner = Combiner[float, float](
    aggregate=lambda a, b: a + b,
    finalise=lambda x: x,
)

max_combiner = Combiner[float, float](
    aggregate=lambda a, b: a if a > b else b, finalise=lambda x: x
)
"""Combines partition maxima into a global maximum."""

min_combiner = Combiner[float, float](
    aggregate=lambda a, b: a if a < b else b, finalise=lambda x: x
)
"""Combines partition minima into a global minimum."""

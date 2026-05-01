from math import inf

from .core import PartialReducer
from .partials import SumPartial, SumOfSquaresPartial


count_reducer = PartialReducer[object, int](
    apply=lambda _: 1,
    merge=lambda a, b: a + b,
    identity=0,
)
"""Counts the number of rows in each partition."""

sum_reducer = PartialReducer[float, SumPartial](
    apply=lambda x: SumPartial(sum=x, count=1),
    merge=lambda a, b: SumPartial(sum=a.sum + b.sum, count=a.count + b.count),
    identity=SumPartial(sum=0, count=0),
)
"""Accumulates the sum and count of values — sufficient to compute mean."""

sum_of_squares_reducer = PartialReducer[float, SumOfSquaresPartial](
    apply=lambda x: SumOfSquaresPartial(sum=x, sumsq=x * x, count=1),
    merge=lambda a, b: SumOfSquaresPartial(
        sum=a.sum + b.sum,
        sumsq=a.sumsq + b.sumsq,
        count=a.count + b.count,
    ),
    identity=SumOfSquaresPartial(sum=0, sumsq=0, count=0),
)
"""Accumulates sum, sum of squares, and count — sufficient to compute variance and std dev."""

max_reducer = PartialReducer[float, float](
    apply=lambda x: x,
    merge=lambda a, b: a if a > b else b,
    identity=-inf,
)
"""Tracks the running maximum value."""

min_reducer = PartialReducer[float, float](
    apply=lambda x: x,
    merge=lambda a, b: a if a < b else b,
    identity=inf,
)
"""Tracks the running minimum value."""

"""
partialstats — distributed statistical aggregation via partial results.
"""

from .partials import Partial, SumPartial, SumOfSquaresPartial
from .combiners import Combiner

__all__ = [
    "Partial",
    "Combiner",
    "SumPartial",
    "SumOfSquaresPartial",
]

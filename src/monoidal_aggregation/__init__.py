"""
partialstats — distributed statistical aggregation via partial results.
"""

from .core import PartialReducer, Combiner, DistributedStat
from .partials import SumPartial, SumOfSquaresPartial
from . import reducers, combiners

__all__ = [
    "PartialReducer",
    "Combiner",
    "DistributedStat",
    "SumPartial",
    "SumOfSquaresPartial",
    "reducers",
    "combiners",
]

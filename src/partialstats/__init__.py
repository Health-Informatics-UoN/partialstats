"""
partialstats — distributed statistical aggregation via partial results.
"""

from .partials import MeanPartial, VariancePartial
from .combiners import Combiner

__all__ = [
    "Combiner",
    "MeanPartial",
    "VariancePartial"
]

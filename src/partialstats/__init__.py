"""
partialstats — distributed statistical aggregation via partial results.
"""

from .partial_results import MeanPartial, VariancePartial, SumSumSqCountPartial

__all__ = ["MeanPartial", "VariancePartial", "SumSumSqCountPartial"]

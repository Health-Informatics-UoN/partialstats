from dataclasses import dataclass


@dataclass
class SumPartial:
    """Partial result carrying a running sum and count."""
    sum: float
    count: int


@dataclass
class SumOfSquaresPartial:
    """Partial result carrying a running sum, sum of squares, and count."""
    sum: float
    sumsq: float
    count: int

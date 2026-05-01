from dataclasses import dataclass

@dataclass
class SumIntermediate:
    sum: float
    count: int


@dataclass
class SumOfSquaresIntermediate:
    sum: float
    sumsq: float
    count: int

from dataclasses import dataclass
from math import inf
from aggregate_functions import InnerFunction

count_rows = InnerFunction[int, int](apply=lambda _: 1, merge=lambda a, b: a + b, identity=0)


@dataclass
class SumIntermediate:
    sum: float
    count: int


@dataclass
class SumOfSquaresIntermediate:
    sum: float
    sumsq: float
    count: int


sum_rows = InnerFunction[float, SumIntermediate](
    apply=lambda x: SumIntermediate(sum=x, count=1),
    merge=lambda a, b: SumIntermediate(sum=a.sum + b.sum, count=a.count + b.count),
    identity=SumIntermediate(sum=0, count=0),
)

sum_of_squares_rows = InnerFunction[float, SumOfSquaresIntermediate](
    apply=lambda x: SumOfSquaresIntermediate(sum=x, sumsq=x * x, count=1),
    merge=lambda a, b: SumOfSquaresIntermediate(
        sum=a.sum + b.sum, sumsq=a.sumsq + b.sumsq, count=a.count + b.count
    ),
    identity=SumOfSquaresIntermediate(sum=0, sumsq=0, count=0),
)

max_rows = InnerFunction[float, float](
        apply=lambda x: x,
        merge=lambda a, b: a if a > b else b,
        identity=-inf
        )

min_rows = InnerFunction[float, float](
        apply=lambda x: x,
        merge=lambda a, b: a if a < b else b,
        identity=inf
        )

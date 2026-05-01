from math import inf

from .aggregate_functions import OuterFunction
from .inner_functions import SumIntermediate, SumOfSquaresIntermediate

sum_intermediates = OuterFunction[float, float](
        aggregate=lambda a, b: a + b,
        identity=0,
        finalise=lambda x: x
        )

gather_avg_intermediates = OuterFunction[SumIntermediate, float](
        aggregate=lambda a, b: SumIntermediate(sum=a.sum + b.sum, count=a.count + b.count),
        identity=SumIntermediate(0,0),
        finalise=lambda x: x.sum/x.count
        )

gather_var_intermediates = OuterFunction[SumOfSquaresIntermediate, float](
        aggregate=lambda a, b: SumOfSquaresIntermediate(sum=a.sum+b.sum, sumsq=a.sumsq + b.sumsq, count = a.count + b.count),
        identity=SumOfSquaresIntermediate(0,0,0),
        finalise=lambda x: x.sumsq/x.count - (x.sum/x.count * x.sum/x.count)
        )

max_intermediates = OuterFunction[float, float](
        aggregate=lambda a,b: a if a>b else b,
        identity=-inf,
        finalise=lambda x: x
        )

min_intermediates = OuterFunction[float, float](
        aggregate=lambda a,b: a if a<b else b,
        identity=inf,
        finalise=lambda x: x
        )

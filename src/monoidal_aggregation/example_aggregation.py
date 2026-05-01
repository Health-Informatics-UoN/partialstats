from .aggregate_functions import AlgebraicAggregate
from .inner_functions import sum_rows
from .outer_functions import gather_avg_intermediates

federated_mean = AlgebraicAggregate(sum_rows, gather_avg_intermediates)

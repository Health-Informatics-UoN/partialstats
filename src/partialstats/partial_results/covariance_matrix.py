from typing import Self
from dataclasses import dataclass
from .protocol import AddsProtocol, CountPartialProtocol

try:
    import pandas as pd

    @dataclass
    class CovarianceMatrixPartial(CountPartialProtocol, AddsProtocol):
        count: int
        sums: dict[str, float]
        product_sums: pd.DataFrame

        def __post_init__(self):
            variables = set(self.sums.keys())
            if set(self.product_sums.columns) != set(self.product_sums.index) != variables:
                raise KeyError("Variable names for product sums and sums do not match")

        def __add__(self, other: Self) -> Self:
            if set(self.sums.keys()) == set(other.sums.keys()):
                aggregate_sums = {k: v + other.sums[k] for k, v in self.sums.items()}
                return type(self)(
                    count=self.count + self.count,
                    sums=aggregate_sums,
                    product_sums=self.product_sums + other.product_sums,
                )
            else:
                raise KeyError("Variable names do not match")

except ImportError as e:
    raise ImportError(
        "Aggregating covariance matrices requires pandas. Install it with: pip install partialstats[pandas]"
    ) from e

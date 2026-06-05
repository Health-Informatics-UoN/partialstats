# partialstats

Compute statistics across partitioned data without centralising it.

Each node reduces its own rows to a small **partial result**. A single aggregator then combines those partials into the final statistic. The data never has to be in one place at once.

---

## The idea

Many common statistics — mean, variance, max, min — can be computed in two passes:

1. **Reduce**: each partition independently computes a lightweight summary (a *partial result*).
2. **Aggregate**: An aggregator merges partial results
3. **Finalise**: The final answer can be calculated from the aggregation

This works because each statistic's partial result forms a [commutative monoid](https://en.wikipedia.org/wiki/Monoid): partial results can be merged in any order and the answer is the same. `partialstats` makes this pattern explicit and composable.

---

## Glossary

| Term | Definition |
| ---- | ---------- |
| Partial result | In a distributed analysis, each node can return a single summary value, a *partial result* that can be used to get to your final result |
| `Iterable` | Here, specifically a [python type](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable) that can return its members one at a time |
| Reduce | A function that takes another function, which takes an initial value and combines each value of an iterable with that |
| Aggregate | Gather partial results into a summary of the data in all nodes as if they were one dataset |
| Finalise | Take an aggregated summary of a dataset and use it to calculate a desired statistic |
| Aggregate/Transform | Aggregate partial statistics then use the aggregated summary to calculate a desired statistic |

---

## Quick start

```python
from partialstats.reference import DistributedStat, sum_reducer, sum_of_squares_reducer
from partialstats.aggregate_transforms import mean, variance, std

# Compute the mean of values spread across partitions
distributed_mean = DistributedStat(sum_reducer, mean)

# Compute variance and std dev (same reducer, different aggregation)
distributed_variance = DistributedStat(sum_of_squares_reducer, variance)
distributed_std = DistributedStat(sum_of_squares_reducer, std)

if __name__ == "__main__":
    partitions = [
        [1.0, 2.0, 3.0],
        [4.0, 5.0],
        [6.0, 7.0, 8.0, 9.0, 10.0],
    ]

    print(f"Mean:     {distributed_mean.compute(partitions)}")  # 5.5
    print(f"Variance: {distributed_variance.compute(partitions)}")  # 8.25
    print(f"Std dev:  {distributed_std.compute(partitions):.3f}")  # ~2.872
```

---

## Core concepts

### `aggregate_transform`
The most important part of partialstats can be summarised in a few lines:

```python
def aggregate_transform(aggregate, finalise, partials):
  first, *rest = partials
  return finalise(reduce(aggregate, rest, first))
```

The way to understand this is from the inside out:

- `reduce(aggregate, rest, first)` uses the `aggregate` function to combine partial results
- `finalise(...)` applies the `finalise` function to take the combined result and calculate your final result

The rest of the library provides nice ways to run this function, and to tell your IDE what you're trying to do.

### Partial results

Partial results are summary values returned from a node, which can be combined together to summarise a dataset held in multiple nodes.
For scalar values and simple aggregations, combining these values is simple:

```python
def sum_combiner(partials: list[float]) -> float:
    """Returns the sum of a list of partials"""
    return aggregate_transform(
        aggregate=lambda a, b: a + b, finalise=lambda x: x, partials=partials
    )
```

To sum values, you just need to add them together, then return the result.

#### Adding partial results
For other statistics, the values are not a single, scalar value, but some $n$-tuple of values but "adding" the data structure together is still the sensible way of thinking about it.
Python lets you define what happens with the `+` symbol by overriding the `__add__` method.

```python
@dataclass
class SumSumSqCountPartial(SumSumSqCountPartialProtocol, AddsProtocol):
    """Partial result carrying a running sum, sum of squares, and count."""

    sum: float
    sum_of_squares: float
    count: int

    def __add__(self, other: Self) -> Self:
        return type(self)(
            self.sum + other.sum,
            self.sum_of_squares + other.sum_of_squares,
            self.count + other.count,
        )
```

This means we can use similar `aggregate_transform` functions for these structures.
Since this is such a common pattern, `sum_and_transform` is supplied as a function that only requires a `finalise` function and an Iterable of partial results.

---

## Included batteries
### `aggregate_transforms` functions
Common statistics can be calculated on partial results using functions from `partialstats.aggregate_transforms`

- count
- sum
- mean
- variance
- std (standard deviation)

### Partial results
Containers for common univariate statistics are Included

- `MeanPartial` contains sum and count data
- `SumSumSqCountPartial` contains sum, sum of squares, and count data
- `VariancePartial` contains variance data

### `StatAggregator`s
`StatAggregator`s are containers for data with properties that provide common statistics.

---

## Writing your own

To show how advanced users can write their own aggregations using the features in this library, this shows how the aggregation of variance values was designed.
When this was added, variance could already be calculated from the sum, count, and sum of squares, but variance can also be aggregated by [adding in quadrature](https://en.wikipedia.org/wiki/Pythagorean_addition).

First, write a dataclass that can hold your value (in this case a single `variance` value), and an `__add__` method.

```python
from math import hypot
from typing import Self
from dataclasses import dataclass

@dataclass
class VariancePartial(VariancePartialProtocol, AddsProtocol):
    """Partial result carrying the running pythagorean sum of variance"""

    variance: float

    def __add__(self, other: Self) -> Self:
        return type(self)(hypot(self.variance, other.variance))
```

Then write a function that aggregates then transforms the data.
In this case, it's simple because `__add__` is defined on your class.
There's more scaffolding around this in the package, but the essence is here.

```python
def variance(partials: Iterable[VariancePartial]):
  return sum_and_transform(lambda x: x.variance, partials)
```

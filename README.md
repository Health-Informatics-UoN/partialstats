# partialstats

Compute statistics across partitioned data without centralising it.

Each node reduces its own rows to a small **partial result**. A single aggregator then combines those partials into the final statistic. The data never has to be in one place at once.

---

## The idea

Many common statistics — mean, variance, max, min — can be computed in two passes:

1. **Reduce**: each partition independently computes a lightweight summary (a *partial result*).
2. **Combine**: an aggregator merges the partials and produces the final answer.

This works because each statistic's partial result forms a [commutative monoid](https://en.wikipedia.org/wiki/Monoid): partial results can be merged in any order and the answer is the same. `partialstats` makes this pattern explicit and composable.

---

## Quick start

```python
from partialstats.reference import DistributedStat, sum_reducer, sum_of_squares_reducer
from partialstats.combiners import mean_combiner, variance_combiner, std_combiner

# Compute the mean of values spread across partitions
distributed_mean = DistributedStat(sum_reducer, mean_combiner)

# Compute variance and std dev (same reducer, different combiner)
distributed_variance = DistributedStat(sum_of_squares_reducer, variance_combiner)
distributed_std = DistributedStat(sum_of_squares_reducer, std_combiner)

if __name__ == "__main__":
    partitions = [
        [1.0, 2.0, 3.0],
        [4.0, 5.0],
        [6.0, 7.0, 8.0, 9.0, 10.0],
    ]

    print(f"Mean:     {distributed_mean.compute(partitions)}")       # 5.5
    print(f"Variance: {distributed_variance.compute(partitions)}")   # 8.25
    print(f"Std dev:  {distributed_std.compute(partitions)}")        # ~2.872
```

---

## Core concepts

### `Combiner[S, R]`

Runs on the aggregator. Merges partial results of type `S` into a final result of type `R`.

```python
from partialstats import Combiner

sum_combiner = Combiner[float, float](
    aggregate=lambda a, b: a + b,
    identity=0,
    finalise=lambda x: x,
)
```


---

## Built-in reducers

| Name | Partial type | Use for |
|---|---|---|
| `count_reducer` | `int` | counting rows |
| `sum_reducer` | `SumPartial` | sum, mean |
| `sum_of_squares_reducer` | `SumOfSquaresPartial` | variance, std dev |
| `max_reducer` | `float` | maximum |
| `min_reducer` | `float` | minimum |

## Built-in combiners

| Name | Partial type | Final type | Statistic |
|---|---|---|---|
| `sum_combiner` | `float` | `float` | total sum |
| `mean_combiner` | `SumPartial` | `float` | mean |
| `variance_combiner` | `SumOfSquaresPartial` | `float` | population variance |
| `std_combiner` | `SumOfSquaresPartial` | `float` | population std dev |
| `max_combiner` | `float` | `float` | maximum |
| `min_combiner` | `float` | `float` | minimum |

---

## Writing your own

Reducers and combiners are plain dataclasses — just provide the functions.

A `Partial` isn't hard to write either.
It's just a class that implements the `__add__` special method so that you can combine partial results.

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

## Install

```
pip install partialstats
```

---

## Quick start

```python
from partialstats import DistributedStat
from partialstats.reducers import sum_reducer, sum_of_squares_reducer
from partialstats.combiners import mean_combiner, variance_combiner

partitions = [
    [1.0, 2.0, 3.0],
    [4.0, 5.0],
    [6.0, 7.0, 8.0, 9.0, 10.0],
]

mean     = DistributedStat(sum_reducer,            mean_combiner).compute(partitions)
variance = DistributedStat(sum_of_squares_reducer, variance_combiner).compute(partitions)

print(mean)      # 5.5
print(variance)  # 8.25
```

---

## Core concepts

### `PartialReducer[T, S]`

Runs on each partition. Converts rows of type `T` into a partial result of type `S`.

```python
from partialstats import PartialReducer

count_reducer = PartialReducer[object, int](
    apply=lambda _: 1,        # map each row to a value
    merge=lambda a, b: a + b, # fold values together
    identity=0,               # starting value
)
```

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

### `DistributedStat[T, S, R]`

Pairs a `PartialReducer` with a `Combiner` and exposes a single `.compute(partitions)` method.

```python
from partialstats import DistributedStat

stat = DistributedStat(reducer=my_reducer, combiner=my_combiner)
result = stat.compute(partitions)
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

**Example: median of medians (approximate distributed median)**

```python
import statistics
from partialstats import PartialReducer, Combiner, DistributedStat

# Each partition computes its own median
local_median_reducer = PartialReducer[float, float](
    apply=lambda x: x,
    merge=lambda a, b: (a + b) / 2,   # placeholder; see note below
    identity=0.0,
)

# Combine local medians with a simple mean (approximate)
approx_median_combiner = Combiner[list[float], float](
    aggregate=lambda a, b: a + b,
    identity=[],
    finalise=statistics.median,
)
```

> **Tip**: not every statistic has a perfect distributed form. When in doubt, check whether your partial result type is a commutative monoid — i.e. whether `merge(a, merge(b, c)) == merge(merge(a, b), c)` and `merge(a, b) == merge(b, a)`.

---

## Why "partial results" and not "intermediates"?

"Intermediate" implies a step in a pipeline. "Partial" captures the actual meaning: each node has *part of the answer*, and combining the parts gives the whole. The monoid structure is what makes combining valid — but you don't need to know that to use the library.

---

## Licence

MIT

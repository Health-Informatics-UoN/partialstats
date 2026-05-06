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

    print(f"Mean:     {distributed_mean.compute(partitions)}")  # 5.5
    print(f"Variance: {distributed_variance.compute(partitions)}")  # 8.25
    print(f"Std dev:  {distributed_std.compute(partitions)}")  # ~2.872

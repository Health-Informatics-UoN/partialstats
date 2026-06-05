from .core import aggregate_transform


def sum_combiner(partials: list[float]) -> float:
    """Returns the sum of a list of partials"""
    return aggregate_transform(
        aggregate=lambda a, b: a + b, finalise=lambda x: x, partials=partials
    )


def max_combiner(partials: list[float]) -> float:
    """Combines partition maxima into a global maximum."""
    return aggregate_transform(
        aggregate=lambda a, b: a if a > b else b,
        finalise=lambda x: x,
        partials=partials,
    )


def min_combiner(partials: list[float]) -> float:
    """Combines partition minima into a global minimum."""
    return aggregate_transform(
        aggregate=lambda a, b: a if a < b else b,
        finalise=lambda x: x,
        partials=partials,
    )

# Monoidal aggregation in python

This shows some examples of how to use monoids to aggregate statistics using python.

There are better ways of implementing monoids in python, but this is a quick, and hopefully clear way to represent the concept.

The components of the system are generic dataclasses:

- `InnerFunction` is applied to sub-arrays
    - `apply` takes some type `T` and uses it to build some intermediate type `S`
    - `merge` takes two instances of `S` and outputs another
    - `identity` describes the identity element of `S`
- `OuterFunction` is applied to intermediates
    - `aggregate` takes two instances of `S` and outputs another
    - `identity` describes the identity element of `S`
    - `finalise` uses `S` to build the final result of type `R`
- `AlgebraicAggregate` ties the two together, showing a route from `T` to `R`

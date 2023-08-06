"""
Utility functions for dealing with random variables.
"""
from numbers import Number

import torch

from borch.tensor import RandomVariable, TransformedParameter
from borch.utils.torch_utils import is_numeric


def observed_random_variables(random_variables):
    """Filter an iterable of `RandomVariable` objects for instances that are
    observed.

    Args:
        random_variables (iterable: RandomVariable): RandomVariable objects to
          filter.

    Yields:
        RandomVariable objects which are observed.

    Examples:
        >>> import torch
        >>> from borch import RV, distributions
        >>>
        >>> dist = distributions.Normal(torch.ones(1), torch.ones(1))
        >>> rvs = [RV(dist) for _ in range(3)]
        >>> rvs[1].observe(torch.ones(1))
        RandomVariable containing:
        tensor([1.])
        >>> len(list(observed_random_variables(rvs)))
        1
    """
    return (rv for rv in random_variables if rv.observed is not None)


def latent_random_variables(random_variables):
    """Filter an iterable of `RandomVariable` objects for instances that are
    not observed (i.e. latent).

    Args:
        random_variables (iterable: RandomVariable): RandomVariable objects to
          filter.

    Yields:
        RandomVariable objects which are not observed.

    Examples:
        >>> import torch
        >>> from borch import RV, distributions
        >>>
        >>> dist = distributions.Normal(torch.ones(1), torch.ones(1))
        >>> rvs = [RV(dist) for _ in range(3)]
        >>> rvs[1].observe(torch.ones(1))
        RandomVariable containing:
        tensor([1.])
        >>> len(list(latent_random_variables(rvs)))
        2
    """
    return (rv for rv in random_variables if rv.observed is None)


def copy_random_variable_properties(original: RandomVariable, new: RandomVariable):
    """Move observed values and any `TransformedParameter`s arguments from
    an original `RandomVariable` to a new `RandomVariable`.

    Any arguments in the new random variable's distribution which are numeric
    (see is_numeric) but not transformed parameters will have their values
    copied from the original random variable's distribution (todo: why??).

    Args:
        original: The original `RandomVariable` object with properties to copy.
        new: The new `RandomVariable` that properties should be copied to.

    Returns:
        The `RandomVariable` `new` with new properties copied from `original`.
    """
    new.observe(original.observed)
    original_dist = original.q_dist or original.distribution
    for name, arg in new.distribution.arguments.items():
        if not isinstance(arg, TransformedParameter) and is_numeric(arg):
            new.distribution.arguments[name] = original_dist.arguments[name]
    return new


def requires_grad(tensor) -> bool:
    """Checks if a tensor/number requires gradient.

    Args:
        tensor: Tensor or numeric argument to check for `requires_grad`.

    Returns:
        Whether or not `tensor` had a requires_grad attribute which is set
        to `True`.
    """
    if isinstance(tensor, Number):
        return False
    if isinstance(tensor, RandomVariable):
        return any(param.requires_grad for param in tensor.parameters())
    if isinstance(tensor, torch.Tensor):
        return tensor.requires_grad

    msg = f"tensor must be valid numeric type, not '{type(tensor).__name__}'"
    raise TypeError(msg)


def named_observed_random_variables(named_rvs):
    """
    Yield observed random variables form an iterable, where one index of the iterable
    consists of (name, rv).

    Args:
        named_rvs (iterable, where one index of the iterable consists of (name, rv).

    Yields:
        name, rv , if the rv is oberved

    """
    for name, rv in named_rvs:
        if rv.observed is not None:
            yield name, rv

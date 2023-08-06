# pylint: disable=not-callable
"""Utility functions used in the model interface"""

from numbers import Number
from typing import Union

import torch
from torch import Tensor

from borch.tensor import RandomVariable, TransformedParameter
from borch.distributions.distributions import (
    Distribution,
    Normal,
    TransformedDistribution,
    Delta,
)
from borch.utils import requires_grad
from borch.distributions import constraints
from borch.distributions.constraints_registry import transform_to
from borch.utils.torch_utils import is_numeric


def _get_constraint(name, distribution):
    if name in distribution.arg_constraints:
        return distribution.arg_constraints[name]
    if name == "logits":
        return constraints.real
    raise LookupError("Unable to identify the constraint for %s" % name)


def _val_to_tp(value, constraint):
    unconstrained = (
        transform_to(constraint).inv(value).clone().detach().requires_grad_(True)
    )
    value = TransformedParameter(transform_to(constraint), unconstrained)
    return value


def detach_dist(distribution: Distribution) -> Distribution:
    """Takes a `ppl.distributions.Distribution` and creates a new
    distributioon where the gradient does not proppegate trough the
    arguments of the distribution.

    Args:
      distribution: Distributon to clone where the clone does not
        proppegate the gradient to the arguments.

    Returns:
        A `ppl.distributions.Distribution` whose arguments can
        not be optimized.

    Example:
        >>> normal = Normal(0, 1)
        >>> detach_dist(normal)
        Normal(loc: 0.0, scale: 1.0)
    """
    args_distb = {}
    for name, value in distribution.arguments.items():
        if is_numeric(value):
            value = value.clone().detach()
        args_distb[name] = value
    return type(distribution)(**args_distb)


def dist_to_qdist(distribution):
    """Takes a `torch.distributions.Distribution` and converts it to a new
    distribution whose arguments can be optimised.

    If the args in the distribution are none in the field `_grad_fn` it will
    return a TransformedParameter consisting of the same type of transformation
    as its constraints dictates and with the variable being in the
    unconstrained space and detached, else the variable will just be returned.

    Args:
      distribution: torch.distributions.Distribution

    Returns:
        A `ppl.distributions.Distribution` whose arguments can be optimised.
    """
    args_approximating_distb = {}
    for name, value in distribution.arguments.items():
        if is_numeric(value):
            value = _val_to_tp(value, _get_constraint(name, distribution))
        args_approximating_distb[name] = value
    return type(distribution)(**args_approximating_distb)


def dist_to_qdist_infer_hierarchy(distribution):
    """Takes a `torch.distributions.Distribution` and converts it to a new
    distribution whose arguments can be optimised.

    If the args in the distribution are none in the field `_grad_fn` it will
    return a TransformedParameter consisting of the same type of transformation
    as its constraints dictates and with the variable being in the
    unconstrained space and detached, else the variable will just be returned.

    Args:
      distribution: torch.distributions.Distribution

    Returns:
        A `ppl.distributions.Distribution` whose arguments can be optimised.
    """
    args_approximating_distb = {}
    for name, value in distribution.arguments.items():
        if is_numeric(value) and not requires_grad(value):
            value = _val_to_tp(value, _get_constraint(name, distribution))
        args_approximating_distb[name] = value
    return type(distribution)(**args_approximating_distb)


def normal_distribution_from_rv(
    rv: RandomVariable, log_scale: Union[Tensor, Number]
) -> Normal:
    """Create a Normal distribution with optimisable arguments from an
    existing random variable. The loc of the returned distribution is set
    to the current value of ``rv``.

    Args:
        rv: A `RandomVariable` from which to use the value as the
          loc of the Normal.
        log_scale: Log of the scale for the created normal distribution.

    Returns:
        A new distribution of type :class:`borch.ppl.distributions.Normal`.

    Raises:
        TypeError if ``rv`` does not have `real` support.

    Notes:
        When ``rv`` does not have a finite value the underlying distribution
        is sampled to create the mean for the normal distribution.
    """
    # todo check that support is continuous, currently not implemented in torch
    loc_init = (rv * 1).detach()
    if not torch.isfinite(loc_init).all():
        loc_init = rv.distribution.sample()
    scale = (loc_init * 0 + log_scale).clone().detach().requires_grad_(True)
    scale = TransformedParameter(torch.exp, scale)

    if rv.distribution.support is constraints.real:
        loc = loc_init.clone().detach().requires_grad_(True)
        return Normal(TransformedParameter(no_op, loc), scale)

    loc = transform_to(rv.support).inv(loc_init).clone().detach().requires_grad_(True)
    return TransformedDistribution(Normal(loc, scale), [transform_to(rv.support)])


def delta_distribution_from_rv(rv):
    """Create a Delta distribution with optimisable argument from an
    existing random variable. The value of the returned distribution is set
    to the current value of :arg:`rv`.

    Args:
        rv: A `RandomVariable` from which to use the value as the
          loc of the Normal.

    Returns:
        A new distribution of type :class:`borch.ppl.distributions.Delta`.
    """
    # todo check that support is continuous, currently not implemented in torch
    loc_init = (rv * 1).detach()
    if not torch.isfinite(loc_init).all():
        loc_init = rv.distribution.sample()

    if rv.distribution.support is constraints.real:
        loc = loc_init.clone().detach().requires_grad_(True)
        return Delta(loc)

    loc = transform_to(rv.support).inv(loc_init).clone().detach().requires_grad_(True)
    return TransformedDistribution(Delta(loc), [transform_to(rv.support)])


def scaled_normal_dist_from_rv(rv, scaling):
    """Create a Normal distribution with optimisable arguments from an
    existing random variable. The loc of the returned distribution is set
    to the current value of ``rv``.

    Where the scale in initilized as `rv.stddev*scaling` in the constrained space.

    Args:
        rv: A `RandomVariable` from which to use the value as the
          loc of the Normal.
        scaling: the degree of scaling of the stddev of the prior to use for
            the scale of the created normal distribution.

    Returns:
        A new distribution of type :class:`borch.ppl.distributions.Normal`.

    Raises:
        TypeError if ``rv`` does not have `REAL` support.

    Notes:
        When ``rv`` does not have a finite value the underlying distribution
        is sampled to create the mean for the normal distribution.
    """
    if rv.distribution.support != constraints.real:
        raise TypeError("only variables with support real is supported")
    scale = (
        (rv.distribution.stddev * scaling).log().clone().detach().requires_grad_(True)
    )
    scale = TransformedParameter(torch.exp, scale)

    loc_init = rv
    if not torch.isfinite(loc_init).all():
        loc_init = rv.distribution.sample()
    loc = loc_init.clone().detach().requires_grad_(True)
    return Normal(TransformedParameter(no_op, loc), scale)


def no_op(x):  # pylint: disable=missing-docstring
    return x

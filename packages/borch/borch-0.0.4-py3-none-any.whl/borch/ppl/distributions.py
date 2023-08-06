# pylint: disable=abstract-method,undefined-all-variable
"""
Borch proxy for `torch.distributions`.
"""
from functools import wraps
from numbers import Number
import inspect

import torch
from torch import distributions
from torch.distributions import kl_divergence
from torch.distributions import constraints as tc

from borch.tensor.transformed_parameter import TransformedParameter
from borch.utils.func_tools import args_to_kwargs, assign_docs
from borch.utils.namespace_tools import create_augmented_classes
from borch.utils.torch_utils import dict_values_to_tensor
from borch.distributions import constraints
from borch.distributions.transforms import Transform, ExpTransform
from borch.distributions.constraints_registry import transform_to

__all__ = [
    "Bernoulli",
    "Beta",
    "Binomial",
    "Categorical",
    "Cauchy",
    "Chi2",
    "Distribution",
    "Dirichlet",
    "Exponential",
    "ExponentialFamily",
    "FisherSnedecor",
    "Gamma",
    "Geometric",
    "Gumbel",
    "Independent",
    "kl_divergence",
    "Laplace",
    "LogNormal",
    "LogisticNormal",
    "Multinomial",
    "MultivariateNormal",
    "Normal",
    "OneHotCategorical",
    "Pareto",
    "PointMass",
    "Poisson",
    "RelaxedBernoulli",
    "RelaxedOneHotCategorical",
    "StudentT",
    "TransformedDistribution",
    "Uniform",
]


class Distribution(distributions.Distribution):
    """
    Borch distributions class.

    It inherits from the different
    torch.distributions to add some extra functionality.
    """

    def __init__(self, *args, **kwargs):
        arguments = args_to_kwargs(super().__init__, *args, **kwargs)
        self.arguments = dict_values_to_tensor(arguments)
        super().__init__(**_tp_to_new_node(**self.arguments))

    @property
    def _parameters(self):
        return {
            key: val
            for key, val in self.arguments.items()
            if isinstance(val, torch.Tensor)
        }

    def _recreate_distribution(self):
        """
        Creates a new distribution using the same input that self was created
        with.

        Note:
            If any of the input arguments have been modified, then the returned
            distribution reflects these changes (the same _object_ is used, not
            a copy of the object).

        Returns:
            Distribution of type `type(self)`.
        """
        return type(self)(**self.arguments)

    def named_parameters(self):
        """
        Returns:
            A generator of (key, value) pairs of the parameters of the distribtution

        """
        for key, val in self._parameters.items():
            yield key, val

    def parameters(self):
        """
        Returns:
            A generator of the distributions parameters' values.

        """

        for _, val in self.named_parameters():
            yield val

    def _recalculate_transformed_parameter(self):
        """Recalculates all arguments of the distribution that are an instance
        of `TransformedParameter`.
        """
        for var in self.parameters():
            if isinstance(var, TransformedParameter):
                var.recalculate()

    def recalculate(self):
        """
        Recalculates all arguments of the distribution that are an instance
        of `TransformedParameter` and returns a new distribution with the
        updated values.

        Returns:
            a ppl distribution with the same type as self.
        """
        self._recalculate_transformed_parameter()
        return self._recreate_distribution()


def _torch_borch_constraints_map():
    lookup = {}
    for name, torch_constraint in inspect.getmembers(
        tc, lambda obj: isinstance(obj, tc.Constraint)
    ):
        borch_constraint = getattr(constraints, name, None)
        if not borch_constraint is None:
            lookup[torch_constraint] = borch_constraint
    return lookup


_TORCH_BORCH_CONSTRAINTS_MAP = _torch_borch_constraints_map()


def _get_borch_constraint(constraint):
    if constraint in _TORCH_BORCH_CONSTRAINTS_MAP:
        return _TORCH_BORCH_CONSTRAINTS_MAP[constraint]
    return constraints.constraint_from_string(str(constraint))


def _distb_class_creator(cls):
    """Creates a ppl Distirbution that inherits from `cls`."""
    prefix = (
        "This is a ppl class. Please see `help(borch.ppl.distribution)`"
        " for more information."
    )

    @wraps(cls.__init__)
    def _init(*args, **kwargs):
        return Distribution.__init__(*args, **kwargs)

    if isinstance(cls.arg_constraints, dict):
        arg_constraints = {
            key: _get_borch_constraint(val) for key, val in cls.arg_constraints.items()
        }
    else:
        arg_constraints = cls.arg_constraints

    if isinstance(cls.support, tc.Constraint):
        support = _get_borch_constraint(cls.support)
    else:
        support = cls.support
    new_cls = type(
        cls.__name__,
        (Distribution, cls),
        {"__init__": _init, "arg_constraints": arg_constraints, "support": support},
    )
    assign_docs(new_cls, cls, prefix)
    return new_cls


create_augmented_classes(
    caller=__name__,
    module=distributions,
    parent=distributions.Distribution,
    class_factory=_distb_class_creator,
)


class TransformedDistribution(Distribution, distributions.TransformedDistribution):
    # pylint: disable=missing-docstring,super-init-not-called,non-parent-init-called
    __doc__ = distributions.TransformedDistribution.__doc__

    def __init__(self, base_distribution, transforms, validate_args=None):

        self.base_dist = base_distribution
        if not isinstance(transforms, (list, tuple)):
            transforms = [transforms]
        if not all(isinstance(t, Transform) for t in transforms):
            raise ValueError("transforms must be a Transform or a list of Transforms")
        self.transforms = transforms
        shape = self.base_dist.batch_shape + self.base_dist.event_shape
        event_dim = max(
            [len(self.base_dist.event_shape)] + [t.event_dim for t in self.transforms]
        )
        batch_shape = shape[: len(shape) - event_dim]
        event_shape = shape[len(shape) - event_dim :]
        self.arguments = {
            "base_distribution": base_distribution,
            "transforms": transforms,
            "validate_args": validate_args,
        }
        distributions.Distribution.__init__(self, batch_shape, event_shape)

    @property
    def _parameters(self):
        return dict(self.base_dist.named_parameters())


class LogNormal(TransformedDistribution, distributions.LogNormal):
    # pylint: disable=missing-docstring,super-init-not-called,non-parent-init-called
    __doc__ = distributions.TransformedDistribution.__doc__

    arg_constraints = {"loc": constraints.real, "scale": constraints.positive}
    support = constraints.positive
    has_rsample = True

    def __init__(self, loc, scale, validate_args=None):
        # pylint: disable=not-callable,undefined-variable
        loc = torch.tensor(float(loc)) if isinstance(scale, Number) else loc
        scale = torch.tensor(float(scale)) if isinstance(scale, Number) else scale
        base_dist = Normal(loc, scale)
        TransformedDistribution.__init__(
            self, base_dist, ExpTransform(), validate_args=validate_args
        )
        self.arguments = {"loc": loc, "scale": scale}

    @property
    def _parameters(self):
        return {"loc": self.loc, "scale": self.scale}

    def _recreate_distribution(self):
        """Recreates the distribution with the original kwargs self was
        created with.

        Note:
            if one of the kwargs is a tensor it will create with the current
            value and not the value it was created with.

        Returns:
            object of type self
        """
        new = super()._recreate_distribution()
        # import ipdb; ipdb.set_trace()
        new.__dict__ = self.__dict__.copy()
        return new


#     def recalculate(self):
#         """
#         Recalculates all arguments of the distribution that are an instance
#         of `TransformedParameter` and returns a new distribution with the
#         updated values.
#
#         Returns:
#             a ppl distribution with the same type as self.
#         """
#         self._recalculate_transformed_parameter()
#         return self._recreate_distribution()


class Delta(Distribution):
    """Implements a Delta distribution

    Example:
        >>> dist = Delta(0)
        >>> float(dist.sample())
        0.0
    """

    # pylint: disable=not-callable
    has_rsample = True

    def __init__(self, value, event_shape=torch.Size()):
        if isinstance(value, Number):
            value = torch.tensor(float(value))
        batch_shape = value.size()
        super().__init__(batch_shape, event_shape)
        self.arguments = {"value": value, "event_shape": event_shape}
        self._support = constraints.real
        self._arg_constraints = {"value": constraints.real}

    @property
    def value(self):
        """ Get the value of the distribution """
        return dict(self.named_parameters())["value"]

    @property
    def support(self):
        """Get the support of the distribution"""
        return self._support

    @property
    def mean(self):
        return self.rsample()

    @property
    def variance(self):
        return torch.zeros_like(self.rsample())

    @property
    def arg_constraints(self):
        """The constraints of the arguments on self."""
        return self._arg_constraints

    def rsample(self, sample_shape=torch.Size()):
        """Returns transformed value according to the support.

        Returns:
            The current constrained value, expanded to the shape of
            `sample_shape`.
        """
        shape = self._extended_shape(sample_shape)
        return self.value.expand(shape)

    def sample(self, sample_shape=torch.Size()):
        with torch.no_grad():
            return self.rsample(sample_shape).detach()

    def _recreate_distribution(self):
        """Recreates the distribution with the original kwargs self was
        created with.

        Note:
            if one of the kwargs is a tensor it will create with the current
            value and not the value it was created with.

        Returns:
            object of type self
        """
        new = super()._recreate_distribution()
        new.__dict__ = self.__dict__.copy()
        return new

    def log_prob(self, value):
        return (value == self.value).to(value.dtype).to(value.device).log()


class PointMass(Distribution):
    """Implements a PointMass distribution, it takes an unconstrained value
    and constrains it according to the provided support.
    """

    # pylint: disable=not-callable
    has_rsample = True

    def __init__(self, u_tensor, support, event_shape=torch.Size()):
        if isinstance(u_tensor, TransformedParameter):
            raise RuntimeError("u_tensor should not be a TransformedParameter")
        if isinstance(u_tensor, Number):
            u_tensor = torch.tensor(float(u_tensor))
        batch_shape = u_tensor.size()
        super().__init__(batch_shape, event_shape)
        self.arguments = {"u_tensor": u_tensor, "support": support}
        self._support = support
        self.transformation = transform_to(support)
        self._samples = []
        self._arg_constraints = {"u_tensor": constraints.real}
        self.index = None

    @property
    def u_tensor(self):
        """ Get the unconstrained tensor of the distribution """
        return self.arguments["u_tensor"]

    @property
    def support(self):
        """The support of the point mass distribution (determined at
        initialisation).
        """
        return self._support

    @property
    def arg_constraints(self):
        """The constraints of the arguments on self."""
        return self._arg_constraints

    @property
    def value(self):
        """The unconstrained value transformed according to the support."""
        return self.transformation(self.u_tensor)

    def rsample(self, sample_shape=torch.Size()):
        """Returns transformed value according to the support.

        Returns:
            The current constrained value, expanded to the shape of
            `sample_shape`.
        """
        shape = self._extended_shape(sample_shape)
        self.index = None
        return self.value.expand(shape)

    # pylint: disable=arguments-differ
    def sample(self, sample_shape=torch.Size(), index=None):
        """Updates the values of the parameters with the saved samples
        if an index is provided, else it returns a self.value.detach()

        Args:
            sample_shape: shape of the desired sample
            index (int), the index location of the saved samples.

        Notes:
            It is not possible to get gradients through this method.

        Returns:
            torch.tensor
        """
        if index is None:
            index = self.index
        else:
            self.index = index
        if index is None:
            return self.rsample().detach()

        if not self._samples:
            raise IndexError("No samples has been stored")

        shape = self._extended_shape(sample_shape)
        return self.transformation(self._samples[index]).expand(shape)

    def save_state_as_sample(self):
        """Saves the current unconstrained values, such that they can be used
        as samples by calling `sample`.
        """
        self._samples.append(self.u_tensor.data.clone())

    def _recreate_distribution(self):
        """
        Recreates the distribution with the original kwargs self was created
        with.

        Note:
            if one of the kwargs is a tensor it will create with the current
            value and not the value it was created with.
        Returns:
            object of type self
        """
        new = super()._recreate_distribution()
        new.__dict__ = self.__dict__.copy()
        return new


def _tp_to_new_node(**kwargs):
    """
    Hack to create new nodes for TransformedParameter's that are used in the graph
    """
    arguments = {}
    for key, val in kwargs.items():
        if isinstance(val, TransformedParameter):
            val = val.clone()  # new node in graph
        arguments[key] = val
    return arguments


class Categorical(Distribution, distributions.Categorical):
    # pylint: disable=missing-docstring,super-init-not-called
    __doc__ = distributions.Categorical.__doc__.replace(">>>", ">>")
    arg_constraints = {"probs": constraints.simplex, "logits": constraints.real}

    @wraps(distributions.Categorical.__init__)
    def __init__(self, *args, **kwargs):
        Distribution.__init__(self, *args, **kwargs)

    # pylint:disable=invalid-overridden-method
    @constraints.DependentProperty
    def support(self):
        return constraints.IntegerInterval(0, self._num_events - 1)


class Pareto(Distribution, distributions.Pareto):

    #  pylint:disable=missing-docstring,super-init-not-called
    __doc__ = distributions.Pareto.__doc__.replace(">>>", ">>")

    arg_constraints = {"alpha": constraints.positive, "scale": constraints.positive}

    @wraps(distributions.Pareto.__init__)
    def __init__(self, *args, **kwargs):
        Distribution.__init__(self, *args, **kwargs)

    #  pylint:disable=invalid-overridden-method
    @constraints.DependentProperty
    def support(self):
        return constraints.GreaterThan(self.scale)


class Uniform(Distribution, distributions.Uniform):
    # pylint: disable=missing-docstring,super-init-not-called
    __doc__ = distributions.Uniform.__doc__.replace(">>>", ">>")
    arg_constraints = {"low": constraints.dependent, "high": constraints.dependent}

    @wraps(distributions.Uniform.__init__)
    def __init__(self, *args, **kwargs):
        Distribution.__init__(self, *args, **kwargs)

    #  pylint:disable=invalid-overridden-method
    @constraints.DependentProperty
    def support(self):
        return constraints.Interval(self.low, self.high)


class Multinomial(Distribution, distributions.Multinomial):
    # pylint: disable=missing-docstring,super-init-not-called
    __doc__ = distributions.Multinomial.__doc__.replace(">>>", ">>")

    @wraps(distributions.Multinomial.__init__)
    def __init__(self, *args, **kwargs):
        Distribution.__init__(self, *args, **kwargs)

    #  pylint:disable=invalid-overridden-method
    @constraints.DependentProperty
    def support(self):
        return constraints.IntegerInterval(0, self.total_count)


class Binomial(Distribution, distributions.Binomial):
    # pylint: disable=missing-docstring,super-init-not-called
    __doc__ = distributions.Binomial.__doc__.replace(">>>", ">>")
    arg_constraints = {
        "total_count": constraints.nonnegative_integer,
        "probs": constraints.unit_interval,
        "logits": constraints.real,
    }

    @wraps(distributions.Binomial.__init__)
    def __init__(self, *args, **kwargs):
        Distribution.__init__(self, *args, **kwargs)

    #  pylint:disable=invalid-overridden-method
    @constraints.DependentProperty
    def support(self):
        return constraints.IntegerInterval(0, self.total_count)

# pylint: disable=not-callable,no-self-use
"""
Guides
======

Callable classes that create approximating `RandomVariable` objects when
adding `RandomVariable`s to a :class:`~borch.Module`.
"""
from random import randint
from warnings import warn

import torch

import borch
from borch.tensor import RandomVariable
from borch.distributions.distributions import PointMass
from borch.module_base import ModuleBase
from borch.distributions.distribution_utils import (
    dist_to_qdist,
    dist_to_qdist_infer_hierarchy,
    normal_distribution_from_rv,
    delta_distribution_from_rv,
    scaled_normal_dist_from_rv,
)
from borch.utils.inference_conversion import rsample_else_sample
from borch.utils.random_variable_utils import copy_random_variable_properties
from borch.distributions.constraints_registry import transform_to

# pylint: disable=abstract-method


class Guide(ModuleBase):
    """A guide object for the creation, deletion, containment and handling
    of approximating distributions for use in :class:`~borch.Module`s.
    """

    def register_random_variable(self, name, rv):
        r"""Adds a random variable to the module.

        The random variable can be accessed as an attribute using given name.

        Notes:
            This differs from the super in that it first calls
            `_register_random_variable_hook` which is a guide-specific method
            for special manipulation of random variables before they are added.

        Args:
            name (string): name of the parameter. The parameter can be accessed
              from this module using the given name
            rv (RandomVariable, None): random variable to be added to the
              module.
        """
        # There is probably a nice way to do this with class decorators but it
        # may become a bit opaque..
        name, rv = self._register_random_variable_hook(name, rv)
        return super().register_random_variable(name, rv)

    def _register_random_variable_hook(self, name, rv):
        """Use this hook to manipulate `RandomVariable`s or perform any special
        actions before they are added added to the Guide.

        Args:
            name: Name of the random variable.
            rv: A `RandomVariable` object to be registered.

        Returns:
            Tuple of new (name, rv) where all manipulations hasve been made.
        """
        return name, rv

    def __call__(self, name, rv):  # pylint: disable=arguments-differ
        raise NotImplementedError

    def forward(self, *inputs):  # pylint: disable=unused-argument
        """Forward method."""
        msg = "Guide objects do not implement a forward method"
        raise RuntimeError(msg)


class AutomaticGuide(Guide):
    """An automatic guide will automatically add approximating distributions
    based on the `RandomVariable` objects that are used in any call.

    It will use the same type of distribution as the prior and initialize the
    variables in the same point as the prior, but if some of the arguments
    of the prior requires gradients, it will create an parameter for this
    argument.
    """

    def _register_random_variable_hook(self, name, rv):
        """A passed RandomVariable will be cloned and an appropriate
        approximating distribution will be returned in its place, based on
        whether the given `rv` had an approximating distribution or not."""
        if not torch.is_grad_enabled():
            warn(
                """AutomaticGuide can result in different
                    behavior if executed in a `toch.no_grad` context then
                    outiside. All distributions will be created with
                    leaf nodes as arguments"""
            )
        old_dist = rv.q_dist or rv.distribution
        if rv.q_dist:
            q_rv = RandomVariable(rv.q_dist)
        else:
            q_rv = RandomVariable(dist_to_qdist_infer_hierarchy(old_dist))
        q_rv.observe(rv.observed)
        return name, q_rv

    def __call__(self, name, rv):
        if not hasattr(self, name):
            self.register_random_variable(name, rv)
        q_rv = self.get_rv(name)  # approximating distribution
        copy_random_variable_properties(original=rv, new=q_rv)
        rsample_else_sample(q_rv)


class PriorAsGuide(AutomaticGuide):
    """An automatic guide will automatically add approximating distributions
    based on the `RandomVariable` objects that are used in any call.

    It will use the same type of distribution as the prior and initialize the
    variables in the same point as the prior.
    """

    def _register_random_variable_hook(self, name, rv):
        """A passed RandomVariable will be cloned and an appropriate
        approximating distribution will be returned in its place, based on
        whether the given `rv` had an approximating distribution or not."""
        old_dist = rv.q_dist or rv.distribution
        if rv.q_dist:
            q_rv = RandomVariable(rv.q_dist)
        else:
            q_rv = RandomVariable(dist_to_qdist(old_dist))
        q_rv.observe(rv.observed)
        return name, q_rv

    def observe(self, *args, **kwargs):
        """Calls observe on this module (see help on superclass)."""
        warn(
            "Calling observe on this guide can give unintended"
            " consequences if one later unobserves and wants to generate"
            " from the distribution. Consider using AutomaticGuide",
            UserWarning,
            stacklevel=2,
        )
        super().observe(*args, **kwargs)


class NormalGuide(PriorAsGuide):
    r"""An automatic guide which, when given a prior which is a continuous
    distribution, creates an approximating distribution
    :math:`\mathbb{N}(\mu, \sigma^2)`.

    The approximating distribution is initialised at current value of the RV if
    it is finite, otherwise a sample drawn from the prior is used.

    Notes:
        specifying `q_dist` on RandomVariables that gets attached to this guide
        will have no effect.
    """

    def __init__(self, log_scale=-3):
        """
        Args:
            log_scale: Initial value of the log scale for approximating
              distributions.
        """
        super().__init__()
        self._log_scale = log_scale

    def _register_random_variable_hook(self, name, rv):
        new_dist = normal_distribution_from_rv(rv, log_scale=self._log_scale)
        q_rv = RandomVariable(new_dist)
        q_rv.observe(rv.observed)
        return name, q_rv


class ScaledNormalGuide(PriorAsGuide):
    r"""An automatic guide which, when given a prior which is a continuous
    distribution, creates an approximating distribution
    :math:`\mathbb{N}(\mu, \sigma^2)` where :math:\sigma^2 = scale*std(prior)`.

    The approximating distribution is initialised at current value of the RV if
    it is finite, otherwise a sample drawn from the prior is used.

    Notes:
        specifying `q_dist` on RandomVariables that gets attached to this guide
        will have no effect.

    Args:
        scaling: value to mutiply the stddev of the prior with to initlize
           the scale paramater of the q distribution.
    """

    def __init__(self, scaling=0.01):
        super().__init__()
        self._scaling = scaling

    def _register_random_variable_hook(self, name, rv):
        new_dist = scaled_normal_dist_from_rv(rv, scaling=self._scaling)
        q_rv = RandomVariable(new_dist)
        q_rv.observe(rv.observed)
        return name, q_rv


class DeltaGuide(PriorAsGuide):
    r"""An automatic guide which, when given a prior which is a continuous
    distribution, creates an approximating distribution with a Delta distribution.

    The approximating distribution is initialised at current value of the RV if
    it is finite, otherwise a sample drawn from the prior is used.

    Notes:
        specifying `q_dist` on RandomVariables that gets attached to this guide
        will have no effect.
    """

    def _register_random_variable_hook(self, name, rv):
        new_dist = delta_distribution_from_rv(rv)
        q_rv = RandomVariable(new_dist)
        q_rv.observe(rv.observed)
        return name, q_rv

    def __call__(self, name, rv):
        if not hasattr(self, name):
            self.register_random_variable(name, rv)
        q_rv = self.get_rv(name)
        q_rv.observe(rv.observed)
        q_rv.rsample()


class PointMassGuide(Guide):
    """A guide that is used to operate on unconstrained parameter values,
    intended to be used with MCMC.

    Notes:
        There should never be a case where a distribution which is
        not a PointMass can be added to this class (as defined in
        `_register_random_variable_hook`)

        specifying `q_dist` on RandomVariables that gets attached to this guide
        will have no effect.
    """

    def __init__(self):
        super().__init__()
        self._n_samples = 0
        self._sample_index = None

    def _register_random_variable_hook(self, name, rv):
        u_val = transform_to(rv.support).inv(rv.sample()).detach()
        u_val = torch.tensor(u_val, requires_grad=True)
        new = RandomVariable(PointMass(u_val, rv.support))
        return name, new

    def __call__(self, name, rv):
        if not hasattr(self, name):
            self.register_random_variable(name, rv)

        q_rv = self[name]  # approximating distribution
        q_rv.observe(rv.observed)
        if self._sample_index is not None:
            q_rv.distribution.sample(index=self._sample_index)

        return q_rv.clone()  # create a new node in the graph

    def save_state_as_sample(self):
        """Saves the current unconstrained value as a sample, such that it
        can be redrawn in the future when `sample` is called.
        """
        self._n_samples += 1
        for rv in self.random_variables():
            rv.distribution.save_state_as_sample()

    def sample(self):
        """Updates the values of the parameters with the saved samples."""
        if not tuple(self.random_variables()):
            raise RuntimeError(f"No random variables in {self}")
        if self._n_samples == 0:
            raise IndexError("No samples have been stored")
        self._sample_index = randint(0, self._n_samples - 1)  # noqa: S311
        for rv in self.random_variables():
            rv.distribution.index = self._sample_index
            rv.sample()

    def rsample(self):
        """Sets the mode of the guide to do training."""
        self._sample_index = None
        for rv in self.random_variables():
            rv.rsample()


class ManualGuide(Guide):
    """The manual guide must have all `RandomVariable` objects explicitly added
    before they are available for use in a Model.

    Notes:
        specifying `q_dist` on RandomVariables that gets attached to this guide
        will have no effect.

    """

    def __call__(self, name, rv):
        # NB random variables are never added automatically, they are
        # explicitly expected to exist already
        q_rv = self.get_rv(name)
        q_rv.observe(rv.observed)


def set_guides(guide_creator):
    """
    Function that takes any object and if it is a borch.nn.Module
    it sets the guide to `guide_creator()' on that object.


    Args:
        guide_creator (callable): should return a borch.guide.Guide

    Examples:
        >>> from borch import guide, nn, Module
        >>> module = Module(guide=guide.NormalGuide())
        >>> module.lin = nn.Linear(10, 10)
        >>> module.apply(set_guides(guide.AutomaticGuide))
        Module(
          (lin): Linear(in_features=10, out_features=10, bias=True)
        )
        >>> module.guide
        AutomaticGuide()
    """

    def new_guide(module):
        """sets a new guide if a borch.Module"""
        if isinstance(module, borch.Module):
            module.guide = guide_creator()
        else:
            pass

    return new_guide

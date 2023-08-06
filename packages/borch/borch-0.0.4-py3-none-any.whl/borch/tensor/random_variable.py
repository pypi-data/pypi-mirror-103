"""
The ppl primitive RandomVariable is used to model stochastic nodes.

Currently there is no support for `requires_grad=True` on a random variable
(although gradients of the underlying parameters on the distributions are still
supported).

Todo:
  * We need a nice fix for returning distribution arguments that are not
    `TransformedParameter` instances.
    Due to `broadcast_all` being used in some `torch.distributions`, the
    resulting arguments (e.g. loc, scale for Normal) are not leaf nodes which
    causes issues when trying to return parameters from `RandomVariable`.
  * Clean up and remove `TensorBase` and `_RandomVariable`.
"""

import torch

from borch.tensor.tensor_base import TensorBase
from borch.utils.func_tools import replace_none_with_argument


class RandomVariable(TensorBase):
    """Borch RandomVariable primitive.

    A class which inherits form `torch.Tensor` and has access to
    `torch.distribution.Distribution` methods, such as sample, rsample and
    log_prob.

    Example:
        >>> from borch.distributions import distributions
        >>> dist = distributions.Normal(torch.ones(3), torch.ones(3))
        >>> rvar = RandomVariable(dist)
        >>> rvar.sample()
        tensor(...)
        >>> rvar.rsample()
        tensor([..., ..., ...])
        >>> rvar.set_value_(torch.ones(3))
        RandomVariable containing:
        tensor([1., 1., 1.])
        >>> rvar.log_prob()
        tensor([-0.9189, -0.9189, -0.9189])
        >>> rvar.entropy()
        tensor(...)
        >>> # The random variable also acts as a tensor (adopting the value of
        >>> # the latest sample)
        >>> rvar.mean()
        tensor(1.)
    """

    # These are the functions which, when called with value=None, are invoked
    # with `self` for `value`.
    _replace_none_with_self_names = ("log_prob", "cdf", "icdf")

    def __init__(self, distribution, q_dist=None):
        super().__init__()
        self.distribution = distribution
        self.observed = None
        self.q_dist = q_dist
        if self.has_rsample:
            self.rsample()
        else:
            self.sample()

    def named_parameters(self, seen=None, prefix=""):
        """Fetch all parameters from self and yeilds the name and the param

        Yields:
            name, Parameter: yields the name and and tensor
        """
        if seen is None:
            seen = set()

        for name, var in self.distribution.named_parameters():
            if var not in seen:
                seen.add(var)
                if isinstance(var, TensorBase):
                    for _name, _var in var.named_parameters(seen, prefix=name):
                        yield prefix + ("." if prefix else "") + str(_name), _var

                elif isinstance(var, torch.Tensor):
                    yield prefix + ("." if prefix else "") + str(name), var

    def __getattr__(self, item):
        attr = getattr(self.distribution, item)
        if item in self._replace_none_with_self_names:
            attr = replace_none_with_argument(self, attr)
        return attr

    def _do_sample(self, method, shape):
        """Pull a sample from `self.distribution` using the specified method.

        Args:
            method: Method to call on `self.distribution` (sample/rsample)
            shape: sample shape

        Returns:
            The sample drawn from the distribution object.
        """
        if method not in ("sample", "rsample"):
            raise ValueError("method must be one of {sample,rsample}")
        self.recalculate()
        if self.observed is not None:
            return self.set_value_(self.observed)
        sample = getattr(self.distribution, method)(shape)
        self.set_value_(sample)
        return sample

    def sample(self, sample_shape=torch.Size()):
        """Generates a sample_shape shaped sample or sample_shape shaped batch
        of samples if the distribution parameters are batched.
        If the RandomVariable is observed,

        It will obtain the same value as the observed value.

        Args:
          sample_shape: Shape of the new sample to be created.

        Returns:
            A reparameterised sample from the underlying distribution.
        """
        return self._do_sample("sample", sample_shape)

    def rsample(self, sample_shape=torch.Size()):
        """Generates a `sample_shape` shaped reparameterized sample or
        sample_shape shaped batch of reparameterized samples if the
        distribution parameters are batched.

        If the `RandomVariable` is observed, it will obtain the same
        value as the observed value.

        Notes:
            It is recommended to always use the returned value for operations
            if your graph, rather than `self` object. When calling `rsample`
            an inplace operation takes place and gradients cannot be guaranteed
            to propagate correctly. The returned sample however is a unique
            node in the graph and is safe to use in any further operation.

        Args:
          sample_shape: Shape of the new sample to be created.

        Returns:
            A reparameterised sample from the underlying distribution.
        """
        return self._do_sample("rsample", sample_shape)

    def recalculate(self):
        """
        Recalculates all internal values affected by a change to a `.data` in
        one of the arguments

        Returns:
            None
        """
        self.distribution = self.distribution.recalculate()

    def observe(self, val):
        """Set the observed status of the `RandomVariable`.

        If `val` is a tensor then this treats the `RandomVariable` as observed,
        i.e. the value of `self` will be the value `val`, even when calling
        `sample` and `rsample`.

        If `val` is `None`, then observed behaviour is dropped and the the
        `RandomVariable` samples randomly once again.

        Args:
          val: Value of observation (as a `torch.tensor`) or None.
        """
        previously_observed = self.observed is not None
        self.observed = val
        if val is None:
            if previously_observed:
                # draw a new sample when observed is set to None if rv was
                # previously observed
                if self.has_rsample:
                    self.rsample()
                else:
                    self.sample()
        else:
            self.data = val.data  # solves broadcast issue with `copy_`
            self.copy_(val)
        return self


RV = RandomVariable

"""
Module
======

The class from which all torch proxies are created and all sub-classes of
ppl modules should inherit.

`Module` itself can be subclassed to create stochastic neural networks /
modules off the shelf.

Examples:
    >>> import torch
    >>> from borch.distributions import Normal
    >>> from borch.guide import NormalGuide

    >>>
    >>> class MyModule(Module):
    ...     def __init__(self, w_size):
    ...         super().__init__(guide=NormalGuide())
    ...         normal = Normal(torch.ones(w_size), torch.ones(w_size))
    ...         self.weight = RandomVariable(normal)
    ...
    ...     def forward(self, x):
    ...         return x.matmul(self.weight)
    ...
    >>> my_module = MyModule(w_size=(4,))
    >>> # set the values of random variable to be all 0s
    >>> my_module.observe(weight=torch.ones(4))
    >>> my_module(torch.ones((3, 4)))
    tensor([4., 4., 4.], grad_fn=<MvBackward>)
"""
from functools import partial, wraps

from torch.nn import modules

from borch.tensor import RandomVariable
from borch.guide import Guide, AutomaticGuide
from borch.module_base import (
    GUIDE_ATTR,
    ModuleBase,
    named_random_variables,
    named_random_variables_guide,
)
from borch.utils.inference_conversion import pq_dict_to_lists
from borch.utils.module_utils import copy_module_attributes
from borch.utils.inference_conversion import rsample_else_sample


def _add_to_pq_dict(mod, _pq_dict, _seen):
    # pylint: disable=protected-access

    if mod in _seen or not isinstance(mod, Module):
        return

    _seen.add(mod)
    _pq_dict.update({mod._parameters[name]: mod.guide[name] for name in mod._used_rvs})


class _PriorPlaceholder:
    """A placeholder class for direct access to priors via getattr."""

    def __getitem__(self, item):
        return self.__dict__[item]


class ModuleMeta(type):
    """Metaclass for `Module`.

    When `Module.__new__` is called with a pre-instantiated `torch.nn.Module`
    object (passed as the kwarg `existing`), all preexisting attributes are
    copied to the new object before initialisation.
    """

    def __call__(cls, *args, existing=None, **kwargs):
        obj = cls.__new__(cls, *args, **kwargs)

        if isinstance(existing, modules.Module):
            copy_module_attributes(original=existing, new=obj)

            # Initialise only with Module. The corresponding `torch.nn.XXX`
            # initialisations have already been performed (this is for
            # borchification purposes).
            Module.__init__(obj, *args, **kwargs)
        else:
            # Initialise with super. This is a new object creation and all
            # super inits should be called.
            obj.__init__(*args, **kwargs)

        return obj


class Module(ModuleBase, metaclass=ModuleMeta):
    """The ppl Module class is the super class for all PyTorch proxies,
    borchified modules, and can be used as a base class for creating new
    custom modules.

    Todo:
        Mention guides and how they work.
    """

    # pylint: disable=abstract-method,not-callable,protected-access
    __guide_attr = GUIDE_ATTR

    def __init__(self, guide=None):
        super().__init__()
        if guide is None:
            guide = AutomaticGuide()
        self.guide = guide
        self._prior = _PriorPlaceholder()
        self._prior.__dict__ = self._parameters

    @property
    def prior(self):
        """
        Access the Random Variables corresponding  to the prior
        """
        return self._prior

    def _has_guide(self):
        return self.__dict__.get(self.__guide_attr) is not None

    def _apply(self, fn):
        if self._has_guide():
            self.guide._apply(fn)
        super()._apply(fn)

    def apply(self, fn):
        """Apply a function to self and all submodules. See the PyTorch
        documentation for more details.

        Args:
            fn: Function to apply to each module and submodule.

        Returns:
            self.
        """
        if self._has_guide():
            fn(self.guide)
        super().apply(fn)
        return self

    def named_random_variables_guide(self, prefix="", recurse=True):
        """Retrieve all random variables and their names from guides in self and all
        children. NB we *cannot* use `.parameters` here since that, by design,
        only returns leaf parameters.

        Args:
            prefix (str): prefix to prepend to all parameter names.
            recurse (bool): if True, then yields parameters of this module
                and all submodules. Otherwise, yields only parameters that
                are direct members of this module.

        Yields:
            (string, rv): Tuple containing the name and rv
        """
        gen = self._named_members(
            named_random_variables_guide, prefix=prefix, recurse=recurse
        )
        for elem in gen:
            yield elem

    def named_random_variables_prior(self, prefix="", recurse=True):
        """Retrieve all random variables and their names from the prior in self and all
        children. NB we *cannot* use `.parameters` here since that, by design,
        only returns leaf parameters.
        Args:
            prefix (str): prefix to prepend to all parameter names.
            recurse (bool): if True, then yields parameters of this module
                and all submodules. Otherwise, yields only parameters that
                are direct members of this module.

        Yields:
            (string, rv): Tuple containing the name and rv
        """
        gen = self._named_members(
            named_random_variables, prefix=prefix, recurse=recurse
        )
        for elem in gen:
            yield elem

    def _re_add_parameters(self):
        """Re-adds all parameters to the `Module`.

        This is required when setting a new guide on `self` so that all
        `RandomVariable` objects on `self` get exposed to the new guide."""
        for name in tuple(self._parameters.keys()):
            setattr(self, name, self._parameters.pop(name))

    @wraps(ModuleBase.state_dict)
    def state_dict(self, destination=None, prefix="", keep_vars=True):
        # Specifically add the guide (it does not appear in _modules)
        guide_prefix = prefix + self.__guide_attr
        destination = self.guide.state_dict(
            destination, guide_prefix + ".", keep_vars=keep_vars
        )

        return super().state_dict(destination, prefix, keep_vars)

    def _load_from_state_dict(
        self,
        state_dict,
        prefix,
        local_metadata,
        strict,
        missing_keys,
        unexpected_keys,
        error_msgs,
    ):
        """See `torch.nn.Module._load_from_state_dict` for the original
        documentation.

        Notes:
            The primary difference for this implementation is that we first
            load all guide random variables and set those on the current guide.
        """
        # pylint: disable=too-many-arguments

        # First we collect all guide random variables and set those
        guide_prefix = prefix + self.__guide_attr
        for key in tuple(state_dict.keys()):
            if key.startswith(guide_prefix):
                name = key[len(guide_prefix) + 1 :]
                self.guide._parameters[name] = state_dict.pop(key)

        # Then we load the remaining state dist as usual
        super()._load_from_state_dict(
            state_dict,
            prefix,
            local_metadata,
            strict,
            missing_keys,
            unexpected_keys,
            error_msgs,
        )

    def register_random_variable(self, name, rv):
        r"""Adds a random variable to the module.

        The random variable can be accessed as an attribute using given name.

        Args:
            name (string): name of the parameter. The parameter can be accessed
              from this module using the given name
            rv (RandomVariable, None): random variable to be added to
              the module.
        """
        if "_parameters" not in self.__dict__:
            raise AttributeError(
                "Cannot assign random variable before"
                f" {type(self).__name__}.__init__() call"
            )
        if hasattr(self, name) and (
            name not in self._parameters and name not in self.guide._parameters
        ):
            # NB if the guide has the parameter then we're still ok to add it
            raise KeyError("Attribute '{}' already exists".format(name))
        if "." in name:
            raise KeyError('Random variable name can\'t contain "."')
        if name == "":
            raise KeyError('Random variable name can\'t be empty string ""')
        if not isinstance(rv, RandomVariable):
            raise TypeError(
                "Cannot assign '{}' object to random_variable"
                " '{}' (RandomVariable required)".format(type(rv).__name__, name)
            )

        if name in self._observed:
            rv.observe(self._observed[name])
        self._parameters[name] = rv
        self.guide(name, rv)

    def __getattr__(self, item):
        if self._has_guide():
            guide_attr = getattr(self.guide, item, None)
            if guide_attr is not None:
                self._used_rvs.add(item)
                return guide_attr
        return super().__getattr__(item)

    def __setattr__(self, name, value):
        if name == "guide":
            # `__setattr__` comes before data-descriptors in the lookup order.
            # So, when setting guide, we shortcut this to access the property
            # set method directly.
            return type(self).guide.__set__(self, value)
        return super().__setattr__(name, value)

    def observe(self, *args, **kwargs):
        """Calls observe on this module (see help on superclass) as well as
        the guide set to this module."""
        self.guide.observe(*args, **kwargs)
        super().observe(*args, **kwargs)

    @property
    def guide(self):
        """The guide currently associated with this Module."""
        if not self._has_guide():
            # cannot use attribute error without deferring to the error raised
            # by `object.__getattr__`
            raise RuntimeError(f"No guide set on {self}")
        return self._guide

    @guide.setter
    def guide(self, value):
        if not isinstance(value, (Guide, type(None))):
            raise ValueError(
                f"Cannot set a {type(value).__name__} object"
                f" as a guide on {str(self)}"
            )
        self.__dict__[self.__guide_attr] = value
        self._re_add_parameters()

    def pq_dict(self) -> dict:
        """Create a dictionary where keys, values are prior distributions,
        approximating distributions, respectively.

        Returns:
            A dictionary of the format {p: q} for all random variables.
        """
        pq_dict = {}
        fn = partial(_add_to_pq_dict, _pq_dict=pq_dict, _seen=set())
        self.apply(fn)
        return pq_dict

    def pq_to_infer(self):
        """
        Creats a dictionary of lists that can be used in borch.infer
        Returns:
            dictionary with keys corresponding to arguments in
            infer.vi functions

        """
        return pq_dict_to_lists(self.pq_dict())

    def remove_random_variables(self, exclude: set = None):
        """Remove all `RandomVariable` objects on self.

        Note that for `Module` instances, random variables are not removed
        from guides.

        Args:
            exclude: instances of modules to exclude from removal of random
              variables.
        """
        if exclude is None:
            exclude = set()

        exclude.add(self.guide)
        super().remove_random_variables(exclude)

    def sample(self):
        """Draw a new sample for all random variables on `self` and on
        submodules.
        """

        def _sample_rvs(module):
            if isinstance(module, Module) and module._has_guide():
                for param in module._parameters.values():
                    if isinstance(param, RandomVariable):
                        param.recalculate()
                for param in module.guide._parameters.values():
                    if isinstance(param, RandomVariable):
                        rsample_else_sample(param)

        self.apply(_sample_rvs)
        self._reset_used_rvs()

"""
Module Base Class
=================

The `ModuleBase` class is the super class for all `Module`-like which will
contain `RandomVariable` objects. Including: `Module`, PyTorch proxy modules,
`Guide` classes and subclasses.
"""
from functools import wraps
from itertools import chain

from torch import Tensor
from torch.nn import Parameter, modules
from torch.nn.modules.module import _IncompatibleKeys

from borch.tensor import RandomVariable
from borch.tensor.tensor_base import TensorBase
from borch.utils.inference_conversion import rsample_else_sample
from borch.utils import yield_opt_param

GUIDE_ATTR = "_guide"


def _remove_from_dicts(name, *dicts):
    """Remove entries from multiple dictionaries.

    Args:
        name: Name of the entry to remove.
        *dicts: Any number of dicts or dict-like objects.
    """
    for _d in dicts:
        if name in _d:
            del _d[name]


class ModuleBase(modules.Module):
    """The Borch counterpart to `torch.nn.Module`.

    Notes:
        We borrow a lot from the functionality of Module in its treatment of
        Parameters, including reusing the '_parameters' OrderedDict to store
        all random variables in.

        The abstract method `forward` is not implemented here. We want the
        delegation to call the sibling (torch) class in `borch.nn` (see python
        MRO).

        Divergence is not calculated directly on a `ModuleBase` subclass. The
        suggested practise is to use `ModuleBase.random_variables()` to fetch
        all `RandomVariable`s, and then use these as desired.

    Todo:
      * We might run into issues with load/save state dict. There are type
        checks on all parameters and we should possibly consider making
        RandomVariable inherit from Parameter to account for this (it would
        also reduce a lot of repeated code in this class). ALTHOUGH, loading
        and saving random variables will likely require special treatment
        anyway.
      * Look at cuda/cpu and apply in general
      * Override `reset_parameters` to also reset random variables (we want to
        maintain `reset_parameters` since there may be parameters that are not
        random variables)
    """

    # pylint: disable=abstract-method,protected-access

    # PyTorch have implemented this as a mypy workaround... it's not used
    # and Pylint complains at it.
    _forward_unimplemented = None

    def __init__(self):
        if not hasattr(self, "_parameters"):
            # Only initialise if not a pre-initialised module.
            modules.Module.__init__(self)  # Need explicit reference to super

        self._sampling = False
        self._observed = {}
        self._used_rvs = set()

    def register_random_variable(self, name, rv):
        r"""Adds a random variable to the module.

        The random variable can be accessed as an attribute using given name.

        Args:
            name (string): name of the parameter. The parameter can be accessed
              from this module using the given name
            rv (RandomVariable, None): random variable to be added to
              the module.
        """
        # todo: a lot of common code with _parameters here...
        if "_parameters" not in self.__dict__:
            raise AttributeError(
                "Cannot assign random variable before"
                f" {type(self).__name__}.__init__() call"
            )
        if hasattr(self, name) and name not in self._parameters:
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
        # NB `Module.register_parameter` would check if `rv` has an
        # attr `grad_fn` here (to check if it's a non-leaf node). For random
        # variables we skip this step since we can expect `rv` be a
        # non-leaf node, and that it itself may contain nested parameters.
        if name in self._observed:
            rv.observe(self._observed[name])
        self._parameters[name] = rv

    def get_rv(self, name):
        """
        Gets a RandomVarieble from the module, it differs from __getattr__
        in that __getattr__ fetches values from a guide such is present.
        While get_rv get what was attached to the module.

        Args:
            name (string): the name of a RandomVariable

        Returns:
            a RandomVariable
        """

        if name in self._parameters:
            par = self._parameters[name]
            if isinstance(par, RandomVariable):
                return par
        raise AttributeError(f"{self} has no RandomVariable '{name}'")

    def sample(self):
        """Draw a new sample for all random variables on `self` and on
        submodules.
        """

        def _sample_rvs(module):
            if isinstance(module, ModuleBase):
                for param in module._parameters.values():
                    if isinstance(param, RandomVariable):
                        rsample_else_sample(param)

        self.apply(_sample_rvs)
        self._reset_used_rvs()

    def _reset_used_rvs(self):
        """
        Resets the used random variabels
        """
        self.apply(_clear_used_rvs)

    @wraps(modules.Module.state_dict)
    def state_dict(self, destination=None, prefix="", keep_vars=True):
        # Only changing the default value for `keep_vars`. We want this to be
        # `True` so that random variable objects are correctly serialised.
        return super().state_dict(destination, prefix, keep_vars)

    def _load_from_state_dict(  # noqa: C901
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
            This function is identical to the PyTorch function with the
            exception that we use `setattr` to attach any unknown attributes
            to `self` and directly add and relevant RandomVariable objects to
            `self._parameters`. The motivation for this is that these may be
            dynamically objects created outside the `__init__` of the respective
            class that we are loading to.
        """
        # pylint: disable=too-many-arguments,too-many-locals,too-many-branches
        for hook in self._load_state_dict_pre_hooks.values():  # pragma: no cover
            hook(
                state_dict,
                prefix,
                local_metadata,
                strict,
                missing_keys,
                unexpected_keys,
                error_msgs,
            )

        local_params = chain(self._parameters.items(), self._buffers.items())
        local_state = {k: v.data for k, v in local_params if v is not None}

        for name, param in local_state.items():
            key = prefix + name
            if key in state_dict:
                input_param = state_dict[key]
                if isinstance(input_param, Parameter):
                    # backwards compatibility for serialized parameters
                    input_param = input_param.data  # pragma: no cover
                try:
                    param.copy_(input_param)
                except Exception:  # pylint: disable=broad-except
                    error_msgs.append(
                        'While copying the parameter named "{}", '
                        "whose dimensions in the model are {} and "
                        "whose dimensions in the checkpoint are {}.".format(
                            key, param.size(), input_param.size()
                        )
                    )
            elif strict:
                missing_keys.append(key)

        for key, input_param in state_dict.items():
            if key.startswith(prefix):
                name = key[len(prefix) :].split(".", 1)[0]
                if name not in chain(self._modules, local_state):
                    if strict:
                        unexpected_keys.append(key)
                    elif isinstance(input_param, RandomVariable):
                        # Sneak the RV directly into _parameters to avoid
                        # any setattr magic
                        self._parameters[name] = input_param
                    else:
                        # `input_param` was a dynamically created attr, we can
                        # try to the set the unexpected entry directly on self.
                        setattr(self, name, input_param)

        if strict:
            for key in state_dict:
                if key.startswith(prefix):
                    input_name = key[len(prefix) :]
                    input_name = input_name.split(".", 1)[
                        0
                    ]  # get the name of param/buffer/child
                    if (
                        input_name not in self._modules
                        and input_name not in local_state
                    ):
                        unexpected_keys.append(key)

    def load_state_dict(self, state_dict, strict=False):
        r"""Copies parameters and buffers from :attr:`state_dict` into
        this module and its descendants. If :attr:`strict` is ``True``, then
        the keys of :attr:`state_dict` must exactly match the keys returned
        by this module's :meth:`~torch.nn.Module.state_dict` function.

        Arguments:
            state_dict (dict): a dict containing parameters and
                persistent buffers.
            strict (bool, optional): whether to strictly enforce that the keys
                in :attr:`state_dict` match the keys returned by this module's
                :meth:`~torch.nn.Module.state_dict` function. Default: ``True``

        Returns:
            ``NamedTuple`` with ``missing_keys`` and ``unexpected_keys`` fields:
                * **missing_keys** is a list of str containing the missing keys
                * **unexpected_keys** is a list of str containing the unexpected keys
        """
        # this is a direct copy from torch, thus no linting
        # pylint: disable=all
        missing_keys = []
        unexpected_keys = []
        error_msgs = []

        # copy state_dict so _load_from_state_dict can modify it
        metadata = getattr(state_dict, "_metadata", None)
        state_dict = state_dict.copy()
        if metadata is not None:
            state_dict._metadata = metadata

        def load(module, prefix=""):
            local_metadata = {} if metadata is None else metadata.get(prefix[:-1], {})
            module._load_from_state_dict(
                state_dict,
                prefix,
                local_metadata,
                strict,
                missing_keys,
                unexpected_keys,
                error_msgs,
            )
            for name, child in module._modules.items():
                if child is not None:
                    load(child, prefix + name + ".")

        load(self)
        load = None  # break load->load reference cycle

        if strict:
            if len(unexpected_keys) > 0:
                error_msgs.insert(
                    0,
                    "Unexpected key(s) in state_dict: {}. ".format(
                        ", ".join('"{}"'.format(k) for k in unexpected_keys)
                    ),
                )
            if len(missing_keys) > 0:
                error_msgs.insert(
                    0,
                    "Missing key(s) in state_dict: {}. ".format(
                        ", ".join('"{}"'.format(k) for k in missing_keys)
                    ),
                )

        if len(error_msgs) > 0:
            raise RuntimeError(
                "Error(s) in loading state_dict for {}:\n\t{}".format(
                    self.__class__.__name__, "\n\t".join(error_msgs)
                )
            )
        return _IncompatibleKeys(missing_keys, unexpected_keys)

    def random_variables(self, recurse=True):
        """The same as `named_random_variables` but only `RandomVariable`
        objects (no names).

        Args:
            recurse (bool): if True, then yields parameters of this module
                and all submodules. Otherwise, yields only randomVariabels that
                are direct members of this module.

        Yields:
            RandomVariable: module random variable
        """
        for _, param in self.named_random_variables(recurse=recurse):
            yield param

    def named_random_variables(self, prefix="", recurse=True):
        """Retrieve all random variables and their names from self and all
        children. NB we *cannot* use `.parameters` here since that, by design,
        only returns leaf parameters.

        Args:
            prefix (str): prefix to prepend to all parameter names.
            recurse (bool): if True, then yields parameters of this module
                and all submodules. Otherwise, yields only parameters that
                are direct members of this module.

        Yields:
            (string, RandomVariable): Tuple containing the name and parameter
        """

        gen = self._named_members(
            lambda module: yield_for_guide_and_module(module, named_random_variables),
            prefix=prefix,
            recurse=recurse,
        )
        for elem in gen:
            yield elem

    def named_parameters(self, prefix="", recurse=True):
        """Returns an iterator over module parameters, yielding both the
        name of the parameter as well as the parameter itself.

        Args:
            prefix (str): prefix to prepend to all parameter names.
            recurse (bool): if True, then yields parameters of this module
                and all submodules. Otherwise, yields only parameters that
                are direct members of this module.

        Yields:
            (string, Parameter): Tuple containing the name and parameter

        """

        gen = self._named_members(
            lambda module: yield_for_guide_and_module(module, named_parameters),
            prefix=prefix,
            recurse=recurse,
        )
        for elem in gen:
            yield elem

    def opt_parameters(self):
        """Retrieve all tensors that requires gradient and is  leaf node
        Args:
            memo (set): parameters already seen.

        Yields:
            A tensor
        """
        for par in yield_opt_param(self.parameters()):
            yield par

    def __getattr__(self, name):
        """
        Notes:
            If `name` is associated with a `RandomVariable` object, it is
            sampled/rsample/observed accordingly but **the returned value is a
            new node in the graph!** It is not the `RandomVariable` itself.
        """
        param = self.__dict__.get("_parameters", {}).get(name)
        if isinstance(param, RandomVariable):
            if self._observed.get(name) is not None:
                param.observe(self._observed.get(name))
            if self._sampling:
                rsample_else_sample(param)
            self._used_rvs.add(name)
            return param.clone()  # new node in the graph
        return super().__getattr__(name)

    def __setattr__(self, name, value):
        if isinstance(value, RandomVariable):
            if "_parameters" not in self.__dict__:
                # NB we're adding to _parameters
                msg = (
                    f"Cannot assign random variables before"
                    f" {type(self).__name__}.__init__() call"
                )
                raise AttributeError(msg)
            _remove_from_dicts(name, self.__dict__, self._buffers, self._modules)
            self.register_random_variable(name, value)
            self._used_rvs.add(name)
        else:
            super().__setattr__(name, value)

    def __getitem__(self, item):
        if item in self._parameters:
            return self.__getattr__(item)
        raise AttributeError(f"{self} has no parameter '{item}'")

    def __setitem__(self, key, value):
        if not isinstance(value, (Parameter, RandomVariable)):
            raise ValueError(
                f"Cannot set object of type '{type(value).__name__}'"
                f" using subscripts on {type(self).__name__}"
            )
        setattr(self, key, value)

    def _apply(self, fn):
        for module in self.children():
            module._apply(fn)

        for param in self._parameters.values():
            if isinstance(param, TensorBase):
                param._apply(fn)
            elif param is not None:
                param.data = fn(param.data)
                if param._grad is not None:
                    param._grad.data = fn(param._grad.data)

        for key, buf in self._buffers.items():
            if buf is not None:
                self._buffers[key] = fn(buf)

        return self

    def sampling(self, value) -> None:
        """Set `_sampling` attribute to `value` on self and all children of
        `self` (using `Module.apply`).

        Args:
            value: Whether sampling should be performed when attributes are
              accessed.

        Todo:
            * Make this a context manager.
        """

        def _f(module):
            if isinstance(module, ModuleBase):
                module._sampling = value

        self.apply(_f)

    def _empty_observed(self):
        """Empty the `observed` dictionary (NB we want to retain the same
        dict object)."""
        for k in tuple(self._observed.keys()):
            del self._observed[k]

    def observe(self, *args, **kwargs):
        """Set/revert any random variables on the current guide to be observed
        /latent.

        The behaviour of an observed variable means that any `RandomVariable`
        objects assigned will be observed at the stated value (if the name
        matches a previously observed variable).

        Note:
            Calling `observe' will overwrite all `observe()` calls made to ANY
            random variable attached to the module, even if it has a differnt name.
            One can still call `observe` on RV`s in the forward after the
            `observe` call is made on the module.
        Args:
            args: If `None`, all observed behaviour will be forgotten.
            kwargs: Any named arguments will be set to observed given that the
              value is a tensor, or the observed behaviour will be forgotten if
              set to `None`.

        Examples:
            >>> import torch
            >>> from borch.distributions import Normal
            >>> from borch.guide import AutomaticGuide
            >>>
            >>> model = ModuleBase()
            >>> rv = RandomVariable(Normal(Tensor([1.]), Tensor([1.])))
            >>> model.observe(rv_one=Tensor([100.]))
            >>> model.rv_one = rv  # rv_one has been observed
            >>> model.rv_one
            RandomVariable containing:
            tensor([100.])
            >>> model.observe(None)  # stop observing rv_one, the value is no
            >>>                      # longer at 100.
            >>> model.sample()
            >>> torch.equal(model.rv_one, Tensor([100.]))
            False
        """
        if args or not kwargs:
            if len(args) != 1 or args[0] is not None:
                msg = "Invalid arguments: only None or kwargs allowed"
                raise ValueError(msg)
            self._empty_observed()

        not_tensor_or_none = [
            k for k, v in kwargs.items() if not isinstance(v, (Tensor, type(None)))
        ]
        if not_tensor_or_none:
            msg = (
                f"Received named arguments which are not one of"
                f" (None, torch.Tensor): {', '.join(not_tensor_or_none)}"
            )
            raise TypeError(msg)
        self._unobserve_rvs()
        # update dictionary and remove None elements
        self._observed.update(kwargs)
        for k, v in tuple(self._observed.items()):
            if v is None:
                del self._observed[k]

    def _unobserve_rvs(self):
        for rv in self.random_variables(recurse=False):
            # setting `observe` on the module to none does not call `observe(None)`
            # on the RV it self to save compute time as it would result in sampleing
            # the dist twice, first when unobserve and then when getattr
            # so we just modify the `observed` filed on the RV
            rv.observed = None

    def remove_random_variables(self, exclude: set = None):
        """Remove all `RandomVariable` objects on self.

        Args:
            exclude: instances of modules to exclude from removal of random
              variables.
        """
        if exclude is None:
            exclude = set()

        if self not in exclude:
            for name, param in tuple(self._parameters.items()):
                if isinstance(param, RandomVariable):
                    self._parameters.pop(name)

        for mod in self.children():
            mod.remove_random_variables(exclude)


def _clear_used_rvs(slf):
    # pylint: disable=protected-access
    if isinstance(slf, ModuleBase):
        slf._used_rvs.clear()


def has_guide(module):
    """
    Check if a module has a guide

    Args:
        module (borch.nn.ModuleBase): the module

    Returns:
        Bool

    """
    return module.__dict__.get(GUIDE_ATTR) is not None


def named_parameters(module):
    """
    Create generator that yields all the name's and param's for the module

    Args:
        module (borch.nn.ModuleBase): the module

    Yields:
        generator that yields: name, parm
    """
    # pylint: disable=protected-access
    for name, param in module._parameters.items():
        if isinstance(param, TensorBase):
            for _name, _param in param.named_parameters(prefix=name):
                yield _name, _param
        else:
            yield name, param


def named_random_variables(module):
    """
    Retrieve all random variables and their names from the module
    Args:
        module (borch.nn.ModuleBase): the module

    Yields:
        generator that yields: name, parm

    """
    # pylint: disable=protected-access
    for name, param in module._parameters.items():
        if isinstance(param, RandomVariable):
            yield name, param


def yield_for_guide_and_module(module, fn):
    """
    applies a yield function to the module and module.guide if it excists
    Args:
        module (borch.nn.ModuleBase): the module
        fn (callable): callable that yeilds stuff

    Yields:
        yields according to the fn
    """
    for mod in [module, module.guide] if has_guide(module) else [module]:
        for obj in fn(mod):
            yield obj


def named_random_variables_guide(module):
    """
    Retrieve all random variables and their names from the module.guide
    Args:
        module (borch.nn.ModuleBase): the module

    Yields:
        generator that yields: name, parm

    """
    if has_guide(module):
        for name, param in named_random_variables(module.guide):
            yield name, param

"""
Functions to 'borchify' PyTorch modules/networks.
"""
from typing import Optional

from torch.nn import Module

from borch import nn, Module as BorchModule
from borch.guide import Guide, NormalGuide
from borch.rv_factories import apply_rv_factory
from borch.nn.torch_proxies import get_rv_factory


def borchify_module(
    module: Module, rv_factory: Optional[callable] = None, guide: Guide = None
) -> BorchModule:
    """Take a `Module` instance and return a corresponding Borch
    equivalent.

    Args:
        module: The `Module` object to be 'borchified'.
        rv_factory: A callable which, when passed a `Parameter`, returns a
          `RandomVariable`, if None the default of `borch.nn.torch_proxies`
           will be used.
        guide: A guide for which the borchified module should use. The default
          is `NormalGuide` (see `borch.guide`).

    Returns:
        A new module of type `borch.Module`.

    Examples:
        >>> import torch
        >>> linear = torch.nn.Linear(3, 3)  # create a linear module
        >>> blinear = borchify_module(linear)
        >>> type(blinear)
        <class 'borch.nn.torch_proxies.Linear'>
    """
    # Unexpected keyword arg is consumed by the metaclass
    # pylint: disable=unexpected-keyword-arg
    cls_name = type(module).__name__

    if guide is None:
        guide = NormalGuide()

    if cls_name not in dir(nn):
        # If a custom class which inherits from torch.nn.Module was created
        # then it does not exist in borch.nn (obviously). In this case we can
        # simply construct from Module. NB we also still apply the `rv_factory`
        # to all parameters.
        new = BorchModule(guide=guide, existing=module)
    else:
        new_module = getattr(nn, cls_name)
        if issubclass(new_module, BorchModule):
            new = new_module(guide=guide, existing=module)
        else:  # pragma: no cover
            # TODO: it is not sufficient to only check the string to only check for
            # name above 'if cls_name not in dir(nn):' We should check if the actual
            # class is available in nn - see issue 295
            new = new_module()
    temp_rv_factory = get_rv_factory(cls_name) if rv_factory is None else rv_factory
    return apply_rv_factory(new, temp_rv_factory)


def borchify_network(
    module: Module,
    rv_factory: Optional[callable] = None,
    guide_creator: callable = NormalGuide,
    cache: dict = None,
) -> BorchModule:
    """Borchify a whole network. This applies `borchify_module` recursively on
    all modules within a network.

    Args:
        module: The network to be borchified.
        rv_factory: A callable which, when passed a `Parameter`, returns a
          `RandomVariable`, if None the default of `borch.nn.torch_proxies`
           will be used.
        guide_creator: A callable which creates a guide. This will be used to
          create a new guide for each module in the network.
        cache: Cache is mapping from id(torch module) -> ppl module. Used to
          prevent double usage/recursion of borchification (NB recursive
          `Module`s are actually not supported by PyTorch).

    Todo:
      * Specify which modules should be borchified.
      * Specify what random variable factories should be used where.

    Notes:
        Double use and recursion are respected. For example if a nested module
        appears in multiple locations in the original network, then the
        borchified version also uses the same borchified module in these
        locations.

    Returns:
        A new borchified network.

    Examples:
      >>> import torch
      >>>
      >>> class Net(Module):
      ...     def __init__(self):
      ...         super(Net, self).__init__()
      ...         self.linear = torch.nn.Linear(3,3)
      ...         # add a nested module
      ...         self.linear.add_module("nested", torch.nn.Linear(3,3))
      ...         self.sigmoid = torch.nn.Sigmoid()
      ...         self.linear2 = torch.nn.Linear(3,3)
      ...
      >>> net = Net()
      >>> bnet = borchify_network(net)
      >>> type(bnet)
      <class 'borch.module.Module'>
      >>> type(bnet.linear)
      <class 'borch.nn.torch_proxies.Linear'>
    """
    # pylint: disable=protected-access
    if cache is None:
        cache = {}

    _id = id(module)
    if _id in cache:
        # it is implicit that all submodules already exist
        return cache[_id]

    new = borchify_module(module, rv_factory, guide_creator())
    cache[_id] = new

    for name, mod in module._modules.items():
        # NB we recurse into `mod` if it does not appear in `cache`
        adding = cache.get(
            id(mod), borchify_network(mod, rv_factory, guide_creator, cache)
        )
        new.add_module(name, adding)

    return new

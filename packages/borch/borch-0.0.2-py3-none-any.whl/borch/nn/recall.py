"""
Expose a module which recalls the latest outputs from given modules.
"""
from functools import partial
from typing import Any, Callable, Tuple

from torch import nn


def _storer(index, storage, _module, _input, output):
    storage[index] = output


def _register_hooks(modules, storage):
    return [
        mod.register_forward_hook(partial(_storer, mod, storage)) for mod in modules
    ]


def _remove_hooks(handlers):
    while handlers:
        handlers.pop().remove()


def _collect(modules, storage):
    return tuple(storage[mod] for mod in modules)


class Recall(nn.Module):
    """Recall the latest outputs from the given modules.

    Args:
        modules: ``nn.Module`` objects to recall the outputs of during this
          object's forward pass.
        agg_fn: A function used to aggregate the outputs from the supplied
          ``nn.Module`` objects. NB the input is always a single tuple
          containing the inputs into the forward, followed by the outputs
          from the latest forwards from ``modules``.

    Example:
        >>>
        # In this example we construct a simple network where the last module
        # receives input from both a module we construct first (``linear``)
        # and the previous module. The aggregation simply returns its input
        # (which will be a tuple).
        >>> import torch
        >>> linear = nn.Linear(3, 4)
        >>> net = nn.Sequential(
        ...     nn.Sequential(nn.Linear(2, 3), linear),
        ...     nn.Sequential(nn.Linear(4, 5), Recall(linear, agg_fn=lambda x: x)),
        ... )
        >>> output = net(torch.ones(10, 2))
        >>> assert isinstance(output, tuple)
        >>>
        >>> # We can also use `get_nested_modules` to retrieve outputs from a
        >>> # instanciated network:
        >>> from borch.utils.module_utils import get_nested_modules
        >>> modules = get_nested_modules(net, [("0", "0"), ("1", "0")])
        >>> recall = Recall(*modules, agg_fn=lambda x: x)
        >>> _ = net(torch.ones(10, 2))
        >>> outputs = recall()
        >>> out1 = outputs[0]
        >>> out2 = outputs[1]
    """

    # pylint: disable=abstract-method

    def __init__(self, *modules: nn.Module, agg_fn: Callable[[Tuple[Any]], Any]):
        super().__init__()
        self._agg_fn = agg_fn
        self._storage = {}
        self._collect_from = modules
        self._handlers = _register_hooks(self._collect_from, self._storage)

    def forward(self, *x):
        """Forward method."""
        return self._agg_fn(x + _collect(self._collect_from, self._storage))

    def __del__(self):
        _remove_hooks(self._handlers)

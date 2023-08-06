"""
Modules for composition such as Sequential, Select and Concurrent. The modules have
no functionality per se, but they dictate how their children should be executed.
"""


from borch.module import Module
from borch import nn
from borch.nn import torch_proxies


class Concurrent(Module):
    """
    Module for splitting input x to different modules and return a tuple of
    the results

    Args:
        branches: The to feed the input through

    Examples:
        >>> import torch
        >>> split = Concurrent(nn.Identity(), nn.Identity())
        >>> x = torch.ones(2)
        >>> split(x)
        (tensor([1., 1.]), tensor([1., 1.]))
    """

    def __init__(self, *branches):
        super().__init__()
        self.branches = nn.ModuleList(branches)

    def forward(self, x):  # pylint: disable=arguments-differ
        """Forward method."""
        return tuple(branch(x) for branch in self.branches)


def apply_sequentially(x, modules):
    """
    Applies an iterable of modules sequentially to an input x.

    Example:
        >>> import torch
        >>> from borch import nn
        >>> test_img = torch.randn(1, 3, 20, 20)
        >>> m1 = nn.Conv2d(3, 5, 3)
        >>> m2 = nn.Conv2d(5, 9, 3)
        >>> m3 = nn.Conv2d(9, 3, 3)
        >>> modules = [m1, m2, m3]
        >>> out1 = apply_sequentially(test_img, modules)
        >>> out2 = m1(test_img)
        >>> out2 = m2(out2)
        >>> out2 = m3(out2)

        out1 and out2 has the same value whether we apply modules manually or use
        apply_sequentially
        >>> assert(torch.all(torch.eq(out1, out2)))
    """
    for mod in modules:
        if isinstance(x, (tuple, list)):
            x = mod(*x)
        else:
            x = mod(x)
    return x


class Sequential(torch_proxies.Sequential):
    # pylint: disable=arguments-differ, missing-docstring
    __doc__ = (
        torch_proxies.Sequential.__doc__
        + """
        Notes:
            **NOTE THAT ANYTHING WHICH INHERITS FROM SEQUENTIAL SHOULD NOT IMPLEMENT
            CUSTOM LOGIC IN THE FORWARD PASS.** The forward pass of a ``Sequential``
            will by design execute modules in the order they were added.

            Also, note that any input to a module which is a list or tuple will be
            expanded in the Sequential forward pass.
        """
    )

    def __getitem__(self, item):
        modules = list(self._modules.values())
        if isinstance(item, slice):
            return Sequential(*modules[item])
        return modules[item]

    def forward(self, *x):
        """Forward method."""
        return apply_sequentially(x, self.children())


class Select(Module):
    """
    Selects a list of indices in an input tuple and passes them forward in a tuple,
    discarding the rest.

    Args:
        idxs: Indices to select from tuple. If the indices of the list itself is a list
          for example [1, [3, 0]] we will select indexable_structure[1] and
          indexable_structure[3][0].

    Examples
        >>> import torch
        >>> select = Select(0)
        >>> x = (torch.ones(2), torch.ones(2))
        >>> select(x)
        (tensor([1., 1.]),)

        We can also index into nested structures

        >>> select = Select(0, [1, 0])
        >>> x = (torch.ones(1), (torch.ones(1)*5, torch.ones(3,3)))
        >>> select(x)
        (tensor([1.]), tensor([5.]))
        >>> select = Select([1,1])
        >>> select(x)
        (tensor([[1., 1., 1.],
                [1., 1., 1.],
                [1., 1., 1.]]),)
    """

    def __init__(self, *idxs):
        super().__init__()
        self.idxs = idxs

    def forward(self, x):  # pylint: disable=arguments-differ
        """Forward method."""
        return tuple(
            _get_nested_indices(x, idx) if isinstance(idx, (list, tuple)) else x[idx]
            for idx in self.idxs
        )


def _get_nested_indices(indexable, idxs):
    if not idxs:
        return indexable
    return _get_nested_indices(indexable[idxs[0]], idxs[1:])

"""
Module to contain utility modules such as Recall, Concurrent, Select etc.
"""
import torch

from borch import nn


class Identity(nn.Module):
    """
    Identity Module outputs its input

    Examples:
        >>> import torch
        >>> identity = Identity()
        >>> x = torch.ones(2)
        >>> identity(x)
        tensor([1., 1.])
    """

    @staticmethod
    def forward(x):  # pylint: disable=arguments-differ
        """Forward method."""
        return x


class Apply(nn.Module):
    """
    Creates a module that applies a given function in the forward pass.

    Args:
        fn: Function to use in the forward pass of the module.

    Examples:
        >>> import torch
        >>> doubler = Apply(lambda x: 2*x)
        >>> x = torch.ones(2)
        >>> doubler(x)
        tensor([2., 2.])

        To make a resblock
        >>> res_block = nn.Sequential(
        ...     nn.Concurrent(
        ...         nn.Conv2d(3, 3, 3, padding=1),
        ...         Identity(),
        ...     ),
        ...     Apply(lambda x, y: x + y)
        ... )
    """

    def __init__(self, fn):
        super().__init__()
        self._fn = fn

    def forward(self, *x):
        """Forward method."""
        return self._fn(*x)


class Cat(nn.Module):
    """
    Concatenates a tuple of tensors on the dim'th dimension - 1st dimenstion by default,
    as this is where  we have the channels of regular featuremaps

    Args:
        dim: The dimension on which to concatenate the tensors.

    Examples:
        >>> featuremap1 = torch.randn(2, 3, 16, 16)
        >>> featuremap2 = torch.randn(2, 4, 16, 16)
        >>> featuremap3 = torch.randn(2, 5, 16, 16)
        >>> concatter = Cat(dim = 1)
        >>> featuremap = concatter(featuremap1, featuremap2, featuremap3)
        >>> featuremap.shape
        torch.Size([2, 12, 16, 16])
    """

    def __init__(self, dim=1):
        super().__init__()
        self.dim = dim

    def forward(self, *x):
        """Forward method."""
        return torch.cat(x, self.dim)

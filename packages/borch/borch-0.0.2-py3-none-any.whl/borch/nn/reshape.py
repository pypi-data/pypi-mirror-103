"""
Modules that changes the shapes of their input.
"""

from borch import nn


class View(nn.Module):
    r"""
    Creates a View operation that changes the shape of the input to the
    format specified in the init arguments.

    Args:
        *args: args to be fed into input.view()

    Examples:
        >>> import torch
        >>> view = View(1, -1)
        >>> input = torch.randn(10,1,1,1,10)
        >>> out = view(input)
        >>> out.shape
        torch.Size([1, 100])
    """

    def __init__(self, *args):
        super().__init__()
        self.args = args

    def forward(self, val):  # pylint: disable=arguments-differ
        """Forward method."""
        return val.view(*self.args)

    def __repr__(self):
        return "View(%s)" % ", ".join([str(val) for val in self.args])


class BatchView(nn.Module):
    r"""
    Creates a View operation that changes the shape of the input to the
    format specified in the init arguments. The first dim on of the out put
    tensor will be the batch shape of the input.

    Args:
        *args: args to be fed into input.view(batch, *args)

    Examples:
        >>> import torch
        >>> view = BatchView(1, -1)
        >>> input = torch.randn(10,1,1,1,10)
        >>> out = view(input)
        >>> out.shape
        torch.Size([10, 1, 10])
    """

    def __init__(self, *args):
        super().__init__()
        self.args = args

    def forward(self, val):  # pylint: disable=arguments-differ
        """Forward method."""
        return val.view(val.size(0), *self.args)

    def __repr__(self):
        return "BatchView(%s)" % ", ".join([str(val) for val in self.args])


class Flatten(nn.Module):
    r"""
    Creates a View operation that changes the shape of the input to the
    batch shape and a second dim.

    Examples:
        >>> import torch
        >>> view = Flatten()
        >>> input = torch.randn(10,1,1,1,10)
        >>> out = view(input)
        >>> out.shape
        torch.Size([10, 10])
    """

    @staticmethod
    def forward(val):  # pylint: disable=arguments-differ
        """Forward method."""
        return val.view(val.size(0), -1)

    def __repr__(self):
        return "Flatten()"


class Expand(nn.Module):
    r"""
    Creates a expand operation that changes the shape of the input to the
    format specified in the init arguments.

    Args:
        *args: args to be fed into input.expand(batch, *args)

    Examples:
        >>> import torch
        >>> view = Expand(-1, 3)
        >>> input = torch.randn(10,1)
        >>> out = view(input)
        >>> out.shape
        torch.Size([10, 3])
    """

    def __init__(self, *args):
        super().__init__()
        self.args = args

    def forward(self, val):  # pylint: disable=arguments-differ
        """Forward method."""
        return val.expand(*self.args)

    def __repr__(self):
        return "Expand(%s)" % ", ".join([str(val) for val in self.args])


class ExpandBatch(nn.Module):
    r"""
    Creates a expand operation that changes the shape of the input to the
    format specified in the init arguments. The first dim on of the out put
    tensor will be the batch shape of the input.

    Args:
        *args: args to be fed into input.expand(batch, *args)

    Examples:
        >>> import torch
        >>> view = ExpandBatch(1, 10)
        >>> input = torch.randn(10,1,1)
        >>> out = view(input)
        >>> out.shape
        torch.Size([10, 1, 10])
    """

    def __init__(self, *args):
        super().__init__()
        self.args = args

    def forward(self, val):  # pylint: disable=arguments-differ
        """Forward method."""
        return val.expand(val.size(0), *self.args)

    def __repr__(self):
        return "ExpandBatch(%s)" % ", ".join([str(val) for val in self.args])

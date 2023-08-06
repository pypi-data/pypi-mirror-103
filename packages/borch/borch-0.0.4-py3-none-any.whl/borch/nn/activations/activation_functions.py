"""
Implementations of activation functions.
"""


import torch.nn.functional as F

from borch import nn


class Hswish(nn.Module):
    """
    implements the h-swish non-linearity from https://arxiv.org/abs/1905.02244
    """

    def __init__(self, inplace=True):
        super(Hswish, self).__init__()
        self.inplace = inplace

    def forward(self, x):  # pylint: disable=arguments-differ
        """Forward method."""
        return x * F.relu6(x + 3.0, inplace=self.inplace) / 6.0


class Hsigmoid(nn.Module):
    """
    implements the h-sigmoid non-linearity from https://arxiv.org/abs/1905.02244
    """

    def __init__(self, inplace=True):
        super(Hsigmoid, self).__init__()
        self.inplace = inplace

    def forward(self, x):  # pylint: disable=arguments-differ
        """Forward method."""
        return F.relu6(x + 3.0, inplace=self.inplace) / 6.0

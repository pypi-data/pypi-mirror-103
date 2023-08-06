"""
Implementation of Transformed parameter. It is a tensor that has an underlying u_tensor
short for "unconstrained tensor" and a transformation on the u_tensor. It is useful in
cases where we want to optimise a value with some kind of constraint. For example,
standard deviation of a normal distribution is not allowed to be negative. Therefore we
use a TransformedParameter with transformation exp(u_tensor) and this transformed tensor
will only be defined in the region (0, inf).
"""

import torch

from borch.tensor.tensor_base import TensorBase


class TransformedParameter(TensorBase):
    """Tensor that is the result of `transformation(u_tensor)` where
    transformation is a  callable python object and u_tensor is a torch
    tensor. The result of the transformation can be updated using
    `recalculate` method.
    """

    def __init__(self, transformation, u_tensor):
        if not callable(transformation):
            raise ValueError("transformation must be a callable")

        if not isinstance(u_tensor, torch.Tensor):
            raise ValueError("u_tensor must be a torch.Tensor")

        super().__init__()

        self._parameters["u_tensor"] = u_tensor
        self.transformation = transformation
        self._expand = self.transformation(self.u_tensor).size()
        self.recalculate()

    @property
    def u_tensor(self):
        """ Access the u_tensor saved in the transformed parameter """
        return self._parameters["u_tensor"]

    @u_tensor.setter
    def u_tensor(self, value):
        self._parameters["u_tensor"] = value

    def _recalculate_transformation(self):
        """
        Forces the recalculation of the tensor according to the transformation.
        """
        new_calc = self.transformation(self.u_tensor)
        self.set_value_(new_calc)

    def recalculate(self):
        """
        Recalculates all internal values affected by a change to a `.data` in
        one of the arguments

        Returns:
            None
        """
        self._recalculate_transformation()


TP = TransformedParameter

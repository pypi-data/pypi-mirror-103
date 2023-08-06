"""
Base class used as with multiple inheritance when inheriting from torch.tensor
"""
from numbers import Number

import torch
from torch import Tensor

from borch.utils.torch_utils import copy_tensor_attributes


class TensorBase(Tensor):
    """Base class for any tensors which contain subparameters. For example,
    `TransformedParameter` and `RandomVariable`. It ensures that some of the
    new methods are transferred during certain operations such as clone etc.

    Todo:
        Make this inherit from Parameter and reap the benefits.
    """

    # pylint: disable=unused-argument,protected-access

    def __new__(cls, *args, **kwargs):
        requires_grad = False
        return Tensor._make_subclass(cls, Tensor(1), requires_grad)

    def __init__(self):
        super().__init__()
        self._parameters = {}

    def __repr__(self):
        return f"{self.__class__.__name__} containing:\n{Tensor.__repr__(self)}"

    def __reduce_ex__(self, protocol):
        return object.__reduce_ex__(self, protocol)

    def __getstate__(self):
        state = self.__dict__.copy()
        state["value"] = self.data
        return state

    def __setstate__(self, state):
        # pylint: disable=attribute-defined-outside-init
        self.data = state.pop("value")
        self.__dict__ = state.copy()

    def __ipow__(self, other):
        # this is not supposed to be an abstract method...
        raise RuntimeError("in-place pow not implemented")

    def expand(self, *sizes):  # todo might wor
        """Returns a view of the tensor according to the provided arg.

        Args:
            sizes: Size to expand the tensor to.

        Returns:
            New tensor of type `type(self)`.
        """
        temp = super().expand(*sizes).clone()
        return copy_tensor_attributes(self, temp)

    def view(self, *args) -> Tensor:
        """Returns a new tensor with the same data as the `self` tensor but
            of a different size.

        Args:
            args (torch.Size or int [int ...]): desired size for the new view.

        Returns:
            New tensor of type `type(self)`.
        """
        temp = super().view(*args)
        return copy_tensor_attributes(self, temp)

    def clone(self):
        """Returns a copy of the self tensor. The copy has the same size and
            data type as self.

        Returns:
            torch.tensor, a clone of it self

        """
        temp = super().clone()
        return copy_tensor_attributes(self, temp)

    def set_value_(self, value):
        """Sets the value of the TensorBase as copy of `val`

        Args:
          value: Value to set the TensorBase to.

        Returns:
            A TensorBase object (reference to self)
        """

        if isinstance(value, Number):
            value = self.data * 0 + value

        self.detach_()
        self.data = value.data  # solves broadcast issue with `copy_`
        self.copy_(value)
        return self

    def parameters(self, seen=None):
        """Fetch all parameters from self.

        Yields:
            Parameter, this is any tensor which requires grad and is a leaf.
        """
        if seen is None:
            seen = set()

        for _, param in self.named_parameters(seen):
            yield param

    def recalculate(self):
        """
        Recalculates all internal values affected by a change to a `.data` in
        one of the arguments

        Returns:
            None
        """
        raise NotImplementedError

    def named_parameters(self, seen=None, prefix=""):
        """Fetch all parameters from self and yeilds the name and the param

        Yields:
            name, Parameter: yields the name and and tensor
        """
        if seen is None:
            seen = set()

        for name, var in self._parameters.items():
            if var not in seen:
                seen.add(var)
                if isinstance(var, TensorBase):
                    for _name, _var in var.named_parameters(seen, prefix=name):
                        yield prefix + ("." if prefix else "") + str(_name), _var

                elif isinstance(var, Tensor):
                    yield prefix + ("." if prefix else "") + str(name), var

    def _apply(self, fun):
        self.data = fun(self.data)
        if self.grad is not None:
            self.grad.data = fun(self.grad.data)

        for var in self.parameters():
            if isinstance(var, TensorBase):
                var._apply(fun)
            else:
                var.data = fun(var.data)
                if var.grad is not None:
                    var.grad.data = fun(var.grad.data)

        self.recalculate()

    def cuda(self, device=None):  # pragma: no cover
        r"""Moves all model parameters and buffers to the GPU.
        This also makes associated parameters and buffers different objects. So
        it should be called before constructing optimizer if the module will
        live on GPU while being optimized.
        Arguments:
            device (int, optional): if specified, all parameters will be
                copied to that device
        Returns:
            Module: self
        """
        self._apply(lambda t: t.cuda(device))
        return self

    def cpu(self):  # pragma: no cover
        r"""Moves all model parameters and buffers to the CPU.
        Returns:
            Module: self
        """
        self._apply(lambda t: t.cpu())
        return self

    def type(self, dst_type):
        r"""Casts all parameters and buffers to :attr:`dst_type`.
        Arguments:
            dst_type (type or string): the desired type
        Returns:
            Module: self
        """
        self._apply(lambda t: t.type(dst_type))
        return self

    def float(self):
        r"""Casts all floating point parameters and buffers to float datatype.
        Returns:
            Module: self
        """
        self._apply(lambda t: t.float() if t.is_floating_point() else t)
        return self

    def double(self):
        r"""Casts all floating point parameters and buffers to ``double``
        datatype.
        Returns:
            Module: self
        """
        self._apply(lambda t: t.double() if t.is_floating_point() else t)
        return self

    def half(self):
        r"""Casts all floating point parameters and buffers to ``half``
        datatype.

        Returns:
            Module: self
        """
        self._apply(lambda t: t.half() if t.is_floating_point() else t)
        return self

    def to(self, *args, **kwargs):  # noqa: 195  # pragma: no cover
        r"""Moves and/or casts the parameters and buffers.
        This can be called as
        .. function:: to(device=None, dtype=None, non_blocking=False)
        .. function:: to(dtype, non_blocking=False)
        .. function:: to(tensor, non_blocking=False)
        Its signature is similar to :meth:`torch.Tensor.to`, but only accepts
        floating point desired :attr:`dtype` s. In addition, this method will
        only cast the floating point parameters and buffers to :attr:`dtype`
        (if given). The integral parameters and buffers will be moved
        :attr:`device`, if that is given, but with dtypes unchanged. When
        :attr:`non_blocking` is set, it tries to convert/move asynchronously
        with respect to the host if possible, e.g., moving CPU Tensors with
        pinned memory to CUDA devices.
        See below for examples.
        .. note::
            This method modifies the module in-place.

        Args:
            device (:class:`torch.device`): the desired device of the parameters
                and buffers in this module
            dtype (:class:`torch.dtype`): the desired floating point type of
                the floating point parameters and buffers in this module
            tensor (torch.Tensor): Tensor whose dtype and device are the desired
                dtype and device for all parameters and buffers in this module

        Returns:
            self
        """
        # pylint: disable=too-many-branches
        # TODO: in pytoch copy this from torch.nn.Module as it moves stuff
        # to the c++ backend
        def arg_error():  # pragma: no cover
            "will excists in pytoch c++ code at pytorch .5"
            arg_reprs = [repr(arg) for arg in args]
            for key, val in kwargs.items():
                arg_reprs.append("{}={}".format(key, val))
            return ValueError(
                "module.to expects .to(device), .to(dtype) or "
                ".to(device, dtype), where dtype is a floating "
                "point type, but got .to({})".format(", ".join(arg_reprs))
            )

        nargs = len(args) + len(kwargs)
        device = dtype = None
        if nargs < 1 or nargs > 2:
            raise arg_error()
        for key in kwargs:
            if key == "dtype":
                dtype = kwargs["dtype"]
            elif "device" in kwargs:
                device = kwargs["device"]
            else:
                raise arg_error()
        for arg in args:
            if isinstance(arg, torch.dtype):
                if dtype is not None:
                    raise arg_error()
                dtype = arg
            else:
                if device is not None:
                    raise arg_error()
                device = arg

        if dtype is not None:
            if not dtype.is_floating_point:
                raise arg_error()

            if device is None:
                self._apply(lambda t: t.to(dtype) if t.is_floating_point() else t)
                return self

            self._apply(
                lambda t: t.to(device, dtype) if t.is_floating_point() else t.to(device)
            )
            return self
        self._apply(lambda t: t.to(device))
        return self

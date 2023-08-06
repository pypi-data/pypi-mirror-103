"""
Borch Proxies of PyTorch Modules
================================

This module exposes all PyTorch modules as borchified versions. Each module
can be used as it would be in PyTorch, but note that all parameters have now
been transformed into :class:`RandomVariable` objects according to the
argument `rv_factories` (given at initialisation, see ).

Examples:
    >>> import torch
    >>> linear = torch.nn.Linear(3, 3)  # create a linear module
    >>> # Vanilla Linear has parameters for 'bias' and 'weight'
    >>> len(tuple(linear.parameters()))
    2
    >>> blinear = Linear(3, 3)
    >>> # The ppl proxy has `RandomVariable`s for each of these, each with
    >>> # their own parameters (2 when using Normal: loc, scale).
    >>> len(tuple(blinear.opt_parameters()))
    4
    >>> # with sampling set to False, parameter evaluations are the same
    >>> blinear.sampling(False)
    >>> w1 = blinear.weight
    >>> w2 = blinear.weight
    >>> torch.equal(w1, w2)
    True
    >>> # with sampling set to True, parameter evaluations are stochastic
    >>> blinear.sampling(True)
    >>> w1 = blinear.weight
    >>> w2 = blinear.weight
    >>> torch.equal(w1, w2)
    False
"""

# pylint: disable=protected-access,undefined-all-variable
from functools import wraps

from torch import nn

from borch.distributions import Distribution
from borch.guide import NormalGuide

from borch.module import Module, ModuleMeta
from borch.rv_factories import (
    apply_rv_factory,
    kaiming_normal_rv,
    parameter_to_normal_rv,
    priors_to_rv,
)
from borch.utils.func_tools import assign_docs
from borch.utils.namespace_tools import create_augmented_classes

DOC_PREFIX = """This is a ppl class. Please see `help(borch.nn)` for more information.
If one gives distribution as kwargs, where names match the parameters of the Module, they
will be used as priors for those parameters.
"""


RV_FACTORIES = {
    "Linear": kaiming_normal_rv,
    "Bilinear": kaiming_normal_rv,
    "Conv1d": kaiming_normal_rv,
    "Conv2d": kaiming_normal_rv,
    "Conv3d": kaiming_normal_rv,
    "ConvTranspose1d": kaiming_normal_rv,
    "ConvTranspose2d": kaiming_normal_rv,
    "ConvTranspose3d": kaiming_normal_rv,
    "BatchNorm1d": None,
    "BatchNorm2d": None,
    "BatchNorm3d": None,
    "GRU": kaiming_normal_rv,
}

GUIDE_RV_FACTORIES = {}


def get_rv_factory(cls_name):
    """
    Get the rv function corresponding to Module, if no
    custom rv_factory is defined, a defoult will be returned.
    Args:
        cls_name (sting): the name of the class we want the rv_factory for

    Returns:
        callable, an rv_factory
    """
    return RV_FACTORIES.get(cls_name, parameter_to_normal_rv)


def _get_priors_from_kwargs_(kwargs):
    priors = {}
    for key, val in kwargs.items():
        if isinstance(val, Distribution):
            priors[key] = val
    for key in priors:
        kwargs.pop(key)
    return priors


def get_guide(cls_name):
    """
    Get the guide corresponding to the module. If no custom guide is defined we return
    a NormalGuide

    Args:
        cls_name: Name of the class we want the guide for

    Returns:
        callable, a guide

    """
    return GUIDE_RV_FACTORIES.get(cls_name, NormalGuide)


def _torch_proxy_class_factory(cls):
    @wraps(cls.__init__)
    def _init(self, *args, guide=None, **kwargs):
        # This will become the new init function of borch.nn.<cls.__name__>
        priors = _get_priors_from_kwargs_(kwargs)
        cls.__init__(self, *args, **kwargs)

        if guide is None:
            guide = get_guide(cls.__name__)()

        Module.__init__(self, guide=guide)
        params = self._parameters
        rv_factory = get_rv_factory(cls.__name__)

        for key in priors:
            if key not in params:
                raise ValueError(f"{key} does not match any paramaters in the module")

        apply_rv_factory(
            self, lambda name, param: priors_to_rv(name, param, priors, rv_factory)
        )

    new_cls = ModuleMeta(cls.__name__, (Module, cls), {"__init__": _init})
    assign_docs(new_cls, cls, DOC_PREFIX)
    return new_cls


create_augmented_classes(
    caller=__name__,
    module=nn,
    parent=nn.Module,
    class_factory=_torch_proxy_class_factory,
)

__all__ = [
    "AdaptiveAvgPool1d",
    "AdaptiveAvgPool2d",
    "AdaptiveAvgPool3d",
    "AdaptiveMaxPool1d",
    "AdaptiveMaxPool2d",
    "AdaptiveMaxPool3d",
    "AlphaDropout",
    "AvgPool1d",
    "AvgPool2d",
    "AvgPool3d",
    "BCELoss",
    "BCEWithLogitsLoss",
    "BatchNorm1d",
    "BatchNorm2d",
    "BatchNorm3d",
    "Bilinear",
    "ConstantPad1d",
    "ConstantPad2d",
    "ConstantPad3d",
    "Conv1d",
    "Conv2d",
    "Conv3d",
    "ConvTranspose1d",
    "ConvTranspose2d",
    "ConvTranspose3d",
    "CosineEmbeddingLoss",
    "CosineSimilarity",
    "CrossEntropyLoss",
    "CrossMapLRN2d",
    "DataParallel",
    "Dropout",
    "Dropout2d",
    "Dropout3d",
    "ELU",
    "Embedding",
    "EmbeddingBag",
    "Fold",
    "FractionalMaxPool2d",
    "GLU",
    "GRU",
    "GRUCell",
    "GroupNorm",
    "Hardshrink",
    "Hardtanh",
    "HingeEmbeddingLoss",
    "InstanceNorm1d",
    "InstanceNorm2d",
    "InstanceNorm3d",
    "KLDivLoss",
    "L1Loss",
    "LPPool1d",
    "LPPool2d",
    "LSTM",
    "LSTMCell",
    "LayerNorm",
    "LeakyReLU",
    "Linear",
    "LocalResponseNorm",
    "LogSigmoid",
    "LogSoftmax",
    "MSELoss",
    "MarginRankingLoss",
    "MaxPool1d",
    "MaxPool2d",
    "MaxPool3d",
    "MaxUnpool1d",
    "MaxUnpool2d",
    "MaxUnpool3d",
    "Module",
    "ModuleList",
    "MultiLabelMarginLoss",
    "MultiLabelSoftMarginLoss",
    "MultiMarginLoss",
    "NLLLoss",
    "NLLLoss2d",
    "NormalGuide",
    "PReLU",
    "PairwiseDistance",
    "ParameterList",
    "PixelShuffle",
    "PoissonNLLLoss",
    "RNN",
    "RNNBase",
    "RNNCell",
    "RReLU",
    "ReLU",
    "ReLU6",
    "ReflectionPad1d",
    "ReflectionPad2d",
    "ReplicationPad1d",
    "ReplicationPad2d",
    "ReplicationPad3d",
    "SELU",
    "Sigmoid",
    "SmoothL1Loss",
    "SoftMarginLoss",
    "Softmax",
    "Softmax2d",
    "Softmin",
    "Softplus",
    "Softshrink",
    "Softsign",
    "Tanh",
    "Tanhshrink",
    "Threshold",
    "TripletMarginLoss",
    "Unfold",
    "Upsample",
    "UpsamplingBilinear2d",
    "UpsamplingNearest2d",
    "ZeroPad2d",
]

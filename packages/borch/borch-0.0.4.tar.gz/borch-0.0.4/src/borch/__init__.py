"""
Borch
=====

Borch is a universal probabilistic programing language built on top of pytorch and is
used for probabilistic modeling.

It is designed for fast experimentation and research with probabilistic models. With key
focus on beeing very flexible and expressive withouth sacreficing the usabiilty. Thus it
can be used for a wide range of models from classical hierarchical models on small data
sets to complex deep probabilistic models on large data sets.

borch separates model specification(borch) and inference(infer) into two seperate
packages for maximaple flexability and usability. However borch provides a clean
interface to use in combination with the `infer'.

Examples:
    >>> from borch.utils import torch_utils
    >>> from borch.utils.module_utils import yield_named_opt_param
    >>> from borch import infer, Module, RandomVariable
    >>> from borch.optimizer_collection import OptimizersCollection
    >>> import borch.distributions as dist
    >>> import numpy as np
    >>> import torch
    >>> from torch import optim

    Generate random data


    >>> def generate_dataset(n=100):
    ...     x = np.linspace(0, 10, n)
    ...     y = 2*x+4+np.random.normal(0, 4, n)
    ...     return (torch.tensor(y, dtype=torch.float32),
    ... torch.tensor(x, dtype=torch.float32))
    >>> y, x = generate_dataset(100)

    Defining a linear regression model


    >>> def forward(bm, x):
    ...     bm.b = RandomVariable(dist.Normal(0, 3))
    ...     bm.a = RandomVariable(dist.Normal(0, 3))
    ...     bm.sigma = RandomVariable(dist.LogNormal(1, 1))
    ...     mu = bm.b * x + bm.a
    ...     bm.y = RandomVariable(dist.Normal(mu, bm.sigma))
    ...     return bm.y
    >>> model = Module()
    >>> model.observe(y=y)
    >>> optimizer = OptimizersCollection(optimizer=optim.Adam, lr=0.01,
    ...     amsgrad=True)

    Training loop



    >>> for e in range(2):
    ...     model.sample()
    ...     yhat = forward(model, x)
    ...     loss = infer.vi_loss(**model.pq_to_infer())
    ...     loss.backward()
    ...     optimizer.step(model.opt_parameters())
    ...     optimizer.zero_grad()
"""


from borch.version import __version__
from borch.module import Module
from borch import infer, metrics, guide
from borch.tensor import RandomVariable, RV, TransformedParameter, TP

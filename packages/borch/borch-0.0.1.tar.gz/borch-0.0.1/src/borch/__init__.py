"""
Import all the ppl python packages

.. rubric:: References

.. bibliography:: references.bib
   :all:

"""
try:
    import torch

    torch.set_flush_denormal(True)
except ImportError:
    pass

from borch.version import __version__
from borch import ppl, infer, metrics

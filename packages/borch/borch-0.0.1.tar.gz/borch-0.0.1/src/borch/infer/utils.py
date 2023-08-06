"""
Exposes the function `kl_exists` which checks for kl divergence
existence between two distributions.
"""
from torch.distributions import Distribution
from torch.distributions.kl import _KL_REGISTRY

KL_REGISTRY = {
    (key[0].__name__, key[1].__name__): val for key, val in _KL_REGISTRY.items()
}


def kl_exists(p_dist: Distribution, q_dist: Distribution) -> bool:
    """Determine whether the kl divergence is implemented between
    ``p_dist`` and ``q_dist``.

    Args:
        p_dist: Prior distribution.
        q_dist: Approximating distribution.

    Returns:
        True/False: whether kl divergence is defined.
    """
    key = (type(p_dist).__name__, type(q_dist).__name__)
    return KL_REGISTRY.get(key) is not None

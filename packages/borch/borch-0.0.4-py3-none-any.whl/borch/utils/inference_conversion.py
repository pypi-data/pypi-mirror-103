""" Functions to convert collections of random variables to format
supported by infer package"""
from borch.tensor import RandomVariable


def pq_dict_to_lists(rvar_dict):
    """Take a dict with `RandomVariable`s as keys and approximating
     `RandomVariable`s as values as an imput.
     Then converts them to a dict with lists that can be used
      in the infer package.

    Args:
      rvar_dict: dict with `RandomVariable`s as keys and
    approximating `RandomVariable`s as values.

    Returns:
      dict with lists

    """
    p_dists = []
    q_dists = []
    values = []
    observed = []
    for key, val in rvar_dict.items():
        _check_is_random_variable(key, val)
        p_dists.append(key.distribution)
        q_dists.append(val.distribution)
        values.append(val)
        observed.append(val.observed is not None)
    return {
        "p_dists": p_dists,
        "q_dists": q_dists,
        "values": values,
        "observed": observed,
    }


def _check_is_random_variable(*rvars):
    for rvar in rvars:
        if not isinstance(rvar, RandomVariable):
            raise ValueError("One of the provided values is" " not a RandomVariable")


def rsample_else_sample(rvar):
    """
    Draws a sample from the rvar, if rsample is possible to call
    it will be used. If not sample will be called.

    Args:
        rvar (ppl.RandomVariable): the rvar to sample

    Returns:
        the sample
    """
    if rvar.has_rsample:
        return rvar.rsample()
    return rvar.sample()

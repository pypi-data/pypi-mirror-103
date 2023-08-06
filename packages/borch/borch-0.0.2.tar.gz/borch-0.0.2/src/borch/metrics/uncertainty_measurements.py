"""
Implementation of different uncertainty measurements for `RandomVariable`s
that can be used to quantifying the uncertainty. Different uncertainty measurements
measure different types of uncertainty.

Aleatoric uncertainty is also known as statistical uncertainty, represent the
unknowns that differ each time one run the same experiment.

Epistemic uncertainty is also known as systematic uncertainty, represent things one
uncertainty in the model of the process. It is due to limited data and knowledge


    >>> from borch import RV, distributions
    >>> rv = RV(distributions.Normal(0,1))
    >>> het_aleatoric_uncertainty(rv)
    tensor(1.)
    >>> epistemic_uncertainty(rv)
    tensor(1.4189)

"""
import torch


def het_aleatoric_uncertainty(rv):
    """
    Heteroscedastic aleatoric uncertainty is also known as statistical uncertainty,
    represent the unknowns that differ each time one run the same experiment.

    Args:
        rv (RandomVariable): the random variable to calculate the heteroscedastic
        aleatoric uncertainty for.

    Returns:
        torch.tensor with the calculated uncertainty

    Examples:
        >>> from borch import RV, distributions
        >>> rv = RV(distributions.Normal(0,1))
        >>> het_aleatoric_uncertainty(rv)
        tensor(1.)

    """
    return rv.variance


def epistemic_uncertainty(rv):
    """
    Epistemic uncertainty is also known as systematic uncertainty, represent things one
    uncertainty in the model of the process. It is due to limited data and knowledge.

    Args:
        rv (RandomVariable): the random variable to calculate the epistemic_uncertainty
         for.

    Returns:
        torch.tensor with the calculated uncertainty

    Examples:
        >>> from borch import RV, distributions
        >>> rv = RV(distributions.Normal(0,1))
        >>> epistemic_uncertainty(rv)
        tensor(1.4189)
    """
    try:
        return rv.entropy()
    except NotImplementedError:
        return torch.tensor(float("nan"))  # pylint: disable=not-callable

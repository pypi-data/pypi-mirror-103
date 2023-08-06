"""
Constraints

Functionality to encode constraints. For example the scale of a
normal distribution is Positive.

"""
# pylint: disable=invalid-name,abstract-method,comparison-with-itself
import torch


def constraint_from_string(constraint_string):
    """Crates a constrint from a string

    Args:
        constraint_string (str): the string representation of the Constraint

    Returns:
        a Constraint

    Example:
        >>> con = constraint_from_string('Real()')
        >>> isinstance(con, Real)
        True
    """
    return eval(constraint_string)  # pylint: disable=eval-used


class Constraint:
    """
    Abstract base class for constraints.

    A constraint object represents a region over which a variable is valid,
    e.g. within which a variable can be optimized.
    """

    def check(self, value):
        """
        Returns a byte tensor of `sample_shape + batch_shape` indicating
        whether each event in value satisfies this constraint.
        """
        raise NotImplementedError

    def __repr__(self):
        return self.__class__.__name__ + "()"


class _ConstraintLBUB(Constraint):
    # pylint: disable=abstract-method
    """
    Abstract base class for constraints with an upper and lower bound
    """

    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def __repr__(self):
        fmt_string = self.__class__.__name__
        fmt_string += "(lower_bound={}, upper_bound={})".format(
            self.lower_bound, self.upper_bound
        )
        return fmt_string


class _ConstraintUB(Constraint):
    # pylint: disable=abstract-method
    """
    Abstract base class for constraints with an upper bound
    """

    def __init__(self, upper_bound):
        self.upper_bound = upper_bound

    def __repr__(self):
        fmt_string = self.__class__.__name__
        fmt_string += "(upper_bound={})".format(self.upper_bound)
        return fmt_string


class _ConstraintLB(Constraint):
    # pylint: disable=abstract-method
    """
    Abstract base class for constraints with an lower bound
    """

    def __init__(self, lower_bound):
        self.lower_bound = lower_bound

    def __repr__(self):
        fmt_string = self.__class__.__name__
        fmt_string += "(lower_bound={})".format(self.lower_bound)
        return fmt_string


class Dependent(Constraint):
    """
    Placeholder for variables whose support depends on other variables.
    These variables obey no simple coordinate-wise constraints.
    """

    def check(self, value):
        raise ValueError("Cannot determine validity of dependent constraint")


def is_dependent(constraint):
    """Check if the constraint is dependent"""
    return isinstance(constraint, Dependent)


class DependentProperty(property, Dependent):
    """
    Decorator that extends @property to act like a `Dependent` constraint when
    called on a class and act like a property when called on an object.

    Example::

        class Uniform(Distribution):
            def __init__(self, low, high):
                self.low = low
                self.high = high
            @constraints.DependentProperty
            def support(self):
                return constraints.interval(self.low, self.high)
    """


class Boolean(Constraint):
    """
    Constrain to the two values `{0, 1}`.
    """

    def check(self, value):
        return (value == 0) | (value == 1)


class IntegerInterval(_ConstraintLBUB):
    """
    Constrain to an integer interval `[lower_bound, upper_bound]`.
    """

    def check(self, value):
        return (
            (value % 1 == 0) & (self.lower_bound <= value) & (value <= self.upper_bound)
        )


class IntegerLessThan(_ConstraintUB):
    """
    Constrain to an integer interval `(-inf, upper_bound]`.
    """

    def check(self, value):
        return (value % 1 == 0) & (value <= self.upper_bound)


class IntegerGreaterThan(_ConstraintLB):
    """
    Constrain to an integer interval `[lower_bound, inf)`.
    """

    def check(self, value):
        return (value % 1 == 0) & (value >= self.lower_bound)


class Real(Constraint):
    """
    Trivially constrain to the extended real line `[-inf, inf]`.
    """

    def check(self, value):
        return value == value  # False for NANs.


class GreaterThan(_ConstraintLB):
    """
    Constrain to a real half line `(lower_bound, inf]`.
    """

    def check(self, value):
        return self.lower_bound < value


class GreaterThanEq(_ConstraintLB):
    """
    Constrain to a real half line `[lower_bound, inf)`.
    """

    def check(self, value):
        return self.lower_bound <= value


class Positive(Constraint):
    """
    Constrain to a real half line `[0, inf)`.
    """

    def check(self, value):
        return value >= 0


class LessThan(_ConstraintUB):
    """
    Constrain to a real half line `[-inf, upper_bound)`.
    """

    def check(self, value):
        return value < self.upper_bound


class Interval(_ConstraintLBUB):
    """
    Constrain to a real interval `[lower_bound, upper_bound]`.
    """

    def check(self, value):
        return (self.lower_bound <= value) & (value <= self.upper_bound)


class HalfOpenInterval(_ConstraintLBUB):
    """
    Constrain to a real interval `[lower_bound, upper_bound)`.
    """

    def check(self, value):
        return (self.lower_bound <= value) & (value < self.upper_bound)


class Simplex(Constraint):
    """
    Constrain to the unit simplex in the innermost (rightmost) dimension.
    Specifically: `x >= 0` and `x.sum(-1) == 1`.
    """

    def check(self, value):
        return torch.all(value >= 0, dim=-1) & ((value.sum(-1) - 1).abs() < 1e-6)


class LowerTriangular(Constraint):
    """
    Constrain to lower-triangular square matrices.
    """

    def check(self, value):
        value_tril = value.tril()
        return (value_tril == value).view(value.shape[:-2] + (-1,)).min(-1)[0]


class LowerCholesky(Constraint):
    """
    Constrain to lower-triangular square matrices with positive diagonals.
    """

    def check(self, value):
        value_tril = value.tril()
        lower_tri = (value_tril == value).view(value.shape[:-2] + (-1,)).min(-1)[0]

        positive_diagonal = (value.diagonal(dim1=-2, dim2=-1) > 0).min(-1)[0]
        return lower_tri & positive_diagonal


class PositiveDefinite(Constraint):
    """
    Constrain to positive-definite matrices.
    """

    def check(self, value):
        matrix_shape = value.shape[-2:]
        batch_shape = value.unsqueeze(0).shape[:-2]
        # TODO: replace with batched linear algebra routine when one becomes available
        # note that `symeig()` returns eigenvalues in ascending order
        flattened_value = value.reshape((-1,) + matrix_shape)
        return torch.stack(
            [v.symeig(eigenvectors=False)[0][:1] > 0.0 for v in flattened_value]
        ).view(batch_shape)


class RealVector(Constraint):
    """
    Constrain to real-valued vectors. This is the same as `constraints.real`,
    but additionally reduces across the `event_shape` dimension.
    """

    def check(self, value):
        return torch.all(value == value, dim=-1)  # False for NANs.


class Cat(Constraint):
    """
    Constraint functor that applies a sequence of constraints
    `cseq` at the submatrices at dimension `dim`,
    each of size `lengths[dim]`, in a way compatible with :func:`torch.cat`.
    """

    def __init__(self, cseq, dim=0, lengths=None):
        assert all(isinstance(c, Constraint) for c in cseq)
        self.cseq = list(cseq)
        if lengths is None:
            lengths = [1] * len(self.cseq)
        self.lengths = list(lengths)
        assert len(self.lengths) == len(self.cseq)
        self.dim = dim

    def check(self, value):
        assert -value.dim() <= self.dim < value.dim()
        checks = []
        start = 0
        for constr, length in zip(self.cseq, self.lengths):
            v = value.narrow(self.dim, start, length)
            checks.append(constr.check(v))
            start = start + length  # avoid += for jit compat
        return torch.cat(checks, self.dim)


class Stack(Constraint):
    """
    Constraint functor that applies a sequence of constraints
    `cseq` at the submatrices at dimension `dim`,
    in a way compatible with :func:`torch.stack`.
    """

    def __init__(self, cseq, dim=0):
        assert all(isinstance(c, Constraint) for c in cseq)
        self.cseq = list(cseq)
        self.dim = dim

    def check(self, value):
        assert -value.dim() <= self.dim < value.dim()
        vs = [value.select(self.dim, i) for i in range(value.size(self.dim))]
        return torch.stack(
            [constr.check(v) for v, constr in zip(vs, self.cseq)], self.dim
        )


dependent = Dependent()
boolean = Boolean()
nonnegative_integer = IntegerGreaterThan(0)
positive_integer = IntegerGreaterThan(1)
real = Real()
real_vector = RealVector()
positive = Positive()
unit_interval = Interval(0.0, 1.0)
simplex = Simplex()
lower_triangular = LowerTriangular()
lower_cholesky = LowerCholesky()
positive_definite = PositiveDefinite()

"""Definition of complexity classes."""

import numpy as np

from py_pal.util import setup_logging

logger = setup_logging(__name__)


class NotFittedError(Exception):
    pass


class UnderDeterminedEquation(Exception):
    pass


class Complexity:
    """Abstract class that fits complexity classes to timing data."""

    def __init__(self):
        # list of parameters of the fitted function class as returned by the
        # last square method np.linalg.lstsq
        self.coeff = None

    def fit(self, n: np.ndarray, t: np.ndarray) -> float:
        """Fit complexity class parameters to timing data.

        Arguments:
            n (:class:`numpy.ndarray`): Array of values of N for which execution time has been measured.
            t (:class:`numpy.ndarray`): Array of execution times for each N in seconds.

        Returns:
            :class:`numpy.ndarray`: Residuals, sum of square errors of fit
        """
        logger.debug(f"x-axis (argument proxy value):\n{n}")
        logger.debug(f"y-axis (aggregated opcodes):\n{t}")
        x = self.transform_n(n)
        y = self.transform_y(t)
        logger.debug(f"x-axis (transformed):\n{x}")
        logger.debug(f"y-axis (transformed):\n{y}")
        x = np.nan_to_num(x)
        y = np.nan_to_num(y)
        logger.debug(f"x-axis (NaN and infinite values replaced):\n{x}")
        logger.debug(f"y-axis (NaN and infinite values replaced):\n{y}")

        coeff, residuals, rank, s = np.linalg.lstsq(x, y, rcond=-1)

        if len(residuals) == 0:
            raise UnderDeterminedEquation("Missing residuals")

        self.coeff = coeff
        return residuals[0]

    def compute(self, n: np.ndarray) -> float:
        """Compute the value of the fitted function at `n`. """
        if self.coeff is None:
            raise NotFittedError()

        # Result is linear combination of the terms with the fitted coefficients
        x = self.transform_n(n)
        tot = 0
        for i in range(len(self.coeff)):
            tot += self.coeff[i] * x[:, i]
        return tot

    def __str__(self):
        prefix = '{}: '.format(self.__class__.__name__)

        if self.coeff is None:
            return prefix + ': not yet fitted'
        return prefix + self.format_str().format(*tuple(self.coeff))

    # --- abstract methods

    @classmethod
    def format_str(cls):
        """Return a string describing the fitted function.

        The string must contain one formatting argument for each coefficient.
        """
        return 'FORMAT STRING NOT DEFINED'

    def transform_n(self, n: np.ndarray):
        """Terms of the linear combination defining the complexity class.

        Output format: number of Ns x number of coefficients.
        """
        raise NotImplementedError()

    def transform_y(self, t: np.ndarray):
        """Transform time as needed for fitting. (e.g., t->log(t)) for exponential class."""
        return t

    def __gt__(self, other):
        if self.__class__ == other.__class__ and self.coeff is not None and other.coeff is not None:
            return self.coeff[-1] > other.coeff[-1]
        return ALL_CLASSES.index(self.__class__) > ALL_CLASSES.index(other.__class__)


# --- Concrete implementations of the most popular complexity classes

class Constant(Complexity):
    def transform_n(self, n: np.ndarray):
        return np.ones((len(n), 1))

    @classmethod
    def format_str(cls):
        return '= {:.2G}'


class Linear(Complexity):
    def transform_n(self, n: np.ndarray):
        return np.vstack([np.ones(len(n)), n]).T

    @classmethod
    def format_str(cls):
        return '= {:.2G} + {:.2G}*n'


class Quadratic(Complexity):
    def transform_n(self, n: np.ndarray):
        return np.vstack([np.ones(len(n)), n * n]).T

    @classmethod
    def format_str(cls):
        return '= {:.2G} + {:.2G}*n^2'


class Cubic(Complexity):
    def transform_n(self, n: np.ndarray):
        return np.vstack([np.ones(len(n)), n ** 3]).T

    @classmethod
    def format_str(cls):
        return '= {:.2G} + {:.2G}*n^3'


class Logarithmic(Complexity):
    def transform_n(self, n: np.ndarray):
        return np.vstack([np.ones(len(n)), np.log(n)]).T

    @classmethod
    def format_str(cls):
        return '= {:.2G} + {:.2G}*log(n)'


class Linearithmic(Complexity):
    def transform_n(self, n: np.ndarray):
        return np.vstack([np.ones(len(n)), n * np.log(n)]).T

    @classmethod
    def format_str(cls):
        return '= {:.2G} + {:.2G}*n*log(n)'


class Polynomial(Complexity):
    def transform_n(self, n: np.ndarray):
        return np.vstack([np.ones(len(n)), np.log(n)]).T

    def transform_y(self, t: np.ndarray):
        return np.log(t)

    @classmethod
    def format_str(cls):
        return '= {:.2G} * x^{:.2G}'


class Exponential(Complexity):
    def transform_n(self, n: np.ndarray):
        return np.vstack([np.ones(len(n)), n]).T

    def transform_y(self, t: np.ndarray):
        return np.log(t)

    @classmethod
    def format_str(cls):
        return '= {:.2G} * {:.2G}^n'


ALL_CLASSES = [Constant, Logarithmic, Linear, Linearithmic, Quadratic, Cubic, Polynomial, Exponential]

"""
Standard checks of randomization. These are mainly used in the unit test suite to sanity check
randomization utilities in this package.
"""

import logging
from typing import Union, List

from numpy import ndarray, median, sqrt

# set logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define public functions (ignored by jupyter notebooks)
__all__ = [
    "runs_test"
]

####################################################################################################


def runs_test(arr: Union[ndarray, List]) -> float:
    """
    runs_test

    Run tests are a very simple method of sanity checking a set of random numbers. A run is defined
    as a series of increasing values or a series of decreasing values. The number of increasing, or
    decreasing, values is the length of the run.

    In a random data set, the probability that the (I+1)th value is larger or smaller than the Ith
    value follows a binomial distribution, which forms the basis of the runs test.

    Null Hypothesis: The sequence was produced in a random manner.

    Frequentist test statistics can be viewed as thresholds on signal to noise ratios (see equation
    below). For this test, the signal is difference in actual number of runs and expected number of
    runs given sample size.

    test statistis = Z = signal / noise = (R - R_bar) / sigma_R

    Parameters
    ----------
    arr: ndarray, list
        A 1d array or list of values to evaluate for "randomness"

    Returns
    -------

    Examples
    --------
    >>> random_arr = np.radnom.normal(0, 10, 1000)
    >>> z_statistic = runs_test(random_arr)

    References
    ----------
    Bradley
        * Distribution-Free Statistical Tests (1968), Chapter 12
    NIST
        * Engineering Statistics Handbook 1.3.5.13

    """
    runs, n1, n2 = 0, 0, 0
    arr_median = median(arr)

    # Checking for start of new run
    for i in range(len(arr)):
        # no. of runs
        if (arr[i] >= arr_median > arr[i - 1]) or (arr[i] < arr_median <= arr[i - 1]):
            runs += 1
        # no. of positive values
        if arr[i] >= arr_median:
            n1 += 1
        # no. of negative values
        else:
            n2 += 1

    runs_exp = ((2 * n1 * n2) / (n1 + n2)) + 1
    stan_dev = sqrt((2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / (((n1 + n2) ** 2) * (n1 + n2 - 1)))
    return (runs - runs_exp) / stan_dev

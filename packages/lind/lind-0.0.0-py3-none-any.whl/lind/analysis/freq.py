"""
Frequentist Tests

Note on estimating the population variance: We often use n-1 instead of n when estimating the
population variance (Bessel's correction), where n is the number of samples. This method corrects
the bias in the estimation of the population variance. It also partially corrects the bias in the
estimation of the population standard deviation. However, the correction often increases the mean
squared error in these estimations. When n is large this correction is small.

TODO: add continuity corrections to unpooled z tests
"""

from typing import Tuple
import logging

import numpy as np
from numpy import ndarray
from scipy.stats import norm, t
from scipy import stats

# set logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__all__ = [
    'find_p_value', 'find_test_statistic', 'find_confidence_interval',
    # 'mean', 'variance', 'standard_deviation',
    'one_samp_z_prop', 'two_samp_z_prop',
    'one_samp_z', 'two_samp_z',
    'one_samp_t', 'two_samp_t',
]

################################################################################
# auxiliary functions


def find_p_value(test_statistic: float, df: float = np.inf, tails: bool = True) -> float:
    """
    A convenience function for finding p values for t tests and z tests.

    Notes
    -----
    * sf is 1 - cdf

    Parameters
    ----------
    test_statistic: float
        The t or z test statistic
    df: float
        The degrees freedom. If infinity (np.inf), this is assumed to be a z test. Otherwise it is
        assumed to be a t-test.
    tails: bool
        An indicator for two tailed tests. If True, this assumes a two tailed test. If False, this
        assumes a one tailed test.

    Returns
    -------
    float
        The p value corresponding to the test statistic.
    """

    tails = 2 if tails else 1
    if df < np.inf:
        return stats.t.sf(
            np.abs(test_statistic), loc=0.0, scale=1.0, df=df,
        ) * tails
    return stats.norm.sf(
        np.abs(test_statistic),
        loc=0.0, scale=1.0,
    ) * tails


def find_test_statistic(p_value: float, df: float = np.inf, tails: bool = True) -> float:
    """
    A convenience function for recovering t and z test statics from p-values

    Parameters
    ----------
    p_value: float
        The p-value of interest
    df: float
        The degrees freedom. If infinity (np.inf), this is assumed to be a z test. Otherwise it is
        assumed to be a t-test. The degrees freedom is usually the number of total samples minus one
        for the t test.
    tails: bool
        An indicator for two tailed tests. If True, this assumes a two tailed test. If False, this
        assumes a one tailed test.

    Returns
    -------
    float
        The corresponding test statistic
    """

    if p_value <= 0.0 or p_value >= 1.0:
        raise ValueError("Input p must be a float between 0 and 1 non-inclusive.")

    p = 1.0 - p_value
    p = (1.0 + p) / 2.0 if tails is True else p
    if df == np.inf:
        return norm(loc=0.0, scale=1.0).ppf(p)
    return t(loc=0.0, scale=1.0, df=df).ppf(p)


def find_confidence_interval(se: float, df: float = np.inf, alpha: float = 0.05,
                             tails: float = True) -> float:
    """
    A convenience function for finding the confidence interval based on the standard error.

    Parameters
    ----------
    se: float
        The standard error of the measurement (estimate).
    df: float
        The degrees freedom. If infinity (np.inf), this is assumed to be a z test. Otherwise it is
        assumed to be a t-test.
    alpha: float
        The probability of making a type I error. A 95% credible interval has alpha = 5% or .05.
    tails: bool
        An indicator for two tailed tests. If True, this assumes a two tailed test. If False, this
        assumes a one tailed test.

    Returns
    -------
    float
        The width of the confidence interval (absolute units).
    """
    tails = 2 if tails else 1
    confidence = 1.0 - alpha
    q = (1.0 + confidence) / tails
    if df < np.inf:
        return se * stats.t.ppf(
            q=q, loc=0.0, scale=1.0, df=df,
        )
    return se * stats.norm.ppf(
        q=q, loc=0.0, scale=1.0,
    )


################################################################################
# educational functions (not for production use)


def mean(arr: ndarray) -> float:
    """
    An example of how mean is calculated. This function is for educational purposes only. Please use
    np.mean(arr) instead.

    Parameters
    ----------
    arr: ndarray
        An array containing the data to calculate the mean.

    Returns
    -------
    float
        The mean (average).
    """
    logger.warning("Please use the mean function in the numpy project instead.")
    return np.sum(arr) / arr.shape[0]


def variance(arr: ndarray, ddof: int = 0) -> float:
    """
    An example of how variance is calculated. This function is for educational purposes only. Please
    use np.var(arr, ddof) instead.

    Parameters
    ----------
    arr: ndarray
        An array containing the data to calculate the variance.
    ddof: int
        The number of degrees of freedom.

    Returns
    -------
    float
        The variance.
    """
    logger.warning("Please use the stddev function in the numpy project instead.")
    assert ddof >= 0, "Degrees freedom must be greater than or equal to 0"
    # Number of observations
    n = arr.shape[0]
    assert ddof < n, "Degrees freedom must be less than total observations"
    # Mean of the data
    mu = np.sum(arr) / n
    # Square deviations
    deviations = (arr - mu)**2.0
    # Variance
    return np.sum(deviations) / (n - ddof)


def standard_deviation(arr: ndarray, ddof: int = 0) -> float:
    """
    An example of how standard deviation is calculated. This function is for educational purposes
    only. Please use np.std(arr, ddof) instead.

    Parameters
    ----------
    arr: ndarray
        An array containing the data to calculate the standard deviation.
    ddof: int
        The number of degrees of freedom.

    Returns
    -------
    float
        The standard deviation.
    """
    logger.warning("Please use the stddev function in the numpy project instead.")
    return np.sqrt(variance(arr, ddof=ddof))

################################################################################
# normal approximation (z) proportions tests


def _one_samp_z_prop(n: int, successes: int, null_h: float = 0.5) -> Tuple[float, float]:
    """
    Function for one sample z test of proportions.

    Parameters
    ----------
    n: int
        The number of samples (observations).
    successes:
        The number of events.
    null_h: float
        The point null hypothesis to use when comparing the means.

    Returns
    -------
    float
        test statistic (t statistic)
    float
        standard error
    """
    assert successes <= n, "Input successes must be less than or equal to n."
    p_hat = successes / n
    se = np.sqrt(p_hat * (1.0 - p_hat) / (n - 1.0))
    z = (p_hat - null_h) / se
    return z, se


def one_samp_z_prop(sample: ndarray, null_h: float = 0.5) -> Tuple[float, float]:
    """
    Function for one sample z test of proportions.

    Parameters
    ----------
    sample: ndarray
        An array of samples (observations).
    null_h: float
        The point null hypothesis to use when comparing the means.

    Returns
    -------
    float
        test statistic (t statistic)
    float
        standard error
    """
    n = sample.shape[0]
    successes = sample.sum()
    return _one_samp_z_prop(n=n, successes=successes, null_h=null_h)


def paired_z_prop(sample1: ndarray, sample2: ndarray, null_h: float = 0.5) -> Tuple[float, float]:
    """
    Function for paired z test of proportions. Math is the same as for a one sample z test of
    proportions.

    Parameters
    ----------
    sample1 : ndarray
        A numpy array with the unit level data from the first sample.
    sample2 : ndarray
        A numpy array with the unit level data from the second sample.
    null_h: float
        The point null hypothesis to use when comparing the means.

    Returns
    -------
    float
        test statistic (t statistic)
    float
        standard error
    """
    return one_samp_z_prop(sample=sample1-sample2, null_h=null_h)


def _two_samp_z_prop(n1: int, n2: int, successes1: int, successes2: int, null_h: float = 0.0,
                     pooled: bool = False) -> Tuple[float, float]:
    """
    Function for two sample z test of proportions.

    Parameters
    ----------
    n1: int
        The number of data points (observations) in sample one.
    n2: int
        The number of data points (observations) in sample two.
    successes1: int
        The number of events in sample one.
    successes2: int
        The number of events in sample two.
    null_h: float
        The point null hypothesis to use when comparing the means.
    pooled: bool
        Indicates whether to use the assumption that the sample variances are equal or not.
        Pooled = True assumes that the variances are equal. It is common to use the pooled
        assumption given that the unpooled assumption yields over confident estimates in practice
        (barring the appropriate corrections).

    Returns
    -------
    float
        test statistic (t statistic)
    float
        standard error
    """
    assert successes1 <= n1, "Input successes1 must be less than or equal to n1."
    assert successes2 <= n2, "Input successes2 must be less than or equal to n2."
    p1 = successes1 / n1
    p2 = successes2 / n2
    if pooled:
        p = (successes1 + successes2) / (n1 + n2)
        se = np.sqrt(p * (1.0 - p) * (1.0 / n1 + 1.0 / n2))
    else:
        se = np.sqrt(
            p1 * (1.0 - p1) / n1 +
            p2 * (1.0 - p2) / n2
        )
    z = (p1 - p2 - null_h) / se
    return z, se


def two_samp_z_prop(sample1: ndarray, sample2: ndarray, null_h: float = 0.0, pooled: bool = False) \
        -> Tuple[float, float]:
    """
    Function for two sample z test of proportions.

    Parameters
    ----------
    sample1 : ndarray
        A numpy array with the unit level data from the first sample.
    sample2 : ndarray
        A numpy array with the unit level data from the second sample.
    null_h: float
        The point null hypothesis to use when comparing the means.
    pooled: bool
        Indicates whether to use the assumption that the sample variances are equal or not.
        Pooled = True assumes that the variances are equal. It is common to use the pooled
        assumption given that the unpooled assumption yields over confident estimates in practice
        (barring the appropriate corrections).

    Returns
    -------
    float
        test statistic (t statistic)
    float
        standard error
    """
    n1 = sample1.shape[0]
    n2 = sample2.shape[0]
    successes1 = sample1.sum()
    successes2 = sample2.sum()
    return _two_samp_z_prop(n1, n2, successes1, successes2, null_h=null_h, pooled=pooled)

################################################################################
# normal (z) tests


def _one_samp_z(n: int, mu: float, sigma: float, null_h: float = 0.0) -> Tuple[float, float]:
    """
    Function for one sample z test.

    Parameters
    ----------
    n: int
        The number of samples (observations).
    mu: float
        The mean of the sample data.
    sigma: float
        The standard deviation of the sample data.
    null_h: float
        The point null hypothesis to use when comparing the means.

    Returns
    -------
    float
        test statistic (t statistic)
    float
        standard error
    """
    se = sigma / np.sqrt(n)
    z = (mu - null_h) / se
    return z, se


def one_samp_z(sample: ndarray, null_h: float = 0.0) -> Tuple[float, float]:
    """
    Function for one sample z test.

    Parameters
    ----------
    sample: ndarray
        An array of samples (observations).
    null_h: float
        The point null hypothesis to use when comparing the means.

    Returns
    -------
    float
        test statistic (t statistic)
    float
        standard error
    """
    n = sample.shape[0]
    mu = sample.mean()
    sigma = sample.std(ddof=1)
    return _one_samp_z(n=n, mu=mu, sigma=sigma, null_h=null_h)


def paired_z(sample1: ndarray, sample2: ndarray, null_h: float = 0.0) -> Tuple[float, float]:
    """
    Function for paired z test. Math is the same as for a one sample z test.

    Parameters
    ----------
    sample1 : ndarray
        A numpy array with the unit level data from the first sample.
    sample2 : ndarray
        A numpy array with the unit level data from the second sample.
    null_h: float
        The point null hypothesis to use when comparing the means.

    Returns
    -------
    float
        test statistic (t statistic)
    float
        standard error
    """
    return one_samp_z(sample=sample1-sample2, null_h=null_h)


def _two_samp_z(n1: int, n2: int, mu1: float, mu2: float, sigma1: float, sigma2: float,
                null_h: float = 0.0, pooled: bool = False) -> \
        Tuple[float, float]:
    """
    Function for a two sample z test.

    Parameters
    ----------
    n1: int
        The sample size for the first sample.
    n2: int
        The sample size for the second sample.
    mu1: float
        The mean of the first sample.
    mu2: float
        The mean of the second sample.
    sigma1: float
        The standard deviation of the first sample.
    sigma2: float
        The standard deviation of the second sample.
    null_h: float
        The point null hypothesis to use when comparing the means.
    pooled: bool
        Indicates whether to use the assumption that the sample variances are equal or not.
        Pooled = True assumes that the variances are equal. It is common to use the pooled
        assumption given that the unpooled assumption yields over confident estimates in practice
        (barring the appropriate corrections).

    Returns
    -------
    float
        test statistic (t statistic)
    float
        standard error
    """
    if pooled:
        se = np.sqrt(
            (n1 * sigma1 ** 2.0 + n2 * sigma2 ** 2.0) / (n1 + n2 - 2) * (1.0 / n1 + 1.0 / n2)
        )
    else:
        se = np.sqrt(sigma1**2.0 / n1 + sigma2**2.0 / n2)
    z = (mu1 - mu2 - null_h) / se
    return z, se


def two_samp_z(sample1: ndarray, sample2: ndarray, null_h: float = 0.0, pooled: bool = False) -> \
        Tuple[float, float]:
    """
    Function for a two sample z test.

    Parameters
    ----------
    sample1 : ndarray
        A numpy array with the unit level data from the first sample.
    sample2 : ndarray
        A numpy array with the unit level data from the second sample.
    null_h: float
        The point null hypothesis to use when comparing the means.
    pooled: bool
        Indicates whether to use the assumption that the sample variances are equal or not.
        Pooled = True assumes that the variances are equal. It is common to use the pooled
        assumption given that the unpooled assumption yields over confident estimates in practice
        (barring the appropriate corrections).

    Returns
    -------
    float
        test statistic (t statistic)
    float
        standard error
    """
    n1 = sample1.shape[0]
    n2 = sample2.shape[0]
    mu1 = sample1.mean()
    mu2 = sample2.mean()
    sigma1 = sample1.std()
    sigma2 = sample2.std()
    return _two_samp_z(n1=n1, n2=n2, mu1=mu1, mu2=mu2, sigma1=sigma1, sigma2=sigma2, null_h=null_h,
                       pooled=pooled)

################################################################################
# student t tests


def _one_samp_t(n: int, mu: float, sigma: float, null_h: float = 0.0) -> Tuple[float, float, float]:
    """

    Parameters
    ----------
    n: int
        The number of samples (observations).
    mu: float
        The mean of the sample data.
    sigma: float
        The standard deviation of the sample data.
    null_h: float
        The point null hypothesis to use when comparing the means.

    Returns
    -------
    float
        test statistic (t statistic)
    float
        standard error
    float
        degrees freedom
    """
    se = sigma / np.sqrt(n)
    t = (mu - null_h) / se
    df = n - 1.0
    return t, se, df


def one_samp_t(sample: ndarray, null_h: float = 0.0) -> Tuple[float, float, float]:
    """

    Parameters
    ----------
    sample: ndarray
        An array of samples (observations).
    null_h: float
        The point null hypothesis to use when comparing the means.

    Returns
    -------
    float
        test statistic (t statistic)
    float
        standard error
    float
        degrees freedom
    """
    n = sample.shape[0]
    mu = sample.mean()
    sigma = sample.std(ddof=1)
    return _one_samp_t(n=n, mu=mu, sigma=sigma, null_h=null_h)


def paired_t(sample1: ndarray, sample2: ndarray, null_h: float = 0.0) -> Tuple[float, float, float]:
    """

    Parameters
    ----------
    sample1 : ndarray
        A numpy array with the unit level data from the first sample.
    sample2 : ndarray
        A numpy array with the unit level data from the second sample. Must be the same dimensions
        as sample1.
    null_h: float
        The point null hypothesis to use when comparing the means.

    Returns
    -------
    float
        test statistic (t statistic)
    float
        standard error
    float
        degrees freedom
    """
    return one_samp_t(sample=sample1-sample2, null_h=null_h)


def _two_samp_t(n1: int, n2: int, mu1: float, mu2: float, sigma1: float, sigma2: float,
                null_h: float = 0.0, pooled: bool = False) -> Tuple[float, float, float]:
    """
    A simple function for running two sample student t tests.

    Calculate the standard deviation assuming one degree of freedom. For
    example, using numpy np.std(ddof=1).

    Parameters
    ----------
    n1: int
        The sample size for the first sample.
    n2: int
        The sample size for the second sample.
    mu1: float
        The mean of the first sample.
    mu2: float
        The mean of the second sample.
    sigma1: float
        The standard deviation of the first sample.
    sigma2: float
        The standard deviation of the second sample.
    null_h: float
        The point null hypothesis to use when comparing the means.
    pooled: bool
        Indicates whether to use the assumptions that the sample variances are equal or not.
        Pooled = True assumes that the variances are equal. The un-pooled t-test is sometimes
        called Welch's t-test.

    Returns
    -------
    float
        test statistic (t statistic)
    float
        standard error
    float
        degrees freedom

    Examples
    --------
    >>> t_stat, se, df = two_samp_t(
    >>>     n1 = 13, n2 = 10,
    >>>     mu1 = 1.1, mu2 = 1.0,
    >>>     sigma1 = 3.0, sigma2 = 2.0,
    >>>     null_h = 0.0, pooled = False
    >>> )

    References
    ----------
    Bernard Rosner
        * Eq 8.11, 8.21 Fundamentals of Biostatistics
    """

    # v1 = sigma1**2.0
    # v2 = sigma2**2.0
    # if pooled:
    #     df = n1 + n2 - 2.0
    #     svar = ((n1 - 1.0) * v1 + (n2 - 1.0) * v2) / df
    #     se = np.sqrt( svar * (1.0 / n1 + 1.0 / n2))
    # else:
    #     vn1 = v1 / n1
    #     vn2 = v2 / n2
    #     df = (vn1 + vn2)**2 / (vn1**2 / (n1 - 1) + vn2**2 / (n2 - 1))
    #     se = np.sqrt(vn1 + vn2)

    if pooled:
        df = n1 + n2 - 2.0
        sp = np.sqrt(((n1 - 1.0)*sigma1**2.0 + (n2 - 1.0)*sigma2**2.0) / df)
        se = sp * np.sqrt(1.0 / n1 + 1.0 / n2)
    else:
        C = (sigma1**2.0 / n1) / (sigma1**2.0 / n1 + sigma2**2.0 / n2)
        df = (n1 - 1.0) * (n2 - 1.0) / \
            ((n2 - 1.0) * C**2.0 + (1.0 - C)**2.0 * (n1 - 1.0))
        se = np.sqrt(sigma1**2.0 / n1 + sigma2**2.0 / n2)

    t = (mu1 - mu2 - null_h) / se
    return t, se, df


def two_samp_t(sample1: ndarray, sample2: ndarray, null_h: float = 0.0, pooled: bool = False) -> \
        Tuple[float, float, float]:
    """
    A simple function for running two sample student t tests.

    Parameters
    ----------
    sample1 : ndarray
        A numpy array with the unit level data from the first sample.
    sample2 : ndarray
        A numpy array with the unit level data from the second sample.
    null_h: float
        The point null hypothesis to use when comparing the means.
    pooled: bool
        Indicates whether to use the assumptions that the sample variances are equal or not.
        Pooled = True assumes that the variances are equal. The un-pooled t-test is sometimes
        called Welch's t-test

    Returns
    -------
    float
        test statistic (t statistic)
    float
        standard error
    float
        degrees freedom

    Examples
    --------
    >>> t_stat, se, df = two_samp_t(
    >>>     sample1 = np.asarray([1, 2, 3]),
    >>>     sample2 = np.asarray([1, 2, 3]),
    >>>     null_h = 0.0, pooled = False
    >>> )

    References
    ----------
    Bernard Rosner
        * Eq 8.11, 8.21 Fundamentals of Biostatistics
    """

    n1 = sample1.shape[0]
    n2 = sample2.shape[0]
    mu1 = sample1.mean()
    mu2 = sample2.mean()
    sigma1 = sample1.std(ddof=1)
    sigma2 = sample2.std(ddof=1)
    return _two_samp_t(
        n1=n1, n2=n2,
        mu1=mu1, mu2=mu2,
        sigma1=sigma1, sigma2=sigma2,
        null_h=null_h, pooled=pooled
    )

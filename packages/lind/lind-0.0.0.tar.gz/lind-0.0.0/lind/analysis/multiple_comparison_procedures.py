"""
multiple_comparison_procedures: This module contains functions to correct for multiple
comparisons in hypothesis testing. Corrected p values will be referred to as q values. Multiple
comparison procedures (MCPs) are sometimes referred to as correction factors.

MCPs tend to correct for family wise error rate (FWER) or false discovery rate (FDR).

Author's Note: This code draws from example code referenced in Rosetta Code. That code is a
translation of code in the R stats package and falls under the R 4.1.0 license (GPL v2).

Most of the code in this module is based on R source code covered by the GPL license. It is thus a
modified version covered by the GPL.

FDR-controlling procedures are designed to control the expected proportion of "discoveries"
(rejected null hypotheses) that are false (incorrect rejections of the null). FDR-controlling
procedures provide less stringent control of Type I errors compared to family-wise error rate (FWER)
controlling procedures, which control the probability of at least one Type I error.

FDR-controlling procedures have greater power, at the cost of increased numbers of Type I errors.
The power of a binary hypothesis test is the probability that the test rejects the null hypothesis
when a specific alternative hypothesis is true (i.e. the probability of avoiding a type II error).

A type I error is the rejection of a true null hypothesis ("false positive"), while a type II error
is the non-rejection of a false null hypothesis ("false negative").

Sometimes experimenters prefer to use the language of sensitivity ans specificity.
Sensitivity measures the proportion of positives that are correctly identified.
Specificity measures the proportion of negatives that are correctly identified.

Recommended import style:
>>> from lind.analysis import multiple_comparison_procedures as mcp

TODO: There are parts of this code written by convenience that could be vectorized for increased
    speed. Will need to update code in the future to better optimize for speed.

TODO: Add better docstrings to private utility functions

"""

import logging
from typing import Union, List

from numpy import ndarray, zeros, asarray, clip, arange

# set logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define public functions (ignored by jupyter notebooks)
__all__ = ["bh", "by", "bonferonni", "holm", "hommel", "hochberg"]


####################################################################################################


def _order(p_values: Union[List, ndarray], reverse: bool = False) -> Union[List, ndarray]:
    """utility for ordering p value list inputs"""
    if reverse is True:
        return sorted(range(len(p_values)), key=lambda k: p_values[k], reverse=True)
    return sorted(range(len(p_values)), key=lambda k: p_values[k])


def _pminf(arr: Union[List, ndarray]) -> Union[List, ndarray]:
    """utility"""
    n = len(arr)
    pmin_list = zeros(n)
    for i in range(n):
        pmin_list[i] = arr[i] if arr[i] < 1 else 1
    return pmin_list


def _cumminf(arr: Union[List, ndarray]) -> Union[List, ndarray]:
    """utility"""
    cummin = zeros(len(arr))
    cumulative_min = arr[0]
    for i, p in enumerate(arr):
        if p < cumulative_min:
            cumulative_min = p
        cummin[i] = cumulative_min
    return cummin


def _cummaxf(arr: Union[List, ndarray]) -> Union[List, ndarray]:
    """utility"""
    cummax = zeros(len(arr))
    cumulative_max = arr[0]
    for i, e in enumerate(arr):
        if e > cumulative_max:
            cumulative_max = e
        cummax[i] = cumulative_max
    return cummax


####################################################################################################


def bh(p_values: Union[List, ndarray]) -> ndarray:
    """
    bh: Benjamini-Hochberg

    The Benjamini and Hochberg method controls the false discovery rate (FDR), the expected
    proportion of false discoveries amongst the rejected hypotheses. The FDR is a less stringent
    condition than the family-wise error rate (so bh is more powerful than many other correction
    methods).

    Parameters
    ----------
    p_values : Union[List[float], ndarray[float]]
        List or numpy array of p values to be converted into q values

    Returns
    -------
    ndarray[float]
        the q values for the respective p value inputs

    Examples
    --------
    >>> q_values = bh([0.05, 0.002, 0.006])

    References
    ----------
    Benjamini and Hochberg
        * Controlling the false discovery rate: a practical and powerful approach to multiple
          testing

    """

    n = len(p_values)
    cummin_input = zeros(n)
    reverse_p_value_order = _order(p_values, True)
    for i in range(n):
        cummin_input[i] = (n/(n-i))* p_values[reverse_p_value_order[i]]
    pmin = _pminf(_cumminf(cummin_input))
    return pmin[_order(reverse_p_value_order, False)]


def by(p_values: Union[List, ndarray]) -> ndarray:
    """
    by: Benjamini-Yekutieli

    The Benjamini and Yekutieli method controls the false discovery rate (FDR), the expected
    proportion of false discoveries amongst the rejected hypotheses. The FDR is a less stringent
    condition than the family-wise error rate (so bh is more powerful than many other correction
    methods).

    Parameters
    ----------
    p_values : Union[List[float], ndarray[float]]
        List or numpy array of p values to be converted into q values

    Returns
    -------
    ndarray[float]
        the q values for the respective p value inputs

    Examples
    --------
    >>> q_values = by([0.05, 0.002, 0.006])

    References
    ----------
    Benjamini and Yekutieli
        * The control of the false discovery rate in multiple testing under dependency.

    """

    n = len(p_values)
    cummin_input = zeros(n)
    reverse_p_value_order = _order(p_values, True)
    q = 0.0
    for i in range(1, n + 1):
        q += 1.0 / i
    for i in range(n):
        cummin_input[i] = q * (n / (n - i)) * p_values[reverse_p_value_order[i]]
    pmin = _pminf(_cumminf(cummin_input))
    return pmin[_order(reverse_p_value_order, False)]


def bonferonni(p_values: Union[List, ndarray]) -> ndarray:
    """
    bonferonni: Bonferonni

    Correction to control for family wise error rate (FWER).

    Recommended to use Hold instead of the uncorrected Bonferonni. Holm is more powerful and valid
    under the same assumption.

    Parameters
    ----------
    p_values : Union[List[float], ndarray[float]]
        List or numpy array of p values to be converted into q values

    Returns
    -------
    ndarray[float]
        the q values for the respective p value inputs

    Examples
    --------
    >>> q_values = bonferonni([0.05, 0.002, 0.006])

    References
    ----------
    Bonferroni
        * Teoria statistica delle classi e calcolo delle probabilità
    Shaffer
        * Multiple Hypothesis Testing

    """

    return clip(asarray(p_values)*len(p_values), 0.0, 1.0)


def holm(p_values: Union[List, ndarray]) -> ndarray:
    """
    holm: Holm

    Correction to control for family wise error rate (FWER).

    More powerful than unmodified Bonferonni and valid under the same assumption.

    Parameters
    ----------
    p_values : Union[List[float], ndarray[float]]
        List or numpy array of p values to be converted into q values

    Returns
    -------
    ndarray[float]
        the q values for the respective p value inputs

    Examples
    --------
    >>> q_values = holm([0.05, 0.002, 0.006])

    References
    ----------
    Holm
        * A simple sequentially rejective multiple test procedure

    """

    n = len(p_values)
    p_value_order = _order(p_values, False)
    cummax_input = zeros(n)
    for i in range(n):
        cummax_input[i] = (n - i) * p_values[p_value_order[i]]
    pmin = _pminf(_cummaxf(cummax_input))
    return pmin[_order(p_value_order, False)]


def hommel(p_values: Union[List, ndarray]) -> ndarray:
    """
    hommel: Hommel

    Correction to control for family wise error rate (FWER).

    Valid when the hypothesis tests are independent or when they are non-negatively associated
    (see Sarkar). Slightly more powerful than Hochberg but also slower.

    Parameters
    ----------
    p_values : Union[List[float], ndarray[float]]
        List or numpy array of p values to be converted into q values

    Returns
    -------
    ndarray[float]
        the q values for the respective p value inputs

    Examples
    --------
    >>> q_values = hommel([0.05, 0.002, 0.006])

    References
    ----------
    Hommel
        * A stagewise rejective multiple test procedure based on a modified Bonferroni test
    Sarkar
        * Some probability inequalities for ordered MTP2 random variables: a proof of Simes
          conjecture
        * The Simes method for multiple hypothesis testing with positively dependent test statistics

    """

    n = len(p_values)
    o = _order(p_values, False)
    p = [p_values[index] for index in o]

    pa, q = zeros(n), zeros(n)

    smin = n * p[0]
    for i in range(n):
        temp = n * p[i] / (i + 1)
        if temp < smin:
            smin = temp

    pa[:], q[:] = smin, smin

    for j in range(n - 1, 1, -1):

        ij = arange(1, n - j + 2) - 1
        i2 = zeros(j, dtype=int)

        for i in range(j):
            i2[i] = n - j + 2 + i - 1

        q1 = j * p[i2[0]] / 2.0
        for i in range(1, j - 1):

            TEMP_Q1 = j * p[i2[i]] / (2.0 + i)
            if TEMP_Q1 < q1:
                q1 = TEMP_Q1

        for i in range(n - j + 1):
            q[ij[i]] = min(j * p[ij[i]], q1)

        for i in range(j - 1):
            q[i2[i]] = q[n - j]

        for i in range(n):

            if pa[i] < q[i]:
                pa[i] = q[i]

    return pa[_order(o, False)]


def hochberg(p_values: Union[List, ndarray]) -> ndarray:
    """
    hochberg: Hochberg

    Correction to control for family wise error rate (FWER).

    Valid when the hypothesis tests are independent or when they are non-negatively associated
    (see Sarkar). Slightly less powerful than Hochberg but also faster.

    Parameters
    ----------
    p_values : Union[List[float], ndarray[float]]
        List or numpy array of p values to be converted into q values

    Returns
    -------
    ndarray[float]
        the q values for the respective p value inputs

    Examples
    --------
    >>> q_values = hochberg([0.05, 0.002, 0.006])

    References
    ----------
    Hochberg
        A sharper Bonferroni procedure for multiple tests of significance by
    Sarkar
        * Some probability inequalities for ordered MTP2 random variables: a proof of Simes
          conjecture
        * The Simes method for multiple hypothesis testing with positively dependent test statistics

    """

    n = len(p_values)
    reverse_p_values_order = _order(p_values, True)
    cummin_input = zeros(n)
    for i in range(n):
        cummin_input[i] = (i + 1) * p_values[reverse_p_values_order[i]]
    pmin = _pminf(_cumminf(cummin_input))
    return pmin[_order(reverse_p_values_order)]

"""
Frequetist tests

TODO: rely less on other packages and add hard coded tests
"""

import pytest
import numpy as np
from scipy.stats import (
    ttest_ind, ttest_1samp,
    norm, t, sem,
)
from statsmodels.stats.weightstats import ztest
from statsmodels.stats.proportion import proportions_ztest

from .test_cases.cases_freq import *

from lind.analysis.freq import (
    find_p_value, find_test_statistic, find_confidence_interval,
    one_samp_z_prop, two_samp_z_prop,
    one_samp_z, two_samp_z,
    one_samp_t, two_samp_t,
)

####################################################################################################


@pytest.mark.parametrize("df, tails", [
    (10, True),
    (10, False),
    (np.inf, True),
    (np.inf, False),
])
def test_find_test_statistic(df, tails):
    """
    """
    test_statistic_s = 1.96
    p_value = find_p_value(test_statistic_s, df, tails=tails)
    test_statistic = find_test_statistic(p_value, df, tails=tails)
    assert np.abs(test_statistic - test_statistic_s) <= 1e-10


@pytest.mark.parametrize("test_data", [
    data,
])
def test_find_confidence_interval(test_data):
    """
    """

    # z test case
    test_statistic, standard_error = one_samp_z(test_data)
    ci = find_confidence_interval(
        se=standard_error,
        df=np.inf,
        alpha=0.05,
        tails=True,
    )
    ci_s = norm.interval(
        alpha=0.95,
        loc=np.mean(test_data),
        scale=sem(test_data),
    )
    ci_s = ci_s[1] - np.mean(test_data)
    assert np.abs(ci - ci_s) <= 1e-10

    # student t test case
    test_statistic, standard_error, degrees_freedom = one_samp_t(test_data)
    ci = find_confidence_interval(
        se=standard_error,
        df=degrees_freedom,
        alpha=0.05,
        tails=True,
    )
    ci_s = t.interval(
        alpha=0.95,
        df=len(data) - 1,
        loc=np.mean(data),
        scale=sem(data)
    )
    ci_s = ci_s[1] - np.mean(test_data)
    assert np.abs(ci - ci_s) <= 1e-10

####################################################################################################
# One Sample Z Prop


@pytest.mark.parametrize("test1, test2, sample", [
    (one_samp_z_prop, proportions_ztest, oszp_data_a),
    (one_samp_z_prop, proportions_ztest, oszp_data_b),
    (one_samp_z_prop, proportions_ztest, oszp_data_c),
    (one_samp_z_prop, proportions_ztest, oszp_data_d),
    (one_samp_z_prop, proportions_ztest, oszp_data_e),
])
def test_one_sample_z_prop_test_validated(test1, test2, sample):
    """
    Check that the test outputs match validated results within an acceptable margin of error
    """

    test_statistic, standard_error = test1(
        sample=sample, null_h=0.0
    )
    p_value = find_p_value(
        test_statistic=test_statistic, df=np.inf, tails=True
    )

    test_statistic_s, p_value_s = test2(
        count=sample.sum(), nobs=sample.shape[0],
        value=0.0, alternative="two-sided", prop_var=False
    )

    assert np.abs(test_statistic - test_statistic_s) <= 1 * 10 ** (-2)
    assert np.abs(p_value - p_value_s) <= 1 * 10 ** (-2)

####################################################################################################
# One Sample Z


@pytest.mark.parametrize("test1, test2, sample", [
    (one_samp_z, ztest, osz_data_a),
    (one_samp_z, ztest, osz_data_b),
    (one_samp_z, ztest, osz_data_c),
    (one_samp_z, ztest, osz_data_d),
    (one_samp_z, ztest, osz_data_e),
])
def test_one_sample_z_test_validated(test1, test2, sample):
    """
    Check that the test outputs match validated results within an acceptable margin of error
    """

    test_statistic, standard_error = test1(
        sample=sample, null_h=0.0
    )
    p_value = find_p_value(
        test_statistic=test_statistic, df=np.inf, tails=True
    )

    test_statistic_s, p_value_s = test2(
        x1=sample, value=0.0
    )

    assert np.abs(test_statistic - test_statistic_s) <= 1 * 10 ** (-10)
    assert np.abs(p_value - p_value_s) <= 1 * 10 ** (-10)

####################################################################################################
# One Sample T


@pytest.mark.parametrize("test1, test2, sample", [
    (one_samp_t, ttest_1samp, ost_data_a),
    (one_samp_t, ttest_1samp, ost_data_b),
    (one_samp_t, ttest_1samp, ost_data_c),
    (one_samp_t, ttest_1samp, ost_data_d),
    (one_samp_t, ttest_1samp, ost_data_e),
])
def test_one_sample_t_test_validated(test1, test2, sample):
    """
    Check that the test outputs match validated results within an acceptable margin of error
    """

    test_statistic, standard_error, degrees_freedom = test1(
        sample=sample, null_h=0.0
    )
    p_value = find_p_value(
        test_statistic=test_statistic, df=degrees_freedom, tails=True
    )

    test_statistic_s, p_value_s = test2(
        a=sample, popmean=0.0
    )

    assert np.abs(test_statistic - test_statistic_s) <= 1 * 10 ** (-10)
    assert np.abs(p_value - p_value_s) <= 1 * 10 ** (-10)

####################################################################################################
# Two Sample Z Prop


@pytest.mark.parametrize("test1, test2, sample1, sample2, pooled", [
    (two_samp_z_prop, proportions_ztest, tszp_data_a[0], tszp_data_a[1], True),
    (two_samp_z_prop, proportions_ztest, tszp_data_a[0], tszp_data_a[1], False),
    (two_samp_z_prop, proportions_ztest, tszp_data_b[0], tszp_data_b[1], True),
    (two_samp_z_prop, proportions_ztest, tszp_data_b[0], tszp_data_b[1], False),
    (two_samp_z_prop, proportions_ztest, tszp_data_c[0], tszp_data_c[1], True),
    (two_samp_z_prop, proportions_ztest, tszp_data_d[0], tszp_data_d[1], True),
    (two_samp_z_prop, proportions_ztest, tszp_data_e[0], tszp_data_e[1], True),
    (two_samp_z_prop, proportions_ztest, tszp_data_e[0], tszp_data_e[1], False),
])
def test_two_sample_z_prop_test_validated(test1, test2, sample1, sample2, pooled):
    """
    Check that the test outputs match validated results within an acceptable margin of error
    """

    test_statistic, standard_error = test1(
        sample1=sample1, sample2=sample2, null_h=0.0, pooled=pooled
    )
    p_value = find_p_value(
        test_statistic=test_statistic, df=np.inf, tails=True
    )

    test_statistic_s, p_value_s = test2(
        count=[sample1.sum(), sample2.sum()], nobs=[sample1.shape[0], sample2.shape[0]],
        value=0.0, alternative="two-sided", prop_var=False
    )

    if pooled is True:
        assert np.abs(test_statistic - test_statistic_s) <= 1 * 10 ** (-10)
        assert np.abs(p_value - p_value_s) <= 1 * 10 ** (-10)
    else:
        assert np.round(np.abs(p_value - p_value_s), 2) <= 1 * 10 ** (-2)
        assert p_value < p_value_s  # unpooled p-values consistently skew lower

####################################################################################################
# Two Sample Z


@pytest.mark.parametrize("test1, test2, sample1, sample2, pooled", [
    (two_samp_z, ztest, tsz_data_a[0], tsz_data_a[1], True),
    (two_samp_z, ztest, tsz_data_a[0], tsz_data_a[1], False),
    (two_samp_z, ztest, tsz_data_b[0], tsz_data_b[1], True),
    (two_samp_z, ztest, tsz_data_b[0], tsz_data_b[1], False),
    (two_samp_z, ztest, tsz_data_c[0], tsz_data_c[1], True),
    (two_samp_z, ztest, tsz_data_d[0], tsz_data_d[1], True),
    (two_samp_z, ztest, tsz_data_d[0], tsz_data_d[1], False),
])
def test_two_sample_z_test_validated(test1, test2, sample1, sample2, pooled):
    """
    Check that the test outputs match validated results within an acceptable margin of error
    """

    test_statistic, standard_error = test1(
        sample1=sample1, sample2=sample2, null_h=0.0, pooled=pooled
    )
    p_value = find_p_value(
        test_statistic=test_statistic, df=np.inf, tails=True
    )

    test_statistic_s, p_value_s = test2(
        x1=sample1, x2=sample2, value=0.0, usevar="pooled", alternative="two-sided"
    )

    if pooled is True:
        assert np.abs(test_statistic - test_statistic_s) <= 1*10**(-10)
        assert np.abs(p_value - p_value_s) <= 1 * 10 ** (-10)
    else:
        assert np.round(np.abs(p_value - p_value_s), 2) <= 1*10**(-2)
        assert p_value < p_value_s  # unpooled p-values consistently skew lower

####################################################################################################
# Two Sample T


@pytest.mark.parametrize("test1, test2, sample1, sample2, pooled", [
    (two_samp_t, ttest_ind, tst_data_a[0], tst_data_a[1], True),
    (two_samp_t, ttest_ind, tst_data_a[0], tst_data_a[1], False),
    (two_samp_t, ttest_ind, tst_data_b[0], tst_data_b[1], True),
    (two_samp_t, ttest_ind, tst_data_b[0], tst_data_b[1], False),
    (two_samp_t, ttest_ind, tst_data_c[0], tst_data_c[1], True),
    (two_samp_t, ttest_ind, tst_data_c[0], tst_data_c[1], False),
    (two_samp_t, ttest_ind, tst_data_d[0], tst_data_d[1], True),
    (two_samp_t, ttest_ind, tst_data_d[0], tst_data_d[1], False),
    (two_samp_t, ttest_ind, tst_data_e[0], tst_data_d[1], True),
    (two_samp_t, ttest_ind, tst_data_e[0], tst_data_d[1], False),
])
def test_two_sample_t_test_validated(test1, test2, sample1, sample2, pooled):
    """
    Check that the test outputs match validated results within an acceptable margin of error
    """

    test_statistic, standard_error, degrees_freedom = test1(
        sample1=sample1, sample2=sample2, null_h=0.0, pooled=pooled
    )
    p_value = find_p_value(
        test_statistic=test_statistic, df=degrees_freedom, tails=True
    )

    test_statistic_s, p_value_s = test2(
        a=sample1, b=sample2, equal_var=pooled
    )

    assert np.abs(test_statistic - test_statistic_s) <= 1*10**(-10)
    assert np.abs(p_value - p_value_s) <= 1 * 10 ** (-10)


if __name__ == '__main__':
    pytest.main(__file__)

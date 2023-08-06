"""
factorial module tests
"""

from numpy import any

import pytest
from pandas.util.testing import assert_frame_equal

from lind.design.factorial import design_full_factorial, design_partial_factorial, \
    fetch_partial_factorial_design
from lind._utilities import _check_balanced, _check_orthogonal
from ._validated_partial_factorial_designs import *

####################################################################################################


@pytest.mark.parametrize("factors, factor_names, expected_output", [
    ([[-1, 1], [-1, 1], [-1, 1]], ["factor_one", "factor_two", "factor_three"],
     pd.DataFrame({
        'factor_one': {0: -1, 1: -1, 2: -1, 3: -1, 4: 1, 5: 1, 6: 1, 7: 1},
        'factor_two': {0: -1, 1: -1, 2: 1, 3: 1, 4: -1, 5: -1, 6: 1, 7: 1},
        'factor_three': {0: -1, 1: 1, 2: -1, 3: 1, 4: -1, 5: 1, 6: -1, 7: 1}
    })),
    ([[-1, 0, 1], ["high", "low"], [-1, 0, 1, 2]], ["factor_one", "factor_two", "factor_three"],
     pd.DataFrame({
        'factor_one': {0: -1, 1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: 0, 9: 0, 10: 0,
                       11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1,
                       22: 1, 23: 1},
        'factor_two': {0: 'high', 1: 'high', 2: 'high', 3: 'high', 4: 'low', 5: 'low', 6: 'low',
                       7: 'low', 8: 'high', 9: 'high', 10: 'high', 11: 'high', 12: 'low', 13: 'low',
                       14: 'low', 15: 'low', 16: 'high', 17: 'high', 18: 'high', 19: 'high',
                       20: 'low', 21: 'low', 22: 'low', 23: 'low'},
        'factor_three': {0: -1, 1: 0, 2: 1, 3: 2, 4: -1, 5: 0, 6: 1, 7: 2, 8: -1, 9: 0, 10: 1,
                         11: 2, 12: -1, 13: 0, 14: 1, 15: 2, 16: -1, 17: 0, 18: 1, 19: 2, 20: -1,
                         21: 0, 22: 1, 23: 2}
     }))
    ])
def test_design_full_factorial_expected(factors, factor_names, expected_output):
    """
    test_design_full_factorial expected

    Check that the proper full factorial designs are returned.
    """

    assert_frame_equal(
        design_full_factorial(factors, factor_names),
        expected_output
    )


def test_design_full_factorial_value_error():
    """
    test_design_full_factorial value error

    Make sure an exception is thrown if the input lengths do not match.
    """

    with pytest.raises(Exception) as execinfo:
        design_full_factorial(
            factors=[[0, 1], [0, 1], [0, 1]],
            factor_names=["Factor_One", "Factor_Two"]
        )

    assert str(execinfo.value) == "The length of factor_names must match the length of factors."


####################################################################################################

@pytest.mark.parametrize("k, res, validated_design", [
    (3, 3, design_2_3_1),
    (4, 4, design_2_4_1),
    (5, 5, design_2_5_1),
    (5, 3, design_2_5_2),
    (6, 6, design_2_6_1),
])
def test_design_partial_factorial_validated_designs(k, res, validated_design):
    """
    design_partial_factorial validated designs

    Ensure that this function returns partial factorial designs verified by trusted sources.
    """
    columns = validated_design.columns.tolist()
    assert_frame_equal(
        design_partial_factorial(k=k, res=res).sort_values(columns).reset_index(drop=True),
        validated_design.sort_values(columns).reset_index(drop=True)
    )


@pytest.mark.parametrize("k, res", [
    (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
    (13, 1), (13, 2), (13, 3), (13, 7), (13, 11), (13, 12), (13, 13),
])
def test_design_partial_factorial_orthogonal(k, res):
    """
    design_partial_factorial orthogonal

    Ensure that this function returns orthogonal designs.
    """

    arr = design_partial_factorial(k=k, res=res).values
    assert _check_balanced(arr), "Array not balanced."
    assert _check_orthogonal(arr), "Array not orthogonal."


####################################################################################################


@pytest.mark.parametrize("design", ["2**3-1", "2**5-2", "2**7-3", "2**15-11"])
def test_fetch_partial_factorial_design_orthogonal(design):
    """
    fetch_partial_factorial_design orthogonal

    Ensure that this function returns orthogonal designs. These designs are validated by trusted
    sources, but my motto is "trust but verify".
    """

    arr = fetch_partial_factorial_design(design).values
    assert _check_balanced(arr), "Array not balanced."
    assert _check_orthogonal(arr), "Array not orthogonal."


def test_fetch_partial_factorial_design_value_error():
    """
    fetch_partial_factorial_design value error

    Make sure an exception is thrown if an invalid design is requested.
    """

    with pytest.raises(Exception) as execinfo:
        fetch_partial_factorial_design("fake design")

    assert "Please input a valid design. `fake design` not found." in str(execinfo.value)


if __name__ == '__main__':
    pytest.main(__file__)
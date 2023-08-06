"""
plackett_burman module tests
"""

import pytest

from lind.design.box_wilson import design_box_wilson
from lind._utilities import _check_orthogonal, _check_balanced

####################################################################################################


@pytest.mark.parametrize("num_factors", [i for i in range(2, 10)])
@pytest.mark.parametrize("alpha_design", ["orthogonal", "rotatable"])
@pytest.mark.parametrize("center", [(1, 1), (4, 4)])
@pytest.mark.parametrize("face_design", ["CCC", "CCF", "CCI"])
def test_design_box_wilson_orthogonal(num_factors, alpha_design, center, face_design):
    """
    design_box_wilson orthogonal

    Ensure that this function returns orthogonal designs.
    """

    # close enough to orthogonal
    atol = 0.0 if face_design != "CCI" else 1e-13

    arr = design_box_wilson(
        k=num_factors,
        alpha_design=alpha_design,
        center=center,
        face_design=face_design
    ).values
    assert _check_balanced(arr, atol=atol), "Array not balanced."
    assert _check_orthogonal(arr, atol=atol), "Array not orthogonal."


@pytest.mark.parametrize("num_factors, alpha_design, face_design", [
    (8, "bad input", "ccf"),
    ("bad input", "orthogonal", "ccf"),
    (8, "orthogonal", "bad input"),
    (1, "orthogonal", "ccf")
])
def test_design_box_wilson_value_error(num_factors, alpha_design, face_design):
    """
    design_box_wilson value error

    Make sure an exception is thrown if the input lengths do not match. While we want to provide
    informative errors for some input errors, we don't want to babysit the user. Therefore we
    don't enforce type checking for the input `center`.
    """

    with pytest.raises(Exception) as execinfo:
        design_box_wilson(
            k=num_factors,
            alpha_design=alpha_design,
            center=(1, 1),
            face_design=face_design
        )

    assert "bad input" in str(execinfo.value) or \
           "Input k must be an integer." in str(execinfo.value) or \
           "Input k must be >= 2 to produce a valid design." in str(execinfo.value)


if __name__ == '__main__':
    pytest.main(__file__)
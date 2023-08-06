"""
utilities: common utilities used throughout the code base
"""

import logging
from typing import List, Optional

from numpy import fill_diagonal, dot, eye, allclose, ndarray, zeros

# set logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _backend_warning():
    """
    Convenience function for issuing warnings for backend modules.
    """
    logging.warning("All code in r_backends is merely a python wrapper over "
                    "existing DOE packages in R. Code quality and validation "
                    "supported by underlying R packages.")


def _check_int_input(var, input_name: str) -> int:
    """
    _check_int_input

    Convenience function to check if an input is an int (or a float coercable into an int without
    rounding). If the input is not of the expected types it will raise a helpful value error.

    Parameters
    ----------
    var
        the input variable to check
    input_name : str
        the name of the variable to include if an error is raised

    Returns
    -------
    int
        the input variable coerced into an int
    """

    if not isinstance(var, int) and (
            not isinstance(var, float) or not var.is_integer()):
        raise ValueError("Input {} must be an integer.".format(input_name))

    return int(var)


def _check_str_input(var, input_name: str, valid_options: Optional[List[str]] = None) -> str:
    """
    _check_str_input

    Convenience function to check if an input is a string. If argument valid_options is given, this
    function will also check that var is a valid option from the valid_options specified.

    Parameters
    ----------
    var
        the input variable to check
    input_name : str
        the name of the variable to include if an error is raised
    valid_options: List[str], optional
        a list of valid options for var

    Returns
    -------
    str
        the input var after lowering ans stripping the string
    """

    if not isinstance(var, str):
        raise ValueError("Invalid input {0} for {1}. Input {1} must be a string.".format(
            var, input_name))

    var = var.strip().lower()

    if valid_options is not None:
        valid_options = [option.strip().lower() for option in valid_options]
        if var not in valid_options:
            raise ValueError("Invalid input {0} for {1}. Input {1} must be one of the following "
                             "options: {2}.".format(var, input_name, valid_options))

    return var


def _check_balanced(arr: ndarray, rtol: float = 1e-07, atol: float = 0.0) -> bool:
    """

    Parameters
    ----------
    arr
    rtol
    atol

    Returns
    -------

    """
    col_sums = arr.sum(axis=0).astype(float)
    return allclose(
        col_sums, zeros(col_sums.shape[0], dtype=float),
        rtol=rtol, atol=atol
    )


def _check_orthogonal(arr: ndarray, rtol: float = 1e-07, atol: float = 0.0) -> bool:
    """

    Parameters
    ----------
    arr : np.ndarray
        an array to check for orthogonality
    rtol :
    atol

    Returns
    -------
    bool
        returns True if orthogonal withing specified tolerances, returns False if not orthogonal
    """
    product = dot(arr.T, arr)
    fill_diagonal(product, 1.0)
    return allclose(
        product.astype(float), eye(arr.shape[1], dtype=float),
        rtol=rtol, atol=atol
    )

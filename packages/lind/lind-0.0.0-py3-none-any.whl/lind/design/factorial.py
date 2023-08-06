"""
factorial: This module contains tools for designing factorial experiments. Full factorial
experiments (where every combination of treatments is explored) and partial factorial (where only a
fraction of combinations are explored). Partial factorial experiments are sometimes referred to as
fractional factorial experiments.

The factorial designs here are meant to yield balanced and orthogonal designs. An experimental
design is orthogonal if the effects of any factor (i.e. factor A) balance out (sum to zero) across
the effects of the other factors (i.e. factors B and C). In other words, if A is orthogonal to B
and C, then the measurement of factors B and C will not be biased by the effect size fo A. A
balanced design assumes equal sample sizes across att cohorts / test cells.

One quick check of orthogonality for a 2 level design is to take the sum of the columns of the
design. They should all sum to 0. See below:
>>> design_partial_factorial(factors=6, res=4).sum(axis=0)

If possible, all combinations (rows) in these designs should be run in a random order, or in
parallel using proper randomization of cohort assignment.

Recommended import style:
>>> from lind.design import factorial

"""

import logging
from typing import Union, List, Optional

from itertools import product, combinations
from fractions import Fraction

from numpy import full, arange, vectorize, ndarray, array_str, asarray
from scipy.special import binom

from pandas import DataFrame, read_csv
from patsy import dmatrix  # pylint: disable=no-name-in-module

from lind._utilities import _check_int_input
from lind import _sfap

# set logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define public functions (ignored by jupyter notebooks)
__all__ = [
    'design_full_factorial',
    'design_partial_factorial',
    'fetch_partial_factorial_design'
]

####################################################################################################


def _array_to_string(arr_like: Union[List, ndarray]) -> ndarray:
    """Utility for converting experiment design string into an array of factors"""
    return array_str(asarray(arr_like)).replace("[", "").replace("]", "")


def _k_combo(k: int, res: int) -> int:
    """The number of combinations of k factors given a specific resolution"""
    return binom(
        full(k - res + 1, k),
        arange(res - 1, k, 1)
    ).sum() + k


_k_combo_vec = vectorize(_k_combo, excluded=['res'],
                         doc="The number of combinations of k factors given a specific resolution")


####################################################################################################


def design_full_factorial(factors: List[List],
                          factor_names: Optional[List[str]] = None) -> DataFrame:
    """
    design_full_factorial

    This function helps create a full factorial experiment design. Given how easy it is to design a
    full factorial experiment once the factors and levels have been specified, this is more of a
    convenience function.

    Parameters
    ----------
    factors : List[List]
        a list of lists representing factors and levels
    factor_names : List[str], optional
        a list of names for the factors in the first argument. Must share the order of the first
        argument.

    Returns
    -------
    pd.DataFrame

    Examples
    --------
    >>> # create full factorial design for a 2 level 3 factor experiment
    >>> design_df = design_full_factorial(factors=[[-1, 1], [-1,1], [-1, 1]],
    >>>     factor_names=["factor_one", "factor_two", "factor_three"])

    """

    assert factor_names is None or len(factor_names) == len(factors), \
        "The length of factor_names must match the length of factors."
    factor_names = factor_names if factor_names is not None else \
        ["x{}".format(i) for i in range(len(factors))]
    return DataFrame(data=list(product(*factors)), columns=factor_names)


def design_partial_factorial(k: int, res: int) -> DataFrame:
    """
    design_partial_factorial

    This function helps design 2 level partial factorial experiments. These experiments are often
    described using the syntax l**(k-p) where l represents the level of each factor, k represents
    the total number of factors considered, and p represents a scaling factor relative to the full
    factorial design.

    This function assumes that l=2. Users are not asked to set p, instead the user sets a minimum
    desired resolution for their experiment. Resolution describes the kind of aliasing incurred by
    scaling down from a full to a partial factorial design. Higher resolutions have less potential
    aliasing (confounding).

    Resolution number is determined through the defining relation of the partial factorial design.
    For the 6 factor design 2**(6-p) with factors ABCDEF, example defining relations (I) are shown
    below. The resolution cannot exceed the number of factors in the experiment. So a 6 factor
    experiment can be at most a resolution 6 (otherwise it would be a full factorial experiment).

        * Res I: I = A
        * Res II: I = AB
        * Res III: I = ABC
        * Res IV: I = ABCD
        * Res V: I = ABCDE
        * Res VI: I = ABCDEF

    Practically we tend to use resolution III-, IV- and V-designs.

        * Res I: Cannot distinguish between levels within main effects (not useful).
        * Res II: Main effects may be aliased with other main effects (not useful).
        * Res III: Main effects may be aliased with two-way interactions.
        * Res IV: Two-way interactions may be aliased with each other.
        * Res V: Two-way interactions may be aliased with three-way interactions.
        * Res VI: Three-way interactions may be aliased with each other.

    Parameters
    ----------
    k : int
        the total number of factors considered in the experiment
    res : int
        the desired minimum resolution of the experiment

    Returns
    -------
    pd.DataFrame
        A dataframe with the partial factorial design

    Examples
    --------
    >>> # create partial factorial design for a 2 level 4 factor resolution III experiment
    >>> design_df = design_partial_factorial(k=4, res=3)

    """

    _check_int_input(k, "k")
    _check_int_input(res, "res")
    assert res <= k, "Resolution must be smaller than or equal to the number of factors."

    # Assume l=2 and use k specified by user to solve for p in design
    n = arange(res - 1, k, 1)
    k_minus_p = k - 1 if res == k else n[~(_k_combo_vec(n, res) < k)][0]

    logging.info("Partial Factorial Design: l=2, k={}, p={}".format(k, k - k_minus_p))
    logging.info("Ratio to Full Factorial Design: {}".format(Fraction(2**k_minus_p / 2**k)))

    # identify the main effects and interactions for the design

    main_factors = arange(k_minus_p)
    clean = lambda x: x.replace("  ", " ").strip(" ").replace(" ", ":")
    interactions = [clean(_array_to_string(main_factors))] if res == k else \
        [
            clean(_array_to_string(c))
            for r in range(res - 1, k_minus_p)
            for c in combinations(main_factors, r)
        ][:k - k_minus_p]

    # combine main effects and interactions into a single design string (format inspired by patsy)
    factors = " ".join([_array_to_string(main_factors)] + interactions)
    logging.info("Design string: {}".format(factors))

    main_factors = [i for i in factors.split(" ") if i and ":" not in i]
    two_level_full_factorial = [[-1, 1] for _ in main_factors]
    full_factorial_design = design_full_factorial(two_level_full_factorial)

    interactions = [
        ["x" + i for i in j.split(":")]
        for j in [i for i in factors.split(" ") if i and ":" in i]
    ]

    design = "+".join(full_factorial_design.columns.tolist() + [":".join(i) for i in interactions])
    partial_factorial_design = dmatrix(design, full_factorial_design, return_type='dataframe').drop(
        columns=["Intercept"], axis=1)

    partial_factorial_design.columns = \
        ["x{}".format(i) for i in range(partial_factorial_design.shape[1])]

    return partial_factorial_design


####################################################################################################


def fetch_partial_factorial_design(design_name: str = "toc") -> DataFrame:
    """
    fetch_partial_factorial_design

    The function design_partial_factorial auto generates partial factorial designs using an
    algorithm. We validate that algorithm in our unit tests by comparing against known designs
    from popular experimental design textbooks. For those that want to use the designs from
    these books rather than the auto-generated designs, please use thos function.

    There are multiple ways to generate certain designs given a fixed k and p
    (using formula l**k-p). Both fetch_partial_factorial_design and design_partial_factorial
    deterministically return designs, but there are typically other ways to formulate these designs
    if the user would like to work it out on their own.

    Parameters
    ----------
    design_name : str
        the name of the design to fetch; to see available designs input `toc`

    Returns
    -------
    pd.DataFrame
        experiment design or toc of available designs

    Examples
    --------
    >>> table_of_contents_of_designs = fetch_partial_factorial_design("toc")
    >>> design = fetch_partial_factorial_design("2**3-1")

    References
    ----------
    NIST
        * Section 5.3.3.4.7 of the Engineering Statistics Handbook
    Box, Hunter, & Hunter
        * Statistics For Experimentors
    Taguchi
        * Systems Of Experimental Design, VOL. 2

    Notes
    -----
    * 2**3-1 is equivalent to a Taguchi L4 design
    * 2**15-11 is equivalent to a Taguchi L16 design
    * 2**31-26 is equivalent to a Taguchi L32 design

    """

    assert isinstance(design_name, str), "Input design_name must be a string."
    design_name = design_name.lower().strip() + ".csv"
    if _sfap is None:
        raise Exception("Missing dependency lind-static-resources")
    try:
        return read_csv(_sfap+"/factorial/"+design_name, index_col=0)
    except FileNotFoundError as exception:
        logging.error(exception)
        raise ValueError("Please input a valid design. `{}` not found. "
                         "See docstring for help.".format(design_name[:-4]))

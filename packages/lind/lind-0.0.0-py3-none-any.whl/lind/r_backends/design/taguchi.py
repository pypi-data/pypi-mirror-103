"""
taguchi: Utilities for using the Taguchi method of experimental design.


Developer Note: One of the reasons for including R backends in this package is to make existing DOE
packages available to python users. Howerver, many of these R packages use custom R classes instead
of R dataframes. Rather than translating these classes into R dataframes and then converting to
pandas dataframes, I opted to print the class. Its a quick and dirty interim solution.

"""

import logging

from rpy2.robjects import r
from rpy2.robjects.packages import importr

# set logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define public functions (ignored by jupyter notebooks)
__all__ = ["taguchi_choose", "taguchi_design"]

####################################################################################################


_r_taguchiChoose = importr("qualityTools").taguchiChoose


def taguchi_choose(factor_type_a: int = 0, factor_level_a: int = 0,
                   factor_type_b: int = 0, factor_level_b: int = 0,
                   num_interactions: int = 0) -> None:
    """
    taguchi_choose

    Prints a recommended Taguchi design (orthogonal array) based on the inputes. The function
    taguchi_design can be used to see the recommended design.

    Parameters
    ----------
    factor_type_a: int
        the level of factor group a; should be >= 2
    factor_level_a: int
        the number of factors in factor group a; should be >= 2
    factor_type_b: int
        the level of factor group b; should be >= 2
    factor_level_b: int
        the number of factors in factor group b; should be >= 2
    num_interactions: int
        the number of interactions across the factor groups

    Returns
    -------
    None
        nothing is returned

    Examples
    --------
    >>> taguchi_choose(
    >>>     factor_type_a = 2, factor_level_a = 3,
    >>>     factor_type_b = 0, factor_level_b = 0,
    >>>     num_interactions = 1)

    """

    _r_taguchiChoose(
        factors1=factor_type_a,
        factors2=factor_type_b,
        level1=factor_level_a,
        level2=factor_level_b,
        ia=num_interactions
    )


def taguchi_design(design: str = "L4_2") -> None:
    """
    taguchi_design

    Prints out the details of the recommended Taguchi design.

    Parameters
    ----------
    design: str
        a string defining the name of the taguchi orthogonal array of interest

    Returns
    -------
    None
        nothing is returned

    Examples
    --------
    >>> taguchi_design(design = "L4_2")

    """

    # design <- taguchiDesign("L4_2") # returns an S4 class
    # slotNames(design)
    # design <- slot(design, "design") # returns a list

    cmd = "print(taguchiDesign('{}'))".format(design)
    r(cmd)

"""
plackett_burman: This module contains tools for designing Plackett-Burman experiments.

Plackett and Burman generated sets of useful 2 level experimental designs using a method Raymond
Paley identified in 1933. This method generated orthogonal matrices with elements (1, -1). Paley's
method could be used to find such matrices of size N for most N equal to a multiple of 4
(all such N up to 100 except N = 92). This gave Plackett and Burman the interesting quality that
they only increase the number of rows (require runs) in the experiment for every 4 factors added to
the design.

Plackett and Burman are structured so that each combination of levels for any pair of factors
appears the same number of times, throughout all the experimental runs.

These designs achieved orthogonality with many fewer runs than a full factorial design. When N is
a power of 2 then a Plackett and Burman design is equivalent to a partial factorial resolution III
design. All Plackett and Burman designs assume negligible interaction effects relative to main
effects.

Plackett and Burman do mention designs with more then 2 levels (a rediscovery of methods invented
by Raj Chandra Bose and K. Kishen), however these are rarely used in practice.

Recommended import style:
>>> from lind.design import plackett_burman as pb

"""

import logging

from pandas import DataFrame, read_csv

from lind._utilities import _check_int_input
from lind import _sfap

# set logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define public functions (ignored by jupyter notebooks)
__all__ = ["fetch_plackett_burman_design"]


####################################################################################################


def fetch_plackett_burman_design(num_factors: int) -> DataFrame:
    """
    fetch_plackett_burman_design

    This function helps create Plackett-Burman experimental designs. Plackett-Burman designs are
    very efficient screening designs when only main effects are of interest.

    Parameters
    ----------
    num_factors : int
        the number of factors in the design. Currently only supports up to 47 factors per design.

    Returns
    -------
    pd.DataFrame
        experiment design or toc of available designs

    Examples
    --------
    >>> design = fetch_plackett_burman_design(7)

    References
    ----------
    NIST
        * Section 5.3.3.5 of the Engineering Statistics Handbook
    Plackett and Burman
        * The Design of Optimum Multifactorial Experiments

    """

    _check_int_input(num_factors, "num_factors")
    if num_factors > 47:
        raise ValueError("This function currently does not support designs with greater than "
                         "47 factors.")

    num_factors = int(num_factors)
    design_name = str(4 * (1+num_factors//4)) + ".csv"
    if _sfap is None:
        raise Exception("Missing dependency lind-static-resources")
    return read_csv(_sfap+"/plackett_burman/"+design_name, header=0, index_col=0,
                    names=["x{}".format(i) for i in range(4 * (1+num_factors//4))]
                    ).iloc[:, :num_factors]

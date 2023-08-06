"""
taguchi: Taguchi experiments are quick and dirt designs that are effective for quality control in
engineering. Some experimenters use Taguchi Method designs as screening experiments in a similar
manner to Plackett Burman designs. They are useful designs in quality control but due to recent fads
in marketing are often misapplied in other fields. Taguchi methods were some of the first
`Robust Parameter Designs`.

The Taguchi Method is a multi-step process for producing a design. To fully understand the process
see the reources mentioned below. We provide a quick overview here: First split your factors into
A) inner array factors (factors you control) and B) outer array factors (environmental factors out
of your control). The function `recommend_inner_array` will help identify an orthogonal array
to use as your design base. Once you know which array you want to use as your base, the function
`fetch_inner_array` will retrieve that array. If there are non-trivial interactions you need to
model in your inner array, you may need to censor certain columns before proceeding. Finally,
append the outer array to your inner array using the function `append_outer_array`.

An example workflow is shown below.

Unlike traditional factorial designs like those in the module `lind.design/factorial`, Taguchi
designs rely heavily on pre-experiment judgement. This is often useful in quality control, but can
introduce dangerous assumptions in other fields. Taguchi's method builds on the theory of fractional
factorial designs, depending on the experiment requirements, either methodology may be more
efficient and/or less biased. It is up to the experimenter to understand when to use each method.

Workflow Example
-----------------
>>> # find the appropriate orthogonal array to build inner array of experiment design
>>> print(
>>>     recommend_inner_array(
>>>         levels_group_a=2,
>>>         num_factors_group_a=2,
>>>         interactions_group_a=1,
>>>         measured_moments=1
>>> )) # shows applicable designs
>>> # fetch pandas data frame for inner array
>>> inner_array = fetch_inner_array(design_file_name="L4_2_3")
>>> # print taguchi line graph of inner array interactions
>>> interaction_diagrams("L4_2_3")
>>> # censor columns for interactions assumed to be significant
>>> inner_array = inner_array.drop(columns=["C (A:B)"])
>>> # append noise factors (outer array) to produce full experiment design
>>> experiment_design = append_outer_array(inner_array,
>>>                                        noise_factors=[[-1, 1], [-1, 0, 1], [3.4, 6.7, 1.9]])

References
----------
Taguchi, Chowdhury, and Wu
    * Taguchi's Quality Engineering Handbook (Appendix C)
Experiment Design and Analysis Reference (reliawiki)
    * Experiment Design and Analysis Reference (Appendix D)

"""

import logging
from typing import Optional, List

from pandas import DataFrame, read_csv

from lind.design.factorial import design_full_factorial as _dff
from lind.design import _taguchi_line_diagrams as _tld
from lind import _sfap

# set logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define public functions (ignored by jupyter notebooks)
__all__ = [
    "recommend_inner_array",
    "fetch_inner_array",
    "append_outer_array",
    "interaction_diagrams"
]


####################################################################################################


def recommend_inner_array(levels_group_a: int = 0, num_factors_group_a: int = 0,
                          levels_group_b: int = 0, num_factors_group_b: int = 0,
                          interactions_group_a: int = 0,
                          interactions_group_b: int = 0,
                          measured_moments: int = 1) -> DataFrame:
    """
    recommend_inner_array

    It is sometimes difficult to know which orthogonal array to use when defining the inner array
    of a Taguchi experiment. This function can help narrow down the appropriate choices available
    to an experimenter. The experimenter will often want to choose the design with the fewest
    number of runs, but that may not always be the case.

    If all arguments are left at default values then the function will return all supported
    Taguchi designs. See module docstring for references and examples.

    Parameters
    ----------
    levels_group_a: int, optional

    num_factors_group_a: int, optional
    levels_group_b: int, optional
    num_factors_group_b: int, optional
    interactions_group_a: int, optional
    interactions_group_b: int, optional
    measured_moments: int, optional

    Returns
    -------
    pd.DataFrame
        A data frame describing the available designs that meet the user's criteria; if the data
        frame is empty then no Taguchi orthogonal arrays meet the user's specification
    """

    if _sfap is None:
        raise Exception("Missing dependency lind-static-resources")

    toc = read_csv(_sfap + "/taguchi/taguchi_toc.csv", header=0)
    toc = toc[["design_array_name", "design_file_name", "num_runs", "2", "3", "4", "5", "6"]]
    toc = toc.dropna()

    if num_factors_group_a == 0:
        return toc

    assert levels_group_a >= 2 and num_factors_group_a >= 2
    assert levels_group_b >= 2 or num_factors_group_b == 0

    # dev note: should we log the degrees of freedom?
    # total number of experiments is lower bounded by dof of experiment
    # dof_a = (levels_group_a-1) * num_factors_group_a + interactions_group_a + (measured_moments-1)
    # dof_b = (levels_group_b-1) * num_factors_group_b + interactions_group_b

    toc = toc[toc[str(levels_group_a)] >= num_factors_group_a + interactions_group_a +
              (measured_moments - 1)]
    if num_factors_group_b != 0:
        toc = toc[toc[str(levels_group_b)] >= num_factors_group_b + interactions_group_b]

    return toc


def fetch_inner_array(design_file_name: Optional[str] = None) -> DataFrame:
    """
    fetch_inner_array

    The inner array of a Taguchi design is often just a fractional factorial design very similar
    to more traditional Fisher factorial designs. These are represented by orthogonal arrays that
    are then censored used the experimenter's prior judgement about factor interactions.

    See module docstring for references and examples.

    Parameters
    ----------
    design_file_name: str, optional
        the name of the design / design file name that the experimenter wants to use for the inner
        array of their design

    Returns
    -------
    pd.DataFrame
        a data frame representing the orthogonal array of interest; users may need to censor
        columns in this array to represent prior knowledge about number of factors or number of
        significant interactions
    """

    if _sfap is None:
        raise Exception("Missing dependency lind-static-resources")

    design_file_name = design_file_name + ".csv" if design_file_name is not None \
        else "taguchi_toc.csv"
    return read_csv(_sfap + "/taguchi/" + design_file_name, header=0)


def append_outer_array(inner_array: DataFrame, noise_factors: List[List],
                       noise_factor_names: Optional[List[str]] = None) -> DataFrame:
    """
    append_outer_array

    The outer array of a Taguchi design represents the noise factors that the designer wants to
    control for with respect to the inner array. The outer array represents mini-full factorial
    designs each centered at the individual runs in the inner array. This helps provide data that
    is "robust" to the levels of the noise factors.

    See module docstring for references and examples.

    Parameters
    ----------
    inner_array: pd.DataFrame
        a dataframe representing the inner array of the Taguchi design
    noise_factors: List[List]
        a list of lists representing the noise factors and levels
    noise_factor_names: List[str], optional
        a list of names for the factors in the first argument. Must share the order of the first
        argument.

    Returns
    -------
    pd.DataFrame
        a combination of the inner and outer arrays representing the full taguchi design; uses the
        same format as all factorial designs in this package as opposed to more traditional
        Taguchi design display formats
    """

    outer_array = _dff(
        factors=noise_factors,
        factor_names=noise_factor_names
    )

    return inner_array.assign(key=0).merge(outer_array.assign(key=0), how='left', on='key').drop(
        columns=["key"])


####################################################################################################


def interaction_diagrams(design_name: str, save_path: Optional[str] = None,
                         file_name: Optional[str] = None) -> None:
    """
    interaction_diagrams

    Line diagrams are vidual aids used by Taguchi to show assumptions about factor interactions
    that could be using for adapting the design of the inner array.

    See module docstring for references and examples.

    Parameters
    ----------
    design_name: str
        the name of the Taguchi design assocaited with the line graph(s); i.e. `L4_2_3`
    save_path: str, optional
        the name to use when saving the png of the line graph; should be an absolute path
    file_name: str, optional
        the name to use when saving the png of the line graph; if multiple line graphs are saved a
        number will be appended to the end of the name

    Returns
    -------
    None
        does not return anything

    """

    _tld.plot_line_graph(
        design_name=design_name,
        save_path=save_path,
        file_name=file_name
    )

"""
box_wilson: Box-Wilson experiment designs, sometimes referred to as Central-Composite Designs
(CCDs), are useful for measuring quadratic effects.

Linear effects are typically measured using 2 level factorial or 2 level Plackett-Burman
experiments. However, if the relationship between treatments and response are quadratic, more than
2 levels may be required to accurately represent the response surface of the experiment.

CCDs allow experimenters to model quadratic response surfaces without implementing full 3 level
factorial experiments. CCD designs consist of three "runs": A) a factorial experiment (sometimes
fractional in design) B) a set of center points, experimental runs whose values of each factor are
the medians of the values used in the factorial portion C) a set of axial points, experimental runs
identical to the centre points except for one factor, which will take on values both below and
above the median of the two factorial levels.

| A) corner points (defined by the factorial design or matrix_f)
| B) center points (defined by the matrix_c)
| C) axial points (defined by the matrix_e)

Axial points are sometimes referred to as star points.

If the distance from the center of the design space to a factorial point is 1 unit for each
factor, the distance from the center of the design space to a star point is |alpha| > 1. The
precise value of alpha depends on the variables center, alpha_design, and face_design.

In rare cases (i.e. k=2) a design can be orthogonal and rotatable. However, this is only
true in a vary limited number of cases. See the example below:
>>> design_box_wilson(k=2, alpha_design="orthogonal", center=(1,1), face_design="CCC")
>>> design_box_wilson(k=2, alpha_design="rotatable", center=(1,1), face_design="CCC")

"""

import logging
from typing import Optional, Tuple

from numpy import zeros, ndarray, r_
from pandas import DataFrame

from lind.design.factorial import design_full_factorial
from lind._utilities import _check_int_input, _check_str_input

# set logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define public functions (ignored by jupyter notebooks)
__all__ = ["design_box_wilson"]


####################################################################################################


def _get_alpha(num_factors: int, alpha_design: Optional[str] = None,
               center: Tuple[int, int] = (1, 1)) -> [ndarray, float]:
    """
    Find the distance measure `alpha`

    Notes
    -----
    * number of factorial points = 2.0**num_factors
    * number of axial points = 2*num_factors
    * factorial center position = center[0]
    * axial center position = center[1]
    * alpha is always 1 for CCF face_design (hence default behavior for alpha_design=None)
    * CCDs always contain twice as many star points (axial points) as factors. The star points
      represent new extreme values (low and high) for each factor.
    """
    if alpha_design is None:
        return 1.0
    if alpha_design == 'orthogonal':
        # see Response Surface Methodology by Raymond Myers (1971)
        return (
            num_factors *
            (1.0 + center[1] / (2.0*num_factors)) /
            (1.0 + center[0] / (2.0**num_factors))
        )**0.5
    if alpha_design == 'rotatable':
        # see Section 5.3.3.6.1 of the Engineering Statistics Handbook for formula
        return (2.0**num_factors)**0.25
    raise ValueError("Invalid value for alpha_design: {}".format(alpha_design))


def _get_matrix_f(num_factors):
    """2 level full factorial experiment design defines the matrix_f"""
    return design_full_factorial([[-1, 1] for _ in range(num_factors)]).values


def _get_matrix_c(num_factors):
    """Generate the center point matrix"""
    matrix_c = zeros((2*num_factors, num_factors))
    for i in range(num_factors):
        matrix_c[2*i:2*i+2, i] = [-1, 1]
    return matrix_c


####################################################################################################


def design_box_wilson(k: int, alpha_design: Optional[str] = "rotatable",
                      center: Optional[Tuple[int, int]] = (1, 1),
                      face_design: Optional[str] = "CCC") -> DataFrame:
    """
    boc_wilson: Central Composite Design (CCD)

    A CCD design contains an embedded factorial design with center points
    that are augmented with a group of 'star points' that allow estimation of curvature useful for
    estimating quadratic relationships.

    CCD designs can use facing options: CCC (Circumscribed), CCI (Inscribed), and
    CCF (Face Centered).

    CCC designs are the original form of the central composite design. The star points are at some
    distance alpha from the center based on the properties desired for the design and the number of
    factors in the design. The star points establish new extremes for the low and high settings for
    all factors. These designs have circular, spherical, or hyperspherical symmetry and require 5
    levels for each factor. Augmenting an existing factorial or resolution V fractional factorial
    design with star points can produce this design.

    CCI is useful in situations where the limits specified for factor settings are truly limits, the
    CCI design uses the factor settings as the star points and creates a factorial design within
    those limits (in other words, a CCI design is a scaled down CCC design with each factor level of
    the CCC design divided by alpha to generate the CCI design). This design also requires 5 levels
    of each factor. CCI designs can use partial factorial designs for matrix_f. This is not
    supported here.

    CCF design star points are at the center of each face of the factorial space, so alpha=1. This
    requires 3 levels of each factor. Augmenting an existing factorial or resolution V design with
    appropriate star points can also produce this design.

    Parameters
    ----------
    k: int
        the total number of factors considered in the design
    alpha_design: str, optional
        The method of calculating the distance alpha. Available options: `orthogonal`, `rotatable`;
        Just like MATLAB ccdesign, `rotatable` is the default
    center: Tuple[int, int], optional
        the first value of the tuple is the factorial center point, the second value of the tuple
        is the axial center point; default value is (1, 1)
    face_design: str, optional
        this input determines the symmetry / geometric of the design; valid options are: `CCC`,
        `CCF`, and `CCI`

    Returns
    -------
    pd.DataFrame
        the box-wilson experimental design

    Examples
    --------
    >>> design = design_box_wilson(k=2, alpha_design="rotatable", center=(1,1), face_design="CCC")

    References
    ----------
    NIST
        * Section 5.3.3.6.1 of the Engineering Statistics Handbook
    Myers
        * Response Surface Methodology (1971)
    Box and Wilson
        * On the Experimental Attainment of Optimum Conditions (1951)

    Notes
    -----
    * When face_design=`CCF` the alpha_design argument is ignored and alpha is set to 1.
    * Popular CCD designs are orthogonal (OCCD), rotatable (RCCD), face (FCC), spherical (SCCD),
      and Slope Rotatable (Slope-R); of these only the first three are supported

    """

    k = _check_int_input(k, "k")
    alpha_design = _check_str_input(alpha_design, "alpha_design", ["orthogonal", "rotatable"])
    face_design = _check_str_input(face_design, "face_design", ["CCC", "CCF", "CCI"])

    if k < 2:
        raise ValueError("Input k must be >= 2 to produce a valid design.")

    center = center if alpha_design == "orthogonal" else (1, 1)
    alpha = _get_alpha(k, alpha_design=alpha_design, center=center) if \
        face_design != "ccf" else 1.0

    matrix_f = _get_matrix_f(k)
    matrix_c = _get_matrix_c(k)

    # Circumscribed Face (CCC)
    if face_design == "ccc":
        matrix_c = matrix_c * alpha

    # Inscribed Face (CCI)
    elif face_design == "cci":
        # normalize matrix_f by distance alpha
        matrix_f = matrix_f / alpha

    # Faced Centered Face (CCF): alpha is always 1

    center_1 = zeros((center[0], k))
    center_2 = zeros((center[1], k))

    return DataFrame(data=r_[
        r_[matrix_f, center_1],
        r_[matrix_c, center_2]
    ], columns=["x{}".format(i) for i in range(k)])

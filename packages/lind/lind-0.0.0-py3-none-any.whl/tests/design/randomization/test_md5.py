"""

"""

import pytest
import numpy as np

from lind.design.randomization.md5 import (
    md5shuffle,
    draw_percentile
)
from lind.design.randomization._checks import (
    runs_test
)
from lind.analysis.freq import (
    find_p_value
)

####################################################################################################


@pytest.mark.parametrize("salt", [None, " ", "randomTest", "184SeAHorse_!"])
def test_md5shuffle(salt):
    """
    """

    arr = md5shuffle(
        arr=[i for i in range(1000)],
        salt=salt
    )

    z_statistic = runs_test(arr.astype(int))
    p_value = find_p_value(
        test_statistic=z_statistic,
        df=np.inf,
        tails=True
    )
    assert p_value > 0.05


####################################################################################################


@pytest.mark.parametrize("salt, lb, ub, pct_s", [
    (None, 0.0, 0.5, 0.5),
    (None, 0.0, 0.1, 0.1),
    (None, 0.1, 0.75, 0.65),
    (None, .9, 1.0, 0.1),
])
def test_draw_percentile(salt, lb, ub, pct_s):
    """
    """

    input_arr = np.asarray([i for i in range(100000)])
    arr = draw_percentile(
        arr=input_arr,
        lb=lb, ub=ub,
        salt=salt
    )

    pct = arr.shape[0] / input_arr.shape[0]
    assert np.abs(pct - pct_s) <= 1e-2


if __name__ == '__main__':
    pytest.main(__file__)
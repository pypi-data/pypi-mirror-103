"""

"""

import pytest
import numpy as np

from lind.design.randomization._checks import (
    runs_test
)
from lind.analysis.freq import (
    find_p_value
)

####################################################################################################


@pytest.mark.parametrize("sample, random_flg", [
    (np.random.normal(0, 10, 1000), True),
    (np.linspace(0, 100, 1000), False)
])
def test_md5shuffle(sample, random_flg):
    """
    """
    z_statistic = runs_test(sample)
    p_value = find_p_value(
        test_statistic=z_statistic,
        df=np.inf,
        tails=True
    )
    assert (p_value > 0.05) == random_flg

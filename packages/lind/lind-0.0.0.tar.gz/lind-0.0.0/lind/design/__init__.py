"""
Design
======

This module is dedicated to design of experiments (DOE).
"""

from lind.design import (
    # assignment / randomization
    randomization,
    # factorial / factorial-like designs
    factorial, plackett_burman,
    # response surface designs
    box_wilson, box_behnken,
    # randomized designs
    latin_hyper_cube,
)

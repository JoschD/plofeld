"""
Constants
---------

Constants used in different places around the code.
"""
from typing import Union

import numpy as np

Numeric = Union[int, float, complex, np.number]
RealNumber = Union[int, float, np.number]

EPS = 1E-12
INTEGRATION_TIME_STEP = 0.01


ZORDER = {
    'lines': 1,
    'arrows': 2,
    'charges': 3,
    'marker': 4,
}

DEFAULT = 'default'


ELECTRIC = 'electric'
MAGNETIC = 'magnetic'

CHARGE_COLORS = {
    MAGNETIC: {-1: "#55a868", 1: "#c44e52"},
    ELECTRIC: {-1: "#069af3", 1: "#d40000"},
}

CHARGE_MARKERS = {
    MAGNETIC: {-1: "S", 1: "N"},
    ELECTRIC: {-1: u"\u2212", 1: "+"},
}

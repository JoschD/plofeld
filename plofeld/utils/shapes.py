"""
Shapes
------

Utility functions to generate different shapes.
"""
from typing import List

import numpy as np

from plofeld.utils.classes import Vector
from plofeld.elements import PointCharge


def get_regular_polygon(n: int, skew: bool = False, r: float = 1) -> List[Vector]:
    """Generate the coordinates for a regular polygon with 2n corners around the origin.

    Args:
        n (int): Half of the corners.
        skew (bool): Rotate polygon by half the angle between two poles. Default: ``False``
        r (float): All corners lie on a circle of ratius ``r``. Default: ``1``

    Returns:
         A list of Vectors defining the corners of the polygon.
    """
    n_poles = 2*n
    phases = (np.arange(0, n_poles) + (0.5 * ~skew)) / n_poles
    coordinates = r * np.exp(2 * np.pi * 1j * phases)
    return [Vector(c.real, c.imag) for c in coordinates]


def generate_mulitpole(n: int, skew: bool = False, **kwargs) -> List[PointCharge]:
    """Generate a multipole field consisting of 2n PointCharges with alternating
    polarity around origin.

    Args:
        n (int): Half of the corners.
        skew (bool): Rotate polygon by half the angle between two poles. Default: ``False``

    Keyword Args:
        Are passed on to PointCharge objects

    Return:
        List of 2n PointCharges defining the Multipole.
    """
    charge_map = {0: -1, 1: 1}
    coordinates = get_regular_polygon(n, skew)
    return [PointCharge(vec, charge_map[idx % 2], **kwargs) for idx, vec in enumerate(coordinates)]

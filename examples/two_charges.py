"""
Two Charges
-----------

If this looks familiar: Good! Your memory is fine.
This is the example used in the Readme.
"""
from matplotlib import pyplot as plt

from plofeld.elements import PointCharge
from plofeld.fields import StaticField
from plofeld.utils.classes import Vector
from plofeld.utils.constants import ELECTRIC


def plot_two_charges():
    charges = [
        PointCharge(Vector(x=1, y=0), q=-1),
        PointCharge(Vector(x=-1, y=0), q=1),
    ]

    field = StaticField(charges, field_type=ELECTRIC)
    field.plot(xlim=(-2, 2), ylim=(-2, 2))

    plt.show()


if __name__ == '__main__':
    plot_two_charges()

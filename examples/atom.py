"""
Atom
----

Plots an atom, i.e. a big Proton and a small Electron.
Hint: Not really an atom. Not really to scale.
"""
from matplotlib import pyplot as plt

from plofeld.elements import PointCharge
from plofeld.fields import StaticField
from plofeld.utils.classes import Vector
from plofeld.utils.constants import ELECTRIC


def plot_atom():
    charges = [
        PointCharge(Vector(1, 0), q=1, radius=0.5, linewidth=0.8),
        PointCharge(Vector(-1, 0), q=-1, radius=0.05, linewidth=0.8),
    ]

    field = StaticField(charges, field_type=ELECTRIC)
    field.plot(xlim=(-2, 2), ylim=(-2, 2), n_lines=36)

    plt.show()


if __name__ == '__main__':
    plot_atom()

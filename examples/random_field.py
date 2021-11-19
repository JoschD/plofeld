"""
Some random electric field
--------------------------

Plots an atom, i.e. a big Proton and a small Electron.
Hint: Not really an atom. Not really to scale.
"""
import numpy as np
from matplotlib import pyplot as plt

from plofeld.elements import PointCharge
from plofeld.fields import StaticField
from plofeld.utils.classes import Vector
from plofeld.utils.constants import ELECTRIC


def random_field(n: int):
    random_triples = np.random.rand(n, 3)*4 - 2
    charges = [
        PointCharge(Vector(x, y), q=np.sign(c))
        for x, y, c in random_triples
    ]

    field = StaticField(charges, field_type=ELECTRIC)
    field.plot(xlim=(-2, 2), ylim=(-2, 2), n_lines=16)

    plt.show()


if __name__ == '__main__':
    np.random.seed(121261)
    random_field(5)

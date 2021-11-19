"""
Multipoles
----------

Plot some multipoles!
"""
from matplotlib import pyplot as plt

from plofeld.fields import StaticField
from plofeld.utils.constants import ELECTRIC, MAGNETIC
from plofeld.utils.shapes import generate_mulitpole


def plot_multipole(n: int, skew: bool, field_type: str, **kwargs):
    """Plot a normal or skew multipole of order 2n. The field
     type specifies if you want to plot an 'electric' field,
     or a 'magnetic' field, where the only difference is the markers
     used to indicate charges. (So there are magnetic monopoles.
     I hope they don't bother you too much.)"""
    charges = generate_mulitpole(n, skew)
    field = StaticField(charges, field_type=field_type)
    field.plot(xlim=(-2, 2), ylim=(-2, 2), **kwargs)

    plt.show()


def electric_sextupole():
    """Plot a nice electric sextupole."""
    plot_multipole(
        n=3, skew=False,       # define multipole
        field_type=ELECTRIC,   # define field type ('electric' or 'magnetic')
        n_lines=36,            # number of lines per charge
        no_origin_lines=True,  # remove field lines that go through (0, 0) [ugly]
        arrows=True            # plot arrows on the lines
    )


def magnetic_dodecapole():
    """Plot a nice magnetic dade..dedoc.. 12-pole."""
    plot_multipole(
        n=6, skew=False,       # define multipole
        field_type=MAGNETIC,   # define field type ('electric' or 'magnetic')
        n_lines=24,            # number of lines per charge
        no_origin_lines=True,  # remove field lines that go through (0, 0) [ugly]
        arrows=False           # plot arrows on the lines
    )


if __name__ == '__main__':
    # electric_sextupole()
    magnetic_dodecapole()


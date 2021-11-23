# plofeld
[![Cron Testing](https://github.com/JoschD/plofeld/workflows/Cron%20Testing/badge.svg)](https://github.com/JoschD/plofeld/actions?query=workflow%3A%22Cron+Testing%22)
[![Code Climate coverage](https://img.shields.io/codeclimate/coverage/JoschD/plofeld.svg?style=popout)](https://codeclimate.com/github/JoschD/plofeld)
[![Code Climate maintainability (percentage)](https://img.shields.io/codeclimate/maintainability-percentage/JoschD/plofeld.svg?style=popout)](https://codeclimate.com/github/JoschD/plofeld)
[![GitHub last commit](https://img.shields.io/github/last-commit/JoschD/plofeld.svg?style=popout)](https://github.com/JoschD/plofeld/)
[![GitHub release](https://img.shields.io/github/release/JoschD/plofeld.svg?style=popout)](https://github.com/JoschD/plofeld/)
<!-- [![DOI](https://zenodo.org/badge/DOI/.svg)](https://doi.org/) -->


> "One of these days we must invent a faster-working field plotter!"

 
``plofeld`` is a python plotting library for physical fields.

## Installing

Installation is easily done via `pip`:

```
pip install plofeld
```

required are `numpy, scipy, pandas, matplotlib`.

### Warning: Still under development!

This package is in the early stages of development.
API changes might occur at any new push/release.
If you have a version running to your liking, don't forget to write down the version number to reproduce your results.
Apologies for the inconvenience.

## Usage

First one needs to place some `Elements`, in this example 
`PointCharges` around your coordinate system. 
The positions of these `Elements` need to be given in `Vectors`.

This list is then passed on to the `StaticField` class, which creates the
field.

The field can then be plotted with the `StaticField().plot()` function.


```python
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

```

This code and more can be found in the [`examples`](https://github.com/JoschD/plofeld/tree/master/examples) folder.



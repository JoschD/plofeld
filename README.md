# plofeld

> "One of these days we must invent a faster-working field plotter!"

---
 
``plofeld`` is a python plotting library for physical fields.

## Installing

Installation is easily done via `pip`:

```
pip install plofeld
```

required are `numpy, scipy, pandas, matplotlib`.


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

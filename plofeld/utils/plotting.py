"""
Plotting
--------

Helper functions to ease plotting tasks.
"""
from typing import Sequence

import numpy as np
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Polygon
from matplotlib.textpath import TextPath

from plofeld.utils.classes import Vector
from plofeld.utils.constants import CHARGE_COLORS, ZORDER, CHARGE_MARKERS, EPS
from plofeld.elements import PointCharge


def charge_to_circle(charge: PointCharge, kind: str) -> Circle:
    """Create the Circle Patch from a charge.

    Args:
        charge (PointCharge): The PointCharge object
        kind (str): Field type
    """
    color = charge.color
    if color is None:
        color = CHARGE_COLORS[kind][np.sign(charge.q)]
    return Circle(
        (charge.x, charge.y),
        radius=charge.radius, linewidth=charge.linewidth,
        facecolor=color, edgecolor='k',
        zorder=ZORDER['charges'],
    )


def charge_to_marker(charge: PointCharge, kind: str) -> Polygon:
    """Create the marker polygon for a charge.

    Args:
        charge (PointCharge): The PointCharge object
        kind (str): Field type
    """
    marker = charge.marker
    if marker == 'default':
        marker = CHARGE_MARKERS[kind][np.sign(charge.q)]

    # let mpl create a text-path but convert it to polygon manually
    # (TextPath objects are a bit weird and did not behave as I expected)
    path = TextPath((0, 0), marker, size=charge.radius*1.7)
    extend = path.get_extents()
    polygon = path.to_polygons()[0]

    # some manual move, because TextPath assumes real text
    polygon = polygon - extend.min  # put directly on origin
    polygon = polygon - extend.size / 2     # move center to origin
    polygon = polygon + charge.location.toarray()  # move to charge location

    return Polygon(polygon, facecolor="white", lw=0.2, zorder=ZORDER['marker'])


def add_arrow_to_line(line: Line2D, index: int = None, direction: str = 'right',
                      size: int = 15, color: str = None, **kwargs):
    """Add an arrow to the middle of a line.
    Based on: https://stackoverflow.com/a/34018322/5609590

    Args:
        line (Line2D): Matplotlib Line2D object
        index (int): Index of the data at where to point the arrow head.
                     If direction is ``'left'`` this can't be ``0``,
                     if direction is ``'right'`` this can't be the last index
                     (or ``-1``). If ``None`` is given, the middle element of
                     the line is chosen.
        direction (str): Direction of the arrow, either ``'left'`` or ``'right'``.
                         Default: ``'right'``.
        size (int): size of the arrow in fontsize points. Default: ``15``
        color (str): Color of the arrow. If ``None``, the line color is taken.
                     Default: ``None``

    Keyword Args:
        Passed on to `Axes.annotate()` function.
    """
    xdata = line.get_xdata()
    ydata = line.get_ydata()

    if color is None:
        color = line.get_color()

    if index is None:
        index = len(xdata) // 2

    end_index = index + (1 if direction == "right" else -1)

    line.axes.annotate('',
                       xytext=(xdata[index], ydata[index]),
                       xy=(xdata[end_index], ydata[end_index]),
                       arrowprops=dict(arrowstyle="->", color=color),
                       size=size, **kwargs
                       )


def is_point_visible(ax: Axes, point: Vector):
    """True if point visible within current axes limits."""
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    return xlim[0] < point.x < xlim[1] and ylim[0] < point.y < ylim[1]


def went_straight_through_origin(vectors: Sequence[Vector]):
    """Checks whether the line of points went through the origin.
    Assumes that the line is straight."""
    a, b = vectors[0].unit(), vectors[-1].unit()

    # Start and end vector are on opposite sides
    if (a + b).norm() > EPS:
        return False
    return True

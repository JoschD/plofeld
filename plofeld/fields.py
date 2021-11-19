"""
Fields
------

In this module the Fields are defined, which are the main containers for
the elements.
"""
from dataclasses import dataclass
from typing import Sequence, Tuple, Optional

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, ticker
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from scipy.integrate import ode

from plofeld.utils.classes import Vector
from plofeld.utils.constants import INTEGRATION_TIME_STEP, ZORDER, ELECTRIC, MAGNETIC, RealNumber
from plofeld.elements import PointCharge
from plofeld.utils.plotting import (
    charge_to_marker, charge_to_circle, add_arrow_to_line,
    went_straight_through_origin, is_point_visible
)


@dataclass
class StaticField:
    charges: Sequence[PointCharge]
    field_type: str = ELECTRIC

    def __post_init__(self):
        if self.field_type == MAGNETIC:
            assert all(abs(c.q) == 1 for c in self.charges)

    def field_at(self, location: Vector) -> Vector:
        """Calculates the field Vector at a given location from the charges."""
        return Vector(*np.sum([c.field_at(location) for c in self.charges], axis=0))

    def plot(self,
             xlim: Tuple[RealNumber, RealNumber] = (None, None),
             ylim: Tuple[RealNumber, RealNumber] = (None, None),
             no_ticks: bool = True, **kwargs) -> Figure:
        """Plot the given static field with all the lines and charges.

        Args:
            xlim (Tuple[RealNumber, RealNumber]): xlimits to set
            ylim (Tuple[RealNumber, RealNumber]): ylimits to set
            no_ticks (bool): No ticks on the axes. Default: True

        Keyword Args:
            other: passed on to :func:`plot_field_lines`
        """
        fig, ax = plt.subplots(1, 1)
        ax.axis("image")
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        self.plot_field_lines(ax, **kwargs)
        self.plot_charges(ax)

        if no_ticks:
            ax.xaxis.set_major_locator(ticker.NullLocator())
            ax.yaxis.set_major_locator(ticker.NullLocator())
        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$')
        fig.tight_layout()
        return fig

    # Line Plotting ----------------------------------------------------------------

    def plot_field_lines(self, ax: Axes, **kwargs):
        """Plot all the field lines around the charges in given static field.
        The field lines are on-the-fly evaluated via integration.
        So this can take a while.
        Inspired by: https://www.numbercrunch.de/blog/2013/05/visualizing-streamlines/

        Args:
            ax (Axes): Matplotlib Axes to plot on

        Keyword Args:
            n_lines (int): Number of field lines per charge, distributed in a circle.
                           Default: ``20``
            no_origin_lines (bool): Tries to remove straight lines through the
                                    origin (0, 0). Default: ``False``
            arrows (bool): Plot arrows on the lines. Default: ``True``
            color (str): Desired color of the lines. Default: ``'k'``
            time_step (float): Time step for the integration. Default: see ``INTEGRATION_TIME_STEP``

        """
        n_lines: int = kwargs.get('n_lines', 20)
        no_origin_lines: bool = kwargs.get('no_origin_lines', False)
        arrows: bool = kwargs.get('arrows', True)
        color: str = kwargs.get('color', 'k')
        time_step: float = kwargs.get('time_step', INTEGRATION_TIME_STEP)

        charges_strings = [str(c) for c in self.charges]
        connected_charges = pd.DataFrame(False, index=charges_strings, columns=charges_strings, dtype=bool)

        for charge in self.charges:
            # move forward or backward along field lines
            dt = np.sign(charge.q) * time_step

            # loop over field lines,
            # starting in different directions around current charge
            for phi in np.linspace(0, 2*np.pi*(n_lines-1)/n_lines, n_lines):
                init_point = charge.location + charge.radius * np.array([np.cos(phi), np.sin(phi)])
                line_points = [init_point]

                # Setup integrator
                r = ode(self._integration_function)
                r.set_integrator('vode')
                r.set_initial_value(init_point.tolist())
                while r.successful():
                    r.integrate(r.t + dt)
                    new_point = Vector(r.y[0], r.y[1])
                    line_points.append(new_point)

                    # stop if we left the axes
                    if not is_point_visible(ax, new_point):
                        break

                    # stop if we hit another charge
                    other_charge = self.hit_charge(new_point)
                    if other_charge is not None:
                        connected_charges.loc[str(charge), str(other_charge)] = True

                        # do not plot the line if the other charge already has done so
                        if connected_charges.loc[str(other_charge), str(charge)]:
                            line_points = None
                        break

                if line_points:
                    if no_origin_lines:
                        if went_straight_through_origin(line_points):
                            continue

                    lp_matrix = np.array(line_points)
                    line = ax.plot(lp_matrix[:, 0], lp_matrix[:, 1], color=color, marker=None, zorder=ZORDER['lines'])
                    if arrows and len(line_points) > 3:
                        add_arrow_to_line(line[0], direction="right" if charge.q > 0 else "left", zorder=ZORDER['arrows'])

    def _integration_function(self, t: float, y: Sequence[RealNumber]):
        """Integration function.
        Needs to be dependent on time t and location y to be used with ode."""
        return self.field_at(Vector(*y)).unit()

    def hit_charge(self, point: Vector) -> Optional[PointCharge]:
        """Checks if the point has hit a charge in this field.
        Returns the charge found, otherwise ``None``.

        Args:
            point (Vector): Coordinates to check.

        Returns:
            ``PointCharge`` if it hit a charge, ``None`` otherwise.
        """
        for charge in self.charges:
            if charge.is_within_radius(point):
                return charge
        return None

    # Charge Plotting --------------------------------------------------------------

    def plot_charges(self, ax: Axes):
        """Plot all charges into axes. Charges are shown as circles and
        may have a marker on top.

        Args:
            ax (Axes): The matplotlib Axes to draw on.
        """
        for charge in self.charges:
            ax.add_patch(charge_to_circle(charge, self.field_type))
            if charge.marker is not None:
                ax.add_patch(charge_to_marker(charge, self.field_type))

"""
Classes
-------

Additional Classes used in different places around the code.
Mostly to help to get data around.
"""
import numpy as np

from plofeld.utils.constants import RealNumber


class Vector(np.ndarray):
    """Class to collect coordinates.
    Basically a named-numpy array of size 2 or 3.
    Numpy subclassing of ndarrays is somewhat weird, see:
    https://numpy.org/doc/stable/user/basics.subclassing.html"""
    def __new__(cls, x: RealNumber, y: RealNumber, z: RealNumber = None):
        if z is None:
            vector = [x, y]
        else:
            vector = [x, y, z]
        return np.asarray(vector).view(cls)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        try:
            return self[2]
        except IndexError:
            return None

    def toarray(self):
        """Returns this as a normal numpy array."""
        return np.array(self)

    def norm(self) -> float:
        """Calculate the euclidean (l2) norm of this coordinates."""
        return float(np.sqrt(np.sum(np.square(self))))

    def unit(self) -> 'Vector':
        """Returns the Unit Vector from self"""
        return self / self.norm()

    def distance(self, other: 'Vector') -> float:
        """Calculate the euclidean (l2) distance of this point to other."""
        return (other - self).norm()

    def __str__(self):
        if self.z is None:
            return f"x: {self.x}, y: {self.y}"
        return f"x: {self.x}, y: {self.y}, z: {self.z}"

    def __repr__(self):
        return f"Vector({str(self)})"

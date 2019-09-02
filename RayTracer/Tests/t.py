import numpy as np


class Vector(np.ndarray):
    """
    Class used to describe points and vectors. use @ for dot product.
    """
    def __new__(cls, x, y, z, *args, **kwargs):
        obj = np.asarray([x, y, z]).view(cls)
        return obj

    def norm(self):
        return np.linalg.norm(self)

    def normalize(self):
        return self / self.norm()

    def reflect(self, other):
        other = other.normalize()
        return self - (2 * (self @ other) * other)

    def cross(self, other):
        return Vector(*np.cross(self, other))

    def __str__(self):
        return "Vector({:.2f}, {:.2f}, {:.2f})".format(*self)

    # noinspection PyMethodMayBeStatic
    def __array_finalize__(self, obj):
        if obj is None:
            return


print((Vector(1, 0, 1) * Vector(1, 1, 1)))

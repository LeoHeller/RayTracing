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
        return "Vector({:.3f}, {:.3f}, {:.3f})".format(*self)

    # noinspection PyMethodMayBeStatic
    def __array_finalize__(self, obj):
        if obj is None:
            return

    zero = (0, 0, 0)
    one = (1, 1, 1)
    up = (0, 1, 1)


class _Vector:
    """
    A generic 3-element vector. All of the methods should be self-explanatory.
    """

    # placeholders for constants
    zero = (0, 0, 0)
    one = (1, 1, 1)
    up = (0, 1, 1)

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def norm(self):
        # return np.linalg.norm(np.array([self.x, self.y, self.z]))
        return np.sqrt(np.sum(num * num for num in self))

    def normalize(self):
        return self / self.norm()

    def reflect(self, other):
        other = other.normalize()
        return self - 2 * (self * other) * other

    def cross(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def __str__(self):
        return "Vector({}, {}, {})".format(*self)

    def __add__(self, other):
        # return Vector(*self.array + other.array)
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y + self.z * other.z  # dot product
        else:
            return Vector(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other, self.z / other)

    def __pow__(self, exp):
        if exp != 2:
            raise ValueError("Exponent can only be two")
        else:
            return self * self

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    # def __eq__(self, other):
    #     return math.isclose(self.x, other.x) and math.isclose(self.y, other.y) and math.isclose(self.z, other.z)
    #     return (self.x, self.y, self.z) == (other.x, other.y, other.z)


# Since 3D points and RGB colors are effectively 3-element vectors, we simply
# declare them as aliases to the `Vector` class to take advantage of all its
# defined operations (like overloaded addition, multiplication, etc.) while
# improving readability (so we can use `color = Color(0xFF)` instead of
# `color = Vector(0xFF)`).
Point = Vector
Color = Vector


class Material:

    def __init__(self, color, specular=0.5, lambert=1, ambient=0.2):
        self.color = color
        self.specular = specular
        self.lambert = lambert
        self.ambient = ambient


class Ray:
    """
    A mathematical ray.
    """

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()

    def point_at_dist(self, dist):
        return self.origin + self.direction * dist


Vector.zero = Vector(0, 0, 0)
Vector.one = Vector(1, 1, 1)
Vector.up = Vector(0, 1, 0)

import time
from functools import reduce
import numpy as np

from helpers import *
from ViewPortMath import Camera
from abc import ABC, abstractmethod

# constants
FAR = 1.0e35  # very far away!


class Scene:
    """
    this holds all the objects and some helper functions for rendering
    """

    def __init__(self, scene_camera):
        self.camera = scene_camera

        self.objects_to_render = set()
        self.lights = set()
        s = time.time()
        self.render_scene()
        print(time.time() - s)

    def setup(self):
        pass

    def add_light(self, new_light):
        self.lights.add(new_light)

    def add_object(self, new_object):
        self.objects_to_render.add(new_object)

    def render_scene(self):
        xx, yy = np.meshgrid(np.linspace(1, self.camera.res[0], self.camera.res[0], dtype=int),
                             np.linspace(1, self.camera.res[1], self.camera.res[1], dtype=int))
        xx = xx.flatten()[:, None]
        yy = yy.flatten()[:, None]
        all_rays = self.camera.get_ray_at(xx, yy)

    def ray_trace(self, ray, depth=0, max_depth=5):
        distances = [o.intersect(ray) for o in self.objects_to_render]
        nearest = reduce(np.minimum, distances)


class Light:
    def __init__(self, light_position: Vector, light_strength: float, light_color: Color):
        self.position = light_position
        self.strength = light_strength
        self.color = light_color


class Object(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def intersect(self, *args):
        pass

    @abstractmethod
    def get_norm_at(self, point: Vector) -> Vector:
        return Vector.zero


class Sphere(Object):
    """
    A sphere object.
    """

    def __init__(self, center: Vector, radius: float, material: Vector):
        self.center = center
        self.radius = radius
        self.material = material
        super().__init__()

    def intersect(self, ray):
        """
        If `ray` intersects sphere, return the distance at which it does;
        otherwise, `None`.
        """

        sphere_to_ray = ray.origin - self.center
        b = 2 * ray.direction * sphere_to_ray
        c = sphere_to_ray ** 2 - self.radius ** 2
        discriminant = b ** 2 - 4 * c

        if discriminant >= 0:
            dist = (-b - np.sqrt(discriminant)) / 2
            if dist > 0:
                return dist

    def get_norm_at(self, pt):
        """
        Return the surface normal to the sphere at `pt`.
        """

        return (pt - self.center).normalize()


class Plane(Object):
    def __init__(self, position: Vector, normal: Vector, material: Vector):
        self.position = position
        self.normal = normal.normalize()
        self.material = material
        super().__init__()

    def intersect(self, ray):
        denominator = ray.direction * self.normal
        if np.abs(denominator) < 1e-6:
            return np.inf
        d = (self.position - ray.origin) * self.normal / denominator
        if d < 0:
            return np.inf

        return d

    def get_norm_at(self, point: Vector) -> Vector:
        return self.normal


myCamera = Camera(res=(720, 1280))
myScene = Scene(myCamera)

light = Light(Vector(5, 5, -10), 10, Color(255, 255, 255))  # point light
sphere1 = Sphere(Vector(0, 0, 2), 5, Vector(255, 0, 0))

myScene.add_object(sphere1)
myScene.add_light(light)

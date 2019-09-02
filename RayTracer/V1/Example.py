"""
A simple raytracer that supports spheres with configurable color properties
(like the base color and specular coefficient).
"""
import time

import numpy as np
from matplotlib import pyplot as plt
from V1.helpers import *


class Scene:
    """
    The scene that gets rendered. Contains information like the camera
    position, the different objects present, etc.
    """

    def __init__(self, scene_camera, scene_objects, scene_lights, width, height):
        self.camera = scene_camera
        self.objects = scene_objects
        self.lights = scene_lights
        self.width = width
        self.height = height

    def render(self):
        """
        Return a `self.height`x`self.width` 2D array of `Color`s representing
        the color of each pixel, obtained via ray-tracing.
        """

        pixels = [
            [Color() for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                ray_direction = Point(x, y) - self.camera
                ray = Ray(self.camera, ray_direction)
                pixels[y][x] = self._trace_ray(ray)

        return pixels

    def _trace_ray(self, ray, depth=0, max_depth=5):
        """
        Recursively trace a ray through the scene, returning the color it
        accumulates.
        """

        color = Color()

        if depth >= max_depth:
            return color

        intersection = self._get_intersection(ray)
        if intersection is None:
            return color

        obj, dist = intersection
        intersection_pt = ray.point_at_dist(dist)
        surface_norm = obj.surface_norm(intersection_pt)

        # ambient light
        color += obj.material.color * obj.material.ambient

        # lambert shading
        for light in self.lights:
            pt_to_light_vec = (light - intersection_pt).normalize()
            pt_to_light_ray = Ray(intersection_pt, pt_to_light_vec)
            if self._get_intersection(pt_to_light_ray) is None:
                lambert_intensity = surface_norm * pt_to_light_vec
                if lambert_intensity > 0:
                    color += obj.material.color * obj.material.lambert * \
                             lambert_intensity

        # specular (reflective) light
        reflected_ray = Ray(
            intersection_pt, ray.direction.reflect(surface_norm).normalize())
        color += self._trace_ray(reflected_ray, depth + 1) * \
                 obj.material.specular
        return color

    def _get_intersection(self, ray):
        """
        If ray intersects any of `self.objects`, return `obj, dist` (the object
        itself, and the distance to it). Otherwise, return `None`.
        """

        intersection = None
        for obj in self.objects:
            dist = obj.intersects(ray)
            if dist is not None and \
                    (intersection is None or dist < intersection[1]):
                intersection = obj, dist

        return intersection


def pixels_to_ppm(pixels):
    """
    Convert `pixels`, a 2D array of `Color`s, into a PPM P3 string.
    """

    header = "P3 {} {} 255\n".format(len(pixels[0]), len(pixels))
    img_data_rows = []
    for row in pixels:
        pixel_strs = [
            " ".join([str(int(color)) for color in pixel]) for pixel in row]
        img_data_rows.append(" ".join(pixel_strs))
    return header + "\n".join(img_data_rows)


def pixels_to_img(pixels):
    p = []
    for row in pixels:
        r = []
        for v in row:
            r.append(list(map(lambda x: x / 255, v)))
        p.append(r)
    p = np.array(p)

    plt.imshow(p, interpolation="nearest")
    plt.savefig("test.png")


if __name__ == "__main__":
    objects = [
        Sphere(
            Point(150, 120, -20), 80, Material(Color(0xFF, 0, 0),
                                               specular=0.2)),
        Sphere(
            Point(420, 120, 0), 100, Material(Color(0, 0, 0xFF),
                                              specular=0.8)),
        Sphere(Point(320, 240, -40), 50, Material(Color(0, 0xFF, 0))),
        Sphere(
            Point(300, 200, 200), 100, Material(Color(0xFF, 0xFF, 0),
                                                specular=0.8)),
        Sphere(Point(300, 130, 100), 40, Material(Color(0xFF, 0, 0xFF))),
        Sphere(Point(300, 1000, 0), 700, Material(Color(0xFF, 0xFF, 0xFF),
                                                  lambert=0.5)),
    ]
    lights = [Point(200, -100, 0), Point(600, 200, -200)]
    camera = Point(200, 200, -400)
    scene = Scene(camera, objects, lights, 192, 108)
    start = time.time()
    rendered_pixels = scene.render()
    print(f"took {time.time() - start}s to render")
    # with open("image.ppm", "w") as img_file:
    #     img_file.write(pixels_to_ppm(pixels))
    pixels_to_img(rendered_pixels)

# 16 threads: 74.6
# 8 threads: 76.7
# 4 threads: 75.3

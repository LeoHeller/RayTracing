from helpers import Vector
import math


class Camera:
    def __init__(self, fov=90, res=(1280, 720), position=Vector(0, 0, -5), target=Vector.zero, roll=Vector.up):
        self.fov = fov
        self.res = res
        self.target = target
        self.position = position
        self.roll = roll  # vertical vector which indicates where up and down is

        self.d = 1

        self.get_ray_at = self.calculate_viewport()

    def look_at(self, target: Vector):
        self.target = target
        # recalculate where rays go
        self.get_ray_at = self.calculate_viewport()

    def set_position(self, position: Vector):
        self.position = position
        # recalculate where rays go
        self.get_ray_at = self.calculate_viewport()

    def set_roll(self, roll):
        roll = math.radians(roll)
        self.roll = Vector(math.cos(roll), math.sin(roll), 0)
        # recalculate where rays go
        self.get_ray_at = self.calculate_viewport()

    def calculate_viewport(self):
        theta = math.radians(self.fov)

        m = self.res[0]
        k = self.res[1]

        t = self.target - self.position
        b = self.roll.cross(t)

        t_n = t.normalize()
        b_n = b.normalize()

        v_n = t_n.cross(b_n)

        g_x = self.d * math.tan(theta / 2)
        g_y = g_x * (m / k)

        q_x = ((2 * g_x) / (k - 1)) * b_n
        q_y = ((2 * g_y) / (m - 1)) * v_n
        p_1m = (t_n * self.d) - (g_x * b_n) - (g_y * v_n)

        LL = p_1m
        UL = p_1m + q_y * m
        LR = p_1m + q_x * k
        UR = p_1m + q_y * m + q_x * k

        def ray_at(i, j):
            u = i / self.res[0]
            v = j / self.res[1]
            p = (1 - u) * ((1 - v) * LL + v * UL) + u * ((1 - v) * LR + (v * UR))
            return p - self.position

        return ray_at


if __name__ == "__main__":
    testCam = Camera()
    print(testCam.get_ray_at(0, 0)[1])

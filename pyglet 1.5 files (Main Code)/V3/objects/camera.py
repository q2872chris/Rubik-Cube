import numpy as np
from math import sin, cos, radians
from pyglet.window import key
from utilities.general_utilities import get_quadrant
from utilities.maths_utilities import spherical_coords

vectors = {
    key.UP: lambda x, y, z: [x, 0, -z],
    key.DOWN: lambda x, y, z: [-x, 0, z],
    key.LEFT: lambda x, y, z: [-z, 0, -x],
    key.RIGHT: lambda x, y, z: [z, 0, x],
    key.SPACE: lambda x, y, z: [0, y, 0],
    key.N: lambda x, y, z: [0, -y, 0]
}


class camera:
    def __init__(self, pos=(0, 0, 0), rot=None, r_speed=0.5, speed=9.0):
        self.speed = speed
        self.r_speed = r_speed  # mouse sensitivity
        self.pos = np.array(pos, dtype=float)
        self.angle_bound = 60
        if rot is None:
            self.rot = list(spherical_coords(pos))
        else:
            self.rot = list(rot)
        self.quadrant = get_quadrant(pos)

    def check_quadrant(self) -> (tuple | None):
        """Returns the quadrant when a new quadrant is entered"""
        quadrant = get_quadrant(self.pos)
        if self.quadrant != quadrant:
            self.quadrant = quadrant
            return quadrant
        return None

    def move(self, dt: float, keys: dict):
        self.free_movement(dt, keys)
        # Locks camera onto origin:
        # (Must run after free_movement to avoid camera juddering)
        if keys[key.TAB]:
            self.rot = list(spherical_coords(self.pos))

    def orientate(self, dx: float, dy: float):
        x, y = dx * self.r_speed, dy * self.r_speed
        self.rot[0] += x
        if -self.angle_bound < self.rot[1] + y < self.angle_bound:
            self.rot[1] += y

    def free_movement(self, dt: float, keys: dict):
        angle = radians(-self.rot[0])
        xyz = [sin(angle), 1.0, cos(angle)]
        vec = np.sum([v(*xyz) for k, v in vectors.items() if keys[k]], axis=0)
        if (n := np.linalg.norm(vec)) != 0:
            self.pos += vec * dt * self.speed / n




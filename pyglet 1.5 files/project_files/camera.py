from pyglet.window import key
from numpy import array
from math import sin, cos, pi

vectors = {
    key.UP: lambda x, y, z: [x, 0, -z],
    key.DOWN: lambda x, y, z: [-x, 0, z],
    key.LEFT: lambda x, y, z: [-z, 0, -x],
    key.RIGHT: lambda x, y, z: [z, 0, x],
    key.SPACE: lambda x, y, z: [0, y, 0],
    key.N: lambda x, y, z: [0, -y, 0]
}


class camera:
    def __init__(self, pos, rot=None, speed=10):
        self.speed = speed
        self.r_speed = 0.5      # mouse sensitivity
        self.pos = array(pos, dtype=float)
        self.rot = list(rot)

    def orientate(self, dx, dy):
        self.rot[0] += dx * self.r_speed
        self.rot[1] += dy * self.r_speed

    def move(self, dt, keys):
        velocity = dt * self.speed
        angle = self.rot[0] * -pi / 180
        xyz = [velocity * sin(angle), velocity, velocity * cos(angle)]
        self.pos += sum(array(v(*xyz)) for k, v in vectors.items() if keys[k])




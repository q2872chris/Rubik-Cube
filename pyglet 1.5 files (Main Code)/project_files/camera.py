from pyglet.window import key
from numpy import array
from math import sin, cos, pi, sqrt
from collections import defaultdict
from project_files.general_utilities import sign, spherical_coords

vectors = {
    key.UP: lambda x, y, z: [x, 0, -z],
    key.DOWN: lambda x, y, z: [-x, 0, z],
    key.LEFT: lambda x, y, z: [-z, 0, -x],
    key.RIGHT: lambda x, y, z: [z, 0, x],
    key.SPACE: lambda x, y, z: [0, y, 0],
    key.N: lambda x, y, z: [0, -y, 0]
}

alternative_vectors = {key.UP: key.W, key.DOWN: key.S,
                       key.LEFT: key.A, key.RIGHT: key.D}


class camera:
    def __init__(self, pos, rot=None, speed=10):
        self.speed = speed
        self.r_speed = 0.5      # mouse sensitivity
        self.pos = array(pos, dtype=float)
        self.angle_bound = 60
        if rot is None:
            self.rot = list(spherical_coords(pos))
        else:
            self.rot = list(rot)
        # quadrant must be a tuple as it's used to index a dictionary
        self.quadrant = (sign(pos[0]), sign(pos[2]))
        self.rotate_mode = 0
        self.rotate_mode_y_vec = key.SPACE
        self.rotate_mode_xz_vec = key.UP

    def rotation_animation(self, mode):
        self.rotate_mode = mode

    def orientate(self, dx, dy):
        x, y = dx * self.r_speed, dy * self.r_speed
        self.rot[0] += x
        if -self.angle_bound < self.rot[1] + y < self.angle_bound:
            self.rot[1] += y

    def move(self, dt, keys):
        if self.rotate_mode:
            keys = defaultdict(lambda: False, {})
            # try deepcopy(keys) and lock relevant movements
            self.animate(keys)
        self.free_movement(dt, keys)
        if keys[key.TAB] or self.rotate_mode:      # locks camera onto origin
            self.rot = list(spherical_coords(self.pos))
        # checks if camera has moved to a new quadrant:
        return self.check_quadrant()

    def animation_start_position(self):
        pass

    def animate(self, keys):
        if self.rotate_mode & 1:
            keys[key.RIGHT] = True
        if self.rotate_mode & 2:
            keys[self.rotate_mode_y_vec] = True
        if self.rotate_mode & 4:
            keys[self.rotate_mode_xz_vec] = True
        self.animation(self.rotate_mode & 2)

    def animation(self, y_check):
        # movement distance/angle isn't consistent depending on start position
        # try easing functions/etc for the speed in the future?
        dist = sqrt(self.pos[0] ** 2 + self.pos[2] ** 2)
        xz_check = dist > 20 and not y_check
        if dist < 5:
            self.rotate_mode_xz_vec = key.DOWN
        if self.pos[1] > 15 or xz_check:
            self.rotate_mode_y_vec = key.N
            self.rotate_mode_xz_vec = key.UP
        elif self.pos[1] < -15 or xz_check:
            self.rotate_mode_y_vec = key.SPACE
            self.rotate_mode_xz_vec = key.UP

    def free_movement(self, dt, keys):
        velocity = dt * self.speed
        angle = self.rot[0] * -pi / 180
        xyz = [velocity * sin(angle), velocity, velocity * cos(angle)]
        self.pos += sum(array(v(*xyz)) for k, v in vectors.items() if keys[k])

    def check_quadrant(self):
        quadrant = (sign(self.pos[0]), sign(self.pos[2]))
        if self.quadrant != quadrant:
            self.quadrant = quadrant
            return quadrant
        return None


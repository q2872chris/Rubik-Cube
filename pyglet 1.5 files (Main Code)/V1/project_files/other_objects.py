from pyglet.gl import GL_LINES
from numpy import linspace
from collections import defaultdict
from project_files.general_utilities import sign

zero_sign = lambda x: 0 if x == 0 else sign(x)
num_bound = lambda s: int(max(min(s, 101), 3))


class grid:
    def __init__(self, dim, width, gap, extension_mult=2.4):
        total_cube_width = (dim * width + (dim - 1) * gap)
        self.total_grid_width = total_cube_width * extension_mult
        self.num_x = int(self.total_grid_width // (2 * width)) * 2 + 1
        self.width = self.total_grid_width / self.num_x
        quadrants = {(1, 1): [255, 255, 0], (-1, -1): [120, 40, 200],
                     (-1, 1): [0, 255, 255], (1, -1): [255, 50, 255]}
        self.quadrants = defaultdict(lambda: [255, 255, 255], quadrants)
        self.default_quadrants = defaultdict(lambda: [255, 255, 255], {})
        self.grid_data = None
        self.full = False
        self.colour = False

    def adjust_num(self, inc=False, dec=False):     # [{ and }] keys
        if inc:
            self.num_x = num_bound(self.num_x + 2)
        elif dec:
            self.num_x = num_bound(self.num_x - 2)
        self.width = self.total_grid_width / self.num_x
        self.generate_grid(self.full, self.colour)

    @staticmethod
    def lines(a, b):
        inner = [0, 0, 0]
        if a.count(0) == 2:
            return [a, inner, inner, b]
        i, v = [(j, a[j]) for j in range(3) if a[j] == b[j] and a[j] != 0][0]
        inner[i] = v
        return [a, inner, inner, b]

    @staticmethod
    def vertical_gradient(default):
        return [default, [255, 255, 255], [255, 255, 255], default]

    def horizontal_gradient(self, i, end, default):
        if i == 0 or not self.colour:
            return [[255, 255, 255] * 4]
        elif i == end or i == -end:
            return [default * 4]
        else:
            c = int(255 * self.width / abs(i))
            return [[c, c, c] * 4]

    def generate_grid(self, full=False, colour=False):
        self.full = full
        self.colour = colour
        end = self.num_x * self.width / 2
        quadrants = self.quadrants if colour else self.default_quadrants
        default = [0, 0, 0] if colour else [255, 255, 255]
        vertices = []
        colours = []
        for i in linspace(-end, end, self.num_x):
            vertices.extend(self.lines([-end, 0, i], [end, 0, i]))
            colours.extend([quadrants[(-1, zero_sign(i))] * 2])
            colours.extend([quadrants[(1, zero_sign(i))] * 2])
            vertices.extend(self.lines([i, 0, -end], [i, 0, end]))
            colours.extend([quadrants[(zero_sign(i), -1)] * 2])
            colours.extend([quadrants[(zero_sign(i), 1)] * 2])
            if full:
                h_gradient = self.horizontal_gradient(i, end, default)
                v_gradient = self.vertical_gradient(default)
                vertices.extend(self.lines([-end, i, 0], [end, i, 0]))
                colours.extend(h_gradient)
                vertices.extend(self.lines([i, -end, 0], [i, end, 0]))
                colours.extend(v_gradient)
                vertices.extend(self.lines([0, i, -end], [0, i, end]))
                colours.extend(h_gradient)
                vertices.extend(self.lines([0, -end, i], [0, end, i]))
                colours.extend(v_gradient)
        total = len(vertices)
        vertices = sum(vertices, [])
        colours = sum(colours, [])
        self.grid_data = (total, GL_LINES, ("v3f", vertices), ("c3B", colours))


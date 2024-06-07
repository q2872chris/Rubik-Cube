from pyglet.gl import GL_QUADS
import numpy as np
from collections import defaultdict

points = np.array([(1, 1, 1), (-1, 1, 1), (-1, 1, -1), (1, 1, -1),
                   (1, -1, 1), (-1, -1, 1), (-1, -1, -1), (1, -1, -1)])
# point order matters
faces = [[3, 2, 1, 0], [4, 5, 6, 7], [0, 1, 5, 4],
         [2, 3, 7, 6], [3, 0, 4, 7], [1, 2, 6, 5]]
face_vertices = sum(faces, [])
# faces = [U, D, F, B, R, L]
# face vertices must be wound counterclockwise for culling

palette = [(255, 255, 255), (255, 255, 0), (255, 150, 0),
           (255, 0, 0), (0, 255, 0), (0, 0, 255)]
default = (0, 0, 0)     # default <=> black
# palette order matters
# U, D, F, B, R, L <=> white, yellow, red, orange, blue, green

def create_colour_array(colours, mode="c3B"):
    if mode == "c4B":
        return sum([[*i, 0] * 4 for i in colours], [])
    elif mode == "c3B":
        return sum([list(i) * 4 for i in colours], [])

def cube_args(vertices, colours, vertex_mode="v3f", colour_mode="c3B"):
    return [24, GL_QUADS, None, (vertex_mode, vertices),
            (colour_mode, colours)]


class cube:
    def __init__(self, batch, centre=(0, 0, 0), colours=tuple(palette),
                 width=1.0):
        colour_array = create_colour_array(colours)
        translated_vertices = points * width / 2 + centre
        wound_vertex_vectors = [translated_vertices[i] for i in face_vertices]
        vertex_array = np.reshape(wound_vertex_vectors, (72, ))
        batch.add(*cube_args(vertex_array, colour_array))


def rubik_cube_generator(batch, dim: int, width, gap):
    end = (dim * width + (dim - 1) * gap) / 2
    s = np.linspace(-end + width / 2, end - width / 2, dim)[::-1]
    cols = [{s[0]: [palette[i], default],
             s[-1]: [default, palette[i + 1]]}
            for i in range(0, 6, 2)]
    cols = [defaultdict(lambda: [default] * 2, c) for c in cols]
    colours = lambda *yzx: sum([cols[i][yzx[i]] for i in range(3)], [])
    if dim == 1:
        colours = lambda *yzx: palette
    cubes = np.array([[[cube(batch, (x, y, z), colours(y, z, x), width)
                        for x in s] for z in s] for y in s])
    return cubes




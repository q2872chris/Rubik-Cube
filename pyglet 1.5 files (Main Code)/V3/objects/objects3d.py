import numpy as np
from pyglet.gl import GL_QUADS
from pyglet.graphics import Batch
from collections import defaultdict
from utilities.cube_utilities import rubik_cube_load_timer
from utilities.general_utilities import elementwise_dict_eval

# point order matters
points = [
    (1, 1, 1), (-1, 1, 1), (-1, 1, -1), (1, 1, -1),
    (1, -1, 1), (-1, -1, 1), (-1, -1, -1), (1, -1, -1)
]
# faces = [U, D, F, B, R, L]
# face vertices must be wound counterclockwise for culling
faces = [
    [3, 2, 1, 0], [4, 5, 6, 7], [0, 1, 5, 4],
    [2, 3, 7, 6], [3, 0, 4, 7], [1, 2, 6, 5]
]
wound_vertex_vectors = np.array([points[i] for i in np.ravel(faces)])
# palette order matters
# U, D, F, B, R, L <=> white, yellow, red, orange, blue, green
palette = (
    (255, 255, 255), (255, 255, 0), (255, 150, 0),
    (255, 0, 0), (0, 255, 0), (0, 0, 255)
)
# default <=> black
default = (0, 0, 0)

def create_colour_array(colours, colour_mode="c3B"):
    if colour_mode == "c4B":
        colours = np.insert(colours, 3, 0, axis=1)
    return np.repeat(colours, 4, axis=0).ravel()


class cube:
    def __init__(self, batch: Batch, centre=(0, 0, 0),
                 colours=palette, width=1.0, draw_flag=True,
                 vertex_mode="v3f", colour_mode="c3B"):
        self.draw_flag = draw_flag or colours.count(default) != 6
        if not self.draw_flag:
            return
        colour_array = create_colour_array(colours, colour_mode)
        translated_vertices = wound_vertex_vectors * width / 2 + centre
        vertex_array = translated_vertices.ravel()
        self.vertex_list = batch.add(
            24, GL_QUADS, None, (vertex_mode, vertex_array), (colour_mode, colour_array)
        )


@rubik_cube_load_timer
def rubik_cube_generator(batch: Batch, dim: int, width: float, gap: float,
                         inner=False) -> np.ndarray:
    end = (dim - 1) * (width + gap) / 2
    centres = np.linspace(-end, end, dim)
    if dim == 1:
        cubes = [[[cube(batch, width=width)]]]
    else:
        # edit?
        sides = [
            defaultdict(
                lambda: [default, default],
                {
                    centres[0]: [default, palette[i + 1]],
                    centres[-1]: [palette[i], default]
                }
            )
            for i in range(0, 6, 2)
        ]
        colours = lambda *yzx: elementwise_dict_eval(sides, yzx, ravel=True)
        cubes = [[[cube(batch, (x, y, z), colours(y, z, x), width, inner)
                   for x in centres] for z in centres] for y in centres]
    return np.array(cubes)




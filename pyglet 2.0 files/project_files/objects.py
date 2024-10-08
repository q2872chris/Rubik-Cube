from pyglet.gl import *
from pyglet.graphics import Group
from pyglet.math import Mat4, Vec3
from collections import defaultdict
from project_files.cube_utilities import rubik_cube_width
from project_files.cube_data import cube_data
import numpy as np

palette = cube_data.palette
default = cube_data.default_colour
points = cube_data.points
example_texture = cube_data.texture
cube_data_dict = cube_data.cube_data_dict


class CustomCubeGroup(Group):
    def __init__(self, shader_program, centre: tuple,
                 draw_self=True, texture=None):
        super().__init__()
        self.draw_self = draw_self
        if not draw_self:
            return
        self.texture = texture
        self.program = shader_program
        self.rotation = Mat4()
        self.program.use()
        self.hash_value = hash(centre)

    def update_rotation(self, angle: float, axis: str):
        if self.draw_self:
            rotation = Mat4.from_rotation(angle, Vec3(**{axis: 1}))
            self.rotation = rotation @ self.rotation

    def set_state(self):
        self.program['model'] = self.rotation
        if self.texture is not None:
            glBindTexture(GL_TEXTURE_2D, self.texture.id)

    def __hash__(self):
        return self.hash_value


class cube_generator:
    def __init__(self, program, batch, width=1.0, draw_self=True):
        self.program = program
        self.cube_data = cube_data_dict | {"batch": batch}
        self.width = width
        self.draw_self = draw_self

    def __call__(self, centre=(0.0, 0.0, 0.0), colours=tuple(palette)):
        draw_flag = self.draw_self or colours.count(default) != 6
        group = CustomCubeGroup(self.program, centre, draw_flag,
                                example_texture)
        if not draw_flag:
            return group
        colours = sum([i * 4 for i in colours], [])
        vertex_vectors = points * self.width / 2 + centre
        vertices = np.reshape(vertex_vectors, (72, ))
        kwargs = {"group": group, "colours": ('Bn', colours),
                  "vertices": ('f', vertices)}
        self.program.vertex_list_indexed(**self.cube_data, **kwargs)
        return group


def generate_rubik_cube(program, batch, dim: int, width: float,
                        gap: float, draw_inner=False):
    cube = cube_generator(program, batch, width, draw_inner)
    end = rubik_cube_width(dim, width, gap) / 2
    s = np.linspace(-end + width / 2, end - width / 2, dim)[::-1]
    colours = rubik_cube_colours(s)
    cubes = np.array([[[cube((x, y, z), colours(y, z, x))
                        for x in s] for z in s] for y in s])
    return cubes


def rubik_cube_colours(s):
    if len(s) == 1:
        colours = lambda *yzx: palette
    else:
        cols = [{s[0]: [palette[i], default],
                 s[-1]: [default, palette[i + 1]]}
                for i in range(0, 6, 2)]
        cols = [defaultdict(lambda: [default, default], c) for c in cols]
        colours = lambda *yzx: sum([cols[i][yzx[i]] for i in range(3)], [])
    return colours

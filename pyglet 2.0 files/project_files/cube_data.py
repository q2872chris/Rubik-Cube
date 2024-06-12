from project_files.general_utilities.colours import *
import pyglet as py
import numpy as np

class cube_data_generator:
    def __init__(self, shared_image="my_cat.JPG"):
        # palette, point, and face order matter
        self.palette = [white, yellow, orange, red, green, blue]
        self.default_colour = black
        # faces = [U, D, F, B, R, L]
        # face vertices must be wound counterclockwise for culling
        cube_vertices = [(1, 1, 1), (-1, 1, 1), (-1, 1, -1), (1, 1, -1),
                         (1, -1, 1), (-1, -1, 1), (-1, -1, -1), (1, -1, -1)]

        face_vectors = [[3, 2, 1, 0], [4, 5, 6, 7], [0, 1, 5, 4],
                        [2, 3, 7, 6], [3, 0, 4, 7], [1, 2, 6, 5]]
        faces = sum(face_vectors, [])

        self.points = np.array([cube_vertices[i] for i in faces])

        index_blocks = [range(i, i + 4) for i in range(0, 24, 4)]
        index_vectors = [[a, b, c, c, d, a] for a, b, c, d in index_blocks]
        indices = sum(index_vectors, [])

        face_texture_vertices = [[1, 1], [0, 1], [0, 0], [1, 0]]
        face_texture_coords = sum(face_texture_vertices, [])
        texture_coords = face_texture_coords * 6

        self.texture = py.image.load(shared_image).get_texture()

        self.cube_data_dict = {
            "count": 24,
            "mode": py.gl.GL_TRIANGLES,
            "indices": indices,
            "texture_coords": ('f', texture_coords)
        }


cube_data = cube_data_generator()

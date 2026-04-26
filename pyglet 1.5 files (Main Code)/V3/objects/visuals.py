import numpy as np
from math import radians
from utilities.maths_utilities import scipy_matrix

func_to_axis = {'y': 0, 'z': 1, 'x': 2}
func_to_axes = {'y': (1, 2), 'z': (2, 0), 'x': (0, 1)}


class move_template:
    speed: int
    quadrant: tuple

    @classmethod
    def update_quadrant(cls, new_quadrant: tuple):
        """Update the quadrant of all moves."""
        cls.quadrant = new_quadrant

    @classmethod
    def update_speed(cls, new_speed: int):
        """Update the speed of all moves."""
        cls.speed = new_speed

    def __init__(self, rot_func: str, rot_dir: int, cut: tuple, name: str):
        self.rot_func = rot_func
        self.rot_dir = rot_dir
        self.cut = cut
        self.name = name
        self.axis = func_to_axis[rot_func]
        self.axes = func_to_axes[rot_func]
        self.slice: (np.ndarray | None) = None
        self.matrix = None
        self.quadrant_dict = {
            (1, 1): self, (1, -1): self, (-1, -1): self, (-1, 1): self
        }
        self.true_reference = self
        self.reverse_reference = self

    # Use properties?
    def get_true_move(self):
        """Returns the reference to the actual move."""
        return self.true_reference

    def get_reverse_move(self):
        """Returns the reference to the reverse move."""
        return self.reverse_reference

    def shift_quadrant(self):
        """Update the quadrant (reference) of all moves."""
        new_quadrant = self.quadrant
        self.true_reference = self.quadrant_dict[new_quadrant]
        reverse_quadrant = new_quadrant[::-1]
        self.reverse_reference = self.quadrant_dict[reverse_quadrant]

    def initialise_rotation(self, cubes: np.ndarray):
        move = self.true_reference
        cubes_slice = np.split(cubes, move.cut, move.axis)[1].ravel()
        self.slice = [cube for cube in cubes_slice if cube.draw_flag]
        angle = radians(self.speed * move.rot_dir)
        self.matrix = scipy_matrix(move.rot_func, angle)

    def rotate_vertices(self):
        for cube in self.slice:
            temp = cube.vertex_list.vertices
            temp = np.reshape(temp, (3, 24), order='F')
            temp = self.matrix @ temp
            temp = np.reshape(temp, (72, ), order='F')
            cube.vertex_list.vertices = temp

    def rotate_array(self, cubes: np.ndarray) -> np.ndarray:
        move = self.true_reference
        temp = np.split(cubes, move.cut, move.axis)
        temp[1] = np.rot90(temp[1], move.rot_dir, move.axes)
        new_cubes = np.concatenate(temp, move.axis)
        return new_cubes

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<objects.visuals.template object ~ {self.name}>"


cube_rotations = ('X', 'Y', 'Z')
basic_rotations = ('U', 'D', 'R', 'L', 'F', 'B')
slice_moves = ('M', 'E', 'S')

class rubik_cube_moves:
    @staticmethod
    def get_core_moves(dim: int):
        return {
            'X': ('x', -1, (0, dim)),  # cube rotation -> right
            'Y': ('y', -1, (0, dim)),  # cube rotation -> up
            'Z': ('z', -1, (0, dim)),  # cube rotation -> front
            'U': ('y', -1, (dim - 1, dim)),  # up
            'D': ('y', 1, (0, 1)),           # down
            'R': ('x', -1, (dim - 1, dim)),  # right
            'L': ('x', 1, (0, 1)),           # left
            'F': ('z', -1, (dim - 1, dim)),  # front
            'B': ('z', 1, (0, 1)),           # back
            'M': ('x', 1, (1, dim - 1)),  # middle slice -> left
            'E': ('y', 1, (1, dim - 1)),  # middle slice -> down
            'S': ('z', -1, (1, dim - 1))  # middle slice -> front
        }

    def get_moves(self, names: iter) -> dict[str, move_template]:
        """Return instantiated moves using a subsection of self.core_moves"""
        return {name: move_template(*self.core_moves[name], name) for name in names}

    def __init__(self, dim: int):
        # self.core_moves must be initialised first:
        self.core_moves = self.get_core_moves(dim)
        # Basic moves:
        self.move_dict = self.get_moves(cube_rotations)
        if dim > 1:
            self.move_dict |= self.get_moves(basic_rotations)
        if dim > 2:
            self.move_dict |= self.get_moves(slice_moves)
        # self.base_moves must be initialised here:
        self.base_moves = list(self.move_dict.keys())   # Make this a property?
        # Higher dimension moves:
        if dim > 2:
            self.move_dict |= self.generate_wide_moves(dim)
        if dim > 3:
            self.move_dict |= self.generate_slice_moves(dim)
        if dim > 4:
            self.move_dict |= self.generate_middle_moves(dim)
        # Prime moves and double moves (must come last):
        self.move_dict |= self.generate_prime_moves()
        # Set quadrants (at the end):
        self.set_quadrants(dim)

    def set_quadrants(self, dim: int):
        """Assigns the reference dictionaries."""
        self.set_quadrant_references(['X', "Z'", "X'", 'Z'])
        if dim > 1:
            roll = ['F', 'R', 'B', 'L']
            moves = ["%s"]
            if dim > 2:
                moves += ["%sw"] + [f"{j}%sw" for j in range(3, dim)]
            if dim > 3:
                moves += [f"{j}%s" for j in range(2, dim)]
            moves += [m + '\'' for m in moves]
            for m in moves:
                self.set_quadrant_references([m % r for r in roll])
        if dim > 2:
            roll = ['M', 'S', "M'", "S'"]
            moves = [''] + [str((i - 1) // 2) for i in range(5, dim + 1, 2)]
            for m in moves:
                self.set_quadrant_references([m + r for r in roll])

    def set_quadrant_references(self, moves: list[str]):
        """Assigns the reference dictionaries."""
        for j, i in enumerate(moves):
            self.move_dict[i].quadrant_dict = {
                (1, 1): self.move_dict[moves[j % 4]],
                (1, -1): self.move_dict[moves[(j + 1) % 4]],
                (-1, -1): self.move_dict[moves[(j + 2) % 4]],
                (-1, 1): self.move_dict[moves[(j + 3) % 4]]
            }

    def generate_wide_moves(self, dim: int) -> dict[str, move_template]:
        """Generates higher dimension wide moves."""
        temp = {}
        for name in basic_rotations:
            rot_func, rot_dir, cut = self.core_moves[name]
            cut = np.array(cut)
            for i in range(1, dim - 1):
                new_cut = cut - [i, 0] if (cut[0] - i > 0) else cut + [0, i]
                new_name = f"{i + 1 if i > 1 else ''}{name}w"
                temp[new_name] = move_template(rot_func, rot_dir, new_cut, new_name)
        return temp

    def generate_slice_moves(self, dim: int) -> dict[str, move_template]:
        """Generates higher dimension slice moves."""
        temp = {}
        for name in basic_rotations:
            rot_func, rot_dir, cut = self.core_moves[name]
            cut = np.array(cut)
            for i in range(1, dim - 1):
                new_cut = cut - i if (cut[0] - i > 0) else cut + i
                new_name = f"{i + 1}{name}"
                temp[new_name] = move_template(rot_func, rot_dir, new_cut, new_name)
        return temp

    def generate_middle_moves(self, dim: int) -> dict[str, move_template]:
        """Generates higher dimension middle slice moves."""
        temp = {}
        for name in slice_moves:
            rot_func, rot_dir, cut = self.core_moves[name]
            cut = np.array(cut)
            for i in range(5, dim + 1, 2):
                new_cut = cut + [(i - 3) // 2, (3 - i) // 2]
                new_name = f"{(i - 1) // 2}{name}"
                temp[new_name] = move_template(rot_func, rot_dir, new_cut, new_name)
        return temp

    def generate_prime_moves(self) -> dict[str, move_template]:
        """Generates all the prime moves."""
        return {
            f"{name}'": move_template(
                move.rot_func, -move.rot_dir, move.cut, f"{move.name}'"
            ) for name, move in self.move_dict.items()
        }

    def __getitem__(self, item: str) -> move_template:
        return self.move_dict[item]

    def __contains__(self, item: str) -> bool:
        return item in self.move_dict

    def update_quadrant(self, new_quadrant: tuple):
        """Update the quadrant (reference) of all moves."""
        move_template.update_quadrant(new_quadrant)
        for move in self.move_dict.values():
            move.shift_quadrant()

    @staticmethod
    def update_speed(new_speed: int):
        """Update the speed of all moves."""
        move_template.update_speed(new_speed)










from project_files.matrix_functions import scipy_matrix as matrix
import numpy as np

func_to_axis = {'y': 0, 'z': 1, 'x': 2}
func_to_axes = {'y': (1, 2), 'z': (2, 0), 'x': (0, 1)}    # tuple order matters
flip_axis = {'x': 'z', 'z': 'x', 'y': 'y'}
reverse = {}


class template:
    speed: int

    @classmethod
    def update_speed(cls, new_speed: int):
        cls.speed = new_speed

    def __init__(self, rot_func, rot_dir, cut, dim):
        self.rot_func = rot_func
        self.rot_dir = rot_dir
        self.cut = cut
        self.axis = func_to_axis[rot_func]
        self.axes = func_to_axes[rot_func]
        self.name: str
        self.main_cut = cut
        self.other_cut = (dim - self.cut[1], dim - self.cut[0])
        other_rot_func = flip_axis[rot_func]
        other_rot_dir = rot_dir if rot_func == 'x' else -rot_dir
        self.quadrant_shift = {
            (1, 1): (rot_func, rot_dir, False),
            (-1, -1): (rot_func, -rot_dir, True),
            (-1, 1): (other_rot_func, other_rot_dir, rot_func == 'z'),
            (1, -1): (other_rot_func, -other_rot_dir, rot_func == 'x')
        }

    def generate_new_move(self, **kwargs):
        return template(**{"rot_func": self.rot_func, "rot_dir": self.rot_dir,
                           "cut": self.cut, **kwargs})

    def unique_id(self):
        return self.rot_func, self.rot_dir, tuple(self.cut)

    def change_quadrant(self, new_quadrant):
        if self.rot_func != 'y':
            self.rot_func, self.rot_dir, cut_flag = \
                self.quadrant_shift[new_quadrant]
            self.axis = func_to_axis[self.rot_func]
            self.axes = func_to_axes[self.rot_func]
            self.cut = self.other_cut if cut_flag else self.main_cut

    def rotate_array(self, cubes):
        temp = np.split(cubes, self.cut, self.axis)
        temp[1] = np.rot90(temp[1], self.rot_dir, self.axes)
        new_cubes = np.concatenate(temp, self.axis)
        return new_cubes

    def rotate_vertices(self, cubes):
        temp = np.split(cubes, self.cut, self.axis)
        angle = self.speed * self.rot_dir * np.pi / 180
        mult = matrix(self.rot_func, angle)
        for cube in temp[1].ravel():
            if cube.draw_self:
                m = np.array(cube.vertex_list.vertices)
                m = np.reshape(m, (3, 24), order='F')
                m = mult(m)
                m = np.reshape(m, (72, ), order='F')
                cube.vertex_list.vertices = m
                if cube.centre_flag:
                    cube.centre = mult(np.reshape(cube.centre, (3, 1)))


class rotate_cubes:
    def __init__(self, dim: int, start_quadrant: tuple, start_speed: int):
        self.U = template('y', -1, (0, 1), dim)           # up
        self.D = template('y', 1, (dim - 1, dim), dim)    # down
        self.R = template('x', -1, (0, 1), dim)           # right
        self.L = template('x', 1, (dim - 1, dim), dim)    # left
        self.F = template('z', 1, (0, 1), dim)            # front
        self.B = template('z', -1, (dim - 1, dim), dim)   # back

        self.M = template('x', 1, (1, dim - 1), dim)  # middle slice -> left
        self.E = template('y', 1, (1, dim - 1), dim)  # middle slice -> down
        self.S = template('z', 1, (1, dim - 1), dim)  # middle slice -> front

        self.X = template('x', -1, (0, dim), dim)      # cube rotation -> right
        self.Y = template('y', -1, (0, dim), dim)      # cube rotation -> up
        self.Z = template('z', 1, (0, dim), dim)       # cube rotation -> front

        add = lambda index, x, y: [x, y] if index < 3 else [-y, -x]
        for ind, i in enumerate(['U', 'R', 'F', 'D', 'L', 'B']):
            move = getattr(self, i)
            old_cut = np.array(move.cut)
            for j in range(2, dim):
                # higher dimension slice moves:
                new_cut = old_cut + add(ind, j - 1, j - 1)
                new_move = move.generate_new_move(cut=new_cut, dim=dim)
                setattr(self, f"{j}{i}", new_move)
                # higher dimension wide moves:
                new_cut = old_cut + add(ind, 0, j - 1)
                new_move = move.generate_new_move(cut=new_cut, dim=dim)
                setattr(self, f"{j if j > 2 else ''}{i}w", new_move)
        # higher dimension middle slice moves
        if dim > 4:
            for i in range(5, dim + 1, 2):
                for j in ['M', 'E', 'S']:
                    move = getattr(self, j)
                    old_cut = np.array(move.cut)
                    new_cut = old_cut + [(i - 3) // 2, (3 - i) // 2]
                    new_move = move.generate_new_move(cut=new_cut, dim=dim)
                    setattr(self, f"{(i - 1) // 2}{j}", new_move)
            # prime moves:
        for name, move in list(self.__dict__.items()):
            new_move = move.generate_new_move(rot_dir=-move.rot_dir, dim=dim)
            setattr(self, name + '\'', new_move)
        # sets name attribute:
        for name, move in self.__dict__.items():
            move.name = name
        # initialises reverse dictionary/adjust moves based on start quadrant
        self.change_quadrant(start_quadrant)
        self.update_speed(start_speed)

    def __getitem__(self, item):
        return self.__dict__[item]

    # adjusts reverse dictionary and move functions based on current quadrant
    def change_quadrant(self, new_quadrant):
        for name, move in self.__dict__.items():
            move.change_quadrant(new_quadrant)
            reverse[move.unique_id()] = name

    @staticmethod
    def update_speed(new_speed: int):
        template.update_speed(new_speed)



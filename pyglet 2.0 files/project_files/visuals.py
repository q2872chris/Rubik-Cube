import numpy as np

func_to_axis = {'y': 0, 'z': 1, 'x': 2}
func_to_axes = {'y': (1, 2), 'z': (2, 0), 'x': (0, 1)}

class template:
    def __init__(self, rot_func: str, rot_dir: int, cut: tuple,
                 dim: int):
        self.rot_func = rot_func
        self.rot_dir = rot_dir
        self.cut = cut
        self.axis = func_to_axis[rot_func]
        self.axes = func_to_axes[rot_func]
        self.name: str
        self.angle = 0

    def rotate_array(self, cubes):
        angle = abs(np.pi / 2 - abs(self.angle)) * self.rot_dir
        self.rotate_vertices(cubes, 0, angle)
        self.angle = 0
        temp = np.split(cubes, self.cut, self.axis)
        temp[1] = np.rot90(temp[1], self.rot_dir, self.axes)
        new_cubes = np.concatenate(temp, self.axis)
        return new_cubes

    def rotate_vertices(self, cubes, dt, angle=None):
        temp = np.split(cubes, self.cut, self.axis)
        if angle is None:
            angle = dt * self.rot_dir * np.pi / 180
            self.angle += angle
        for cube in temp[1].ravel():
            if cube.draw_self:
                cube.update_rotation(angle, self.rot_func)


class cube_rotation_controller:
    def __init__(self, dim: int):
        self.U = template('y', -1, (0, 1), dim)           # up
        self.D = template('y', 1, (dim - 1, dim), dim)  # down
        self.R = template('x', -1, (0, 1), dim)  # right
        self.L = template('x', 1, (dim - 1, dim), dim)  # left
        self.F = template('z', 1, (0, 1), dim)  # front
        self.B = template('z', -1, (dim - 1, dim), dim)  # back

        self.M = template('x', 1, (1, dim - 1), dim)  # middle slice -> left
        self.E = template('y', 1, (1, dim - 1), dim)  # middle slice -> down
        self.S = template('z', 1, (1, dim - 1), dim)  # middle slice -> front

        self.X = template('x', -1, (0, dim), dim)  # cube rotation -> right
        self.Y = template('y', -1, (0, dim), dim)  # cube rotation -> up
        self.Z = template('z', 1, (0, dim), dim)  # cube rotation -> front

        self.__generate_wide_and_slice_moves(dim)
        self.__set_name_attributes()    # must be called last

    def __generate_wide_and_slice_moves(self, dim):
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


    def __set_name_attributes(self):
        for name, move in self.__dict__.items():
            move.name = name

    def __getitem__(self, item):
        return self.__dict__[item]

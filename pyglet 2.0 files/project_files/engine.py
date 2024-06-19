from project_files.visuals import cube_rotation_controller
from project_files.cube_utilities.cube_functions import prime
from copy import deepcopy


class engine:
    def __init__(self, dim: int, cubes, speed=500):
        self.speed = speed
        self.cube_rotations = cube_rotation_controller(dim)
        self.scramble_generator = scramble_generator(dim)
        self.cubes = cubes
        self.frame = 0
        self.move = None
        self.move_buffer = []
        self.auto_string = ""
        self.stack_solve_flag = False
        self.stack = []

    def update_buffer(self, move: str, override=False):
        if (len(self.move_buffer) < 3 and not self.auto_string) or override:
            self.move_buffer.append(self.cube_rotations[move])

    def main(self, dt):
        if self.frame == 0 and len(self.move_buffer) > 0:
            self.new_move()
        if self.move is not None:
            self.active_move(dt)

    def new_move(self):
        self.move = self.move_buffer.pop(0)
        if not self.stack_solve_flag:
            prime_move = self.cube_rotations[prime(self.move.name)]
            self.stack.append(deepcopy(prime_move))

    def active_move(self, dt):
        frame_movement = self.speed * dt         # test: 9 / 100
        if self.frame + frame_movement >= 90:
            self.cubes = self.move.rotate_array(self.cubes)
            self.move = None
            self.frame = 0
        else:
            self.frame += frame_movement
            self.move.rotate_vertices(self.cubes, frame_movement)

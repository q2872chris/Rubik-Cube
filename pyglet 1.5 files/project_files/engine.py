from project_files.cube_utilities import prime, scramble_generator
from project_files.general_utilities import timer
from project_files.visuals import rotate_cubes, reverse
import project_files.parser as parser
from copy import deepcopy
from functools import partial

speeds = [i for i in range(1, 91) if (90 / i).is_integer()]
speed_bound = lambda s: int(max(min(s, 12), 1))
grid_colours = {(1, 1): "yellow", (-1, -1): "purple",
                (-1, 1): "turquoise", (1, -1): "pink"}
grid_defaults = {(1, 1): "", (-1, -1): "", (1, -1): "", (-1, 1): ""}
function_buffer = []

def spam_proof(func, checks=(), anti_checks=(), active=True):
    if not active:
        return func
    def inner(self, *args, **kwargs):
        if any(getattr(self, i) for i in anti_checks):
            return
        elif not any(getattr(self, i) for i in checks):
            func(self, *args, **kwargs)
        else:
            def frozen_func():
                inner(self, *args, **kwargs)
            function_buffer.append(frozen_func)
    return inner


class engine:
    def __init__(self, dim: int, cubes, start_quadrant: tuple, speed=6):
        self.speed = speed_bound(speed)
        self.frame_speed = speeds[self.speed - 1]
        self.rotate_cubes = rotate_cubes(dim, start_quadrant, self.frame_speed)
        self.scramble_generator = scramble_generator(dim)
        self.cubes = cubes
        self.move_buffer = []
        self.frame = 0
        self.move = None
        self.move_count = 0
        self.stack = []
        self.stack_solve_flag = False
        self.auto_string = ""
        self.str_stack_array = []
        self.auto_move_array = []
        self.timer = timer()
        self.quadrant = start_quadrant
        self.time_move_flag = False
        self.move_timer = timer()
        self.grid_colours = grid_defaults
        self.new_line = False

    def add_new_line(self):
        if self.new_line:
            self.new_line = False
            print()

    @partial(spam_proof, checks=("move", "auto_string"))
    def reorient_cube(self, new_quadrant: tuple):
        self.rotate_cubes.change_quadrant(new_quadrant)
        self.quadrant = new_quadrant

    def check_solved(self):
        # needs work with move simplification
        # also with cube rotations
        # maybe check_solved when adding in also
        return all(i.check_rest_position() for i in self.cubes.ravel())

    def update_buffer(self, move, override=False):
        if (len(self.move_buffer) < 3 and not self.auto_string) or override:
            self.move_buffer.append(self.rotate_cubes[move])

    def start_auto_moves(self, arr):
        self.auto_move_array = arr
        self.update_buffer(self.auto_move_array.pop(0), override=True)

    def update_grid(self, colour):          # G
        if colour:
            self.grid_colours = grid_colours
        else:
            self.grid_colours = grid_defaults

    def time_moves(self):           # T
        self.add_new_line()
        self.time_move_flag = not self.time_move_flag
        print(f"Move timer {'' if self.time_move_flag else 'de'}activated")
        print()

    # can overload buffer?
    @partial(spam_proof, checks=("move", ))
    def update_speed(self, new_speed=6, inc=False, dec=False):      # -/+
        old_speed = self.speed
        if inc:
            self.speed = speed_bound(self.speed + 1)
        elif dec:
            self.speed = speed_bound(self.speed - 1)
        else:
            self.speed = speed_bound(new_speed)
        self.frame_speed = speeds[self.speed - 1]
        self.rotate_cubes.update_speed(self.frame_speed)
        if old_speed != self.speed:
            self.add_new_line()
            print(f"New speed: {self.speed}/12")
            print()

    @partial(spam_proof, anti_checks=("auto_string", ))
    def test_move_sequence(self, string: str):       # I
        self.add_new_line()
        print("Performing user inputted move sequence...")
        self.auto_string = "Move sequence: " + string
        self.timer.start()
        self.start_auto_moves(parser.str_to_moves(string))

    @partial(spam_proof, anti_checks=("auto_string", ))
    def full_scramble(self):        # P
        self.add_new_line()
        print("Scrambling...")
        scramble = list(iter(self.scramble_generator))
        self.auto_string = "Scramble: " + " ".join(scramble)
        self.timer.start()
        self.start_auto_moves(parser.double_moves_to_moves(scramble))

    def single_random_move(self):       # J
        move_str = next(iter(self.scramble_generator))
        move = parser.double_moves_to_moves([move_str])[0]
        self.update_buffer(move)

    @partial(spam_proof, checks=("move", ), anti_checks=("auto_string", ))
    def stack_solve(self):      # O
        moves = [reverse[i.unique_id()] for i in self.stack[::-1]]
        self.stack.clear()
        self.timer.start()
        self.add_new_line()
        print("Solving...")
        if self.check_solved():
            print("Solution: No moves needed")
            self.timer.end()
            return
        self.start_auto_moves(parser.simplify_moves(moves))
        self.stack_solve_flag = True
        self.auto_string = "Solution: "

    # main loop function
    def run(self):
        if len(function_buffer) > 0:
            function_buffer.pop(0)()
        if self.frame == 0 and len(self.move_buffer) > 0:
            self.new_move()
        if self.move is not None:
            self.active_move()

    def new_move(self):
        self.move = self.move_buffer.pop(0)
        if not self.stack_solve_flag:
            prime_move = self.rotate_cubes[prime(self.move.name)]
            self.stack.append(deepcopy(prime_move))
        if self.time_move_flag:
            self.move_timer.start()

    def active_move(self):
        self.frame += self.frame_speed
        self.move.rotate_vertices(self.cubes)
        if self.frame == 90:
            self.cubes = self.move.rotate_array(self.cubes)
            if self.auto_string == "":
                self.move_info()
                self.new_line = True
            else:
                self.auto_move()
            self.move = None
            self.frame = 0

    def move_info(self):
        self.move_count += 1
        print(f"{f'Move {self.move_count}: {self.move.name}' : <15}", end="")
        grid_colour = self.grid_colours[self.quadrant]
        quadrant = f"{str(self.quadrant) : <11}colour: {grid_colour}" if \
            grid_colour else self.quadrant
        dist = 50 if grid_colour else 31
        print(f"{f'[current quadrant: {quadrant}]' : <{dist}}", end="")
        if self.time_move_flag:
            self.move_timer.end()
        else:
            print()

    def auto_move(self):
        if self.stack_solve_flag:
            self.str_stack_array.append(self.move.name)
        if self.stack_solve_flag and self.check_solved():
            self.end_sequence()
        elif len(self.auto_move_array) > 0:
            self.update_buffer(self.auto_move_array.pop(0), override=True)
        else:
            self.end_sequence()

    def end_sequence(self):
        if self.stack_solve_flag:
            self.auto_move_array.clear()
            moves = parser.moves_to_double_moves(self.str_stack_array)
            self.auto_string += " ".join(moves)
            self.str_stack_array.clear()
            self.stack_solve_flag = False
        print(self.split_long_string(self.auto_string))
        self.timer.end()
        print()
        self.auto_string = ""

    @staticmethod
    def split_long_string(string, size=100):
        colon_ind = string.index(':') + 2
        pre, post = string[:colon_ind], string[colon_ind:]
        chunks = []
        while post != "":
            sub = post[size:]
            split = sub.index(" ") if " " in sub else 9
            chunks.append(post[:size + split + 1])
            post = post[size + split + 1:]
        return pre + f"\n{' ' * len(pre)}".join(chunks)

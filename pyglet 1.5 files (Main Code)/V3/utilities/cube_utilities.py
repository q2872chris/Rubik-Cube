import numpy as np
import numpy.random as ra
from collections import defaultdict
from utilities.general_utilities import Timer


speeds = [i for i in range(1, 91) if (90 / i).is_integer()]

def speed_bound(speed: (int | float)) -> int:
    return int(max(min(speed, 12), 1))

def frame_speed(speed: int) -> int:
    return speeds[speed - 1]


def rubik_cube_load_timer(func):
    def inner(*args, **kwargs):
        timer = Timer(msg="Time taken to load cubes")
        timer.start()
        cubes = func(*args, **kwargs)
        timer.end()
        print("Rubik cube shape: {}x{}x{}".format(*cubes.shape))
        print("Total cubes:", cubes.size)
        batched_cubes = sum(i.draw_flag for i in cubes.ravel())
        print("Total batched cubes:", batched_cubes, end="\n\n")
        return cubes
    return inner


def wide(move: str, wide_flag: bool, n: int) -> str:
    wide_str = 'w' if wide_flag else ''
    num_str = '' if n < (3 if wide_flag else 2) else str(n)
    return num_str + move + wide_str


def rubik_cube_diagonal(dim: int, width: float, gap: float):
    """Return the positive corner coordinate of the rubik cube."""
    corner = (dim * width + (dim - 1) * gap) / 2
    return np.array([corner] * 3)


class scramble_generator:
    def __init__(self, dim: int):
        lengths = {1: 8, 2: 9, 3: 21}  # {4: 45, 5: 60, 6: 80, 7: 100}
        lengths = defaultdict(lambda: 5, lengths)
        self.length = lengths[dim]
        if dim == 1:
            self.moves = {'X', 'Y', 'Z'}
        else:
            self.moves = {'U', 'D', 'R', 'L', 'F', 'B'}
        self.postfix = ['', '\'', '2']
        self.wide = ["%s"]
        self.wide += ["%sw"] if dim > 3 else []
        self.wide += [f"{j}%sw" for j in range(3, 10) if dim > j * 2 - 1]

    def __iter__(self):
        previous = ''
        for _ in range(self.length):
            available_moves = self.moves - {previous}
            new = ra.choice(list(available_moves))
            previous = new
            wide_move = ra.choice(self.wide)
            new = (wide_move % new).strip()
            new += ra.choice(self.postfix)
            yield new



if __name__ == "__main__":
    scramble_generator1 = scramble_generator(dim=7)
    print(f"{scramble_generator1}:")
    print("\t", *iter(scramble_generator1))




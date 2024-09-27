from collections import defaultdict
from numpy.random import choice
from numpy import array

def prime(x: str):
    return x.rstrip('\'') + ('' if '\'' in x else '\'')


def wide(string: str, w: bool, n: int):
    wide_str = 'w' if w else ''
    num_str = '' if n < (3 if w else 2) else str(n)
    return num_str + string + wide_str


def cube_diagonal(dim, width, gap):
    # finds the positive corner coordinate
    corner = (dim * width + (dim - 1) * gap) / 2 + width / 2
    return array([corner, corner, corner], dtype=float)


def possible_moves_generator(dim: int):
    cube_moves = ['X', 'Y', 'Z']
    base_moves = ['U', 'D', 'R', 'L', 'F', 'B']
    slice_moves = ['M', 'E', 'S']
    wide_moves = [i + 'w' for i in base_moves]
    higher_moves = []
    if dim > 1:
        cube_moves += base_moves
    if dim > 2:
        cube_moves += slice_moves
        higher_moves += wide_moves
    if dim > 3:
        d = min(dim, 10)
        higher_moves += [f"{j}{i}" for j in range(3, d) for i in wide_moves]
        higher_moves += [f"{j}{i}" for j in range(2, d) for i in base_moves]
    if dim > 4:
        d = min(dim, 19)
        higher_moves += [f"{(j - 1) // 2}{i}" for j in range(5, d + 1, 2)
                         for i in slice_moves]
    return cube_moves, higher_moves


class scramble_generator:
    def __init__(self, dim: int):
        lengths = {1: 8, 2: 9, 3: 21}  # {4: 45, 5: 60, 6: 80, 7: 100}
        lengths = defaultdict(lambda: 20, lengths)
        self.length = lengths[dim]
        if dim == 1:
            self.moves = ['X', 'Y', 'Z']
        else:
            self.moves = ['U', 'D', 'R', 'L', 'F', 'B']
        self.postfix = ['', '\'', '2']
        self.wide = ["  "]
        self.wide += [" w"] if dim > 3 else []
        self.wide += [f"{j}w" for j in range(3, 10) if dim > j * 2 - 1]

    def __iter__(self):
        previous = ''
        for _ in range(self.length):
            available_moves = self.moves.copy()
            if previous != '':
                available_moves.remove(previous)
            new = choice(available_moves)
            previous = new
            wide_move = choice(self.wide)
            new = (wide_move[0] + new + wide_move[1]).strip()
            new += choice(self.postfix)
            yield new



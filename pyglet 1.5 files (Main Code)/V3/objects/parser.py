import re

def prime(move: str) -> str:
    """eg: U -> U' or F' -> F"""
    return move.rstrip('\'') + ('' if '\'' in move else '\'')


def moves_to_prime_moves(moves: list[str]) -> list[str]:
    """eg: [U F'] -> [U' F]"""
    return [prime(move) for move in moves]


def double_move_to_move(move: str) -> str:
    """eg: F2 -> F or U -> U"""
    if move[-1] == "2":
        return move[:-1]
    return move


def double_moves_to_moves(moves: list[str]) -> list[str]:
    """eg: [U F2 D] -> [U F F D]"""
    doubles = []
    for move in moves:
        if move[-1] == "2":
            move = move[:-1]
            doubles.append(move)
        doubles.append(move)
    return doubles


def moves_to_double_moves(moves: list[str]) -> list[str]:
    """eg: [F F U] -> [F2 U]"""
    temp = []
    for move in moves:
        if len(temp) > 0 and temp[-1] == move:
            temp[-1] = temp[-1].rstrip('\'') + '2'
        else:
            temp.append(move)
    return temp


def simplify_moves(moves):
    """eg: [F F F] -> [F'] or [F F F F] -> [] or [F F'] -> []"""
    temp = []
    for move in moves:
        if len(temp) > 1 and move == temp[-1] and move == temp[-2]:
            temp = temp[:-2] + [prime(move)]
        elif len(temp) > 0 and prime(move) == temp[-1]:
            temp.pop(-1)
        else:
            temp.append(move)
    return temp


def str_to_moves(string: str) -> list[str]:
    """eg: (R U) * 2 -> [R U R U] or (F R) -> [F R]
    Assumes brackets aren't nested"""
    return string.strip().split(" ")



if __name__ == "__main__":
    # print(moves_to_double_moves(['F', 'F']))
    # print(simplify_moves(['F', 'F', 'F']))
    print(str_to_moves("R U F"))




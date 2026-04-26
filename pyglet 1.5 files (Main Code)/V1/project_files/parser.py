from project_files.cube_utilities import prime
import re

"""eg: [F F] -> [F2]"""
def moves_to_double_moves(moves):
    temp = []
    for move in moves:
        if len(temp) > 0 and temp[-1] == move:
            temp[-1] = temp[-1].rstrip('\'') + '2'
        else:
            temp.append(move)
    return temp


"""eg: [R U R U] -> (R U) * 2"""
def moves_to_str(moves):
    # print(moves)
    string = ""
    temp = []
    mult = 1
    moves_length = len(moves)
    possible_patterns = [[moves[s:i + s] for i in range(2, (moves_length - s) // 2 + 1)]
                         for s in range(moves_length - 3)]
    # for i in possible_patterns:
    #     print(i)
    # quit()
    for i in moves:
        for j in temp:
            j.append(i)
        temp.append([i])
        for j in temp[1:]:
            if len(temp[0]) % len(j) == 0:
                if temp[0] == j * (len(temp[0]) // len(j)):
                    mult += 1
    print(temp)
    return string

# test = parse_moves_to_str(["R", "U", "R", "U'"] * 3)
# print(test)


"""eg: [F F F] -> [F'], [F F F F] -> [], [F F'] -> []"""
def simplify_moves(moves):
    temp = []
    for i in moves:
        if len(temp) > 1 and temp[-1] == i and temp[-2] == i:
            temp = temp[:-2] + [prime(i)]
        elif len(temp) > 0 and temp[-1] == prime(i):
            temp.pop(-1)
        else:
            temp.append(i)
    return temp


"""eg: [F2] -> [F F]"""
def double_moves_to_moves(moves):
    doubles = []
    for i, j in enumerate(moves):
        if j[-1] == "2":
            doubles.extend([j[:-1], j[:-1]])
        else:
            doubles.append(j)
    return doubles


"""eg: (R U) * 2 -> [R U R U], (X Y) -> [X Y]"""
def str_to_moves(string):
    brackets = re.compile(r"^\) *\* *([0-9]{1,2})")
    new_string = ""
    ind = 0
    while ind < len(string):
        if string[ind] == '(':
            end = string.index(')', ind)
            end_shift = 0
            mult = 1
            if match := brackets.search(string[end:]):
                mult = int(match.group(1))
                end_shift = match.span()[1]
            new_string += f"{string[ind + 1:end]} " * mult
            ind = end + end_shift + 1
        else:
            new_string += string[ind]
            ind += 1
    split_string = [i for i in new_string.split(' ') if i != '']
    moves = double_moves_to_moves(split_string)
    return moves



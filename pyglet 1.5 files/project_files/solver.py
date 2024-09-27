# Not yet integrated with rest of code but will solve a 3x3 using a human-like algorithm

import numpy as np, random as ra, re

two = lambda *args: ra.choice(sum([[i + "2'", i + "2"] for i in args], []))
turn = {(2, 1): "", (1, 2): "Y", (0, 1): two("Y"), (1, 0): "Y'",
        (2, 2): "", (0, 2): "Y", (0, 0): two("Y"), (2, 0): "Y'"}
spin = {(2, 1): "", (1, 2): "Dw'", (0, 1): two("Dw"), (1, 0): "Dw"}
r = {0: "", 1: "U'", 2: two("U"), 3: "U"}

def ring(c, mode):  #edges/corners/all
    if mode == 1:
        a = [c[0][1], c[1][2], c[2][1], c[1][0]]
    elif mode == 2:
        a = [c[0][0], c[0][2], c[2][2], c[2][0]]
    else:
        a = [c[0][0], c[0][1], c[0][2], c[1][2], c[2][2], c[2][1], c[2][0], c[1][0]]
    return [i.sides for i in a]

def roll(a, n):
    for i in range(len(a)):
        a[i] = a[i][0] + a[i][2] + a[i][1]
    return a[n:] + a[:n]

def match(pa, s):   # regex
    for i in ["x", "z", "a", "c"]:
        pa = pa.replace(i, s[pa.index(i)]) if i in pa else pa
    return re.match(pa, s)

def template(f):            # OLL/PLL template function
    def inner(self):
        rolls, mode = f(self)
        with open(f"algorithms/{f.__name__}") as g:
            t = g.read().strip().splitlines()
            c = [[k.strip().split(" "), j] for j, k in [i.split(":") for i in t]]
            a = {"".join(i): j for i, j in c}
            b = ["".join(i) for i in ring(self.cubes[2], mode)]
            for i in a.keys():
                for j in range(4):
                    if match(i, "".join(b)):
                        return r[j] + " " + a[i]
                    b = roll(b, rolls)
    return inner


class solve:
    def __init__(self):
        self.cubes = None
        self.current = 0
        self.max = 30
        self.gen = self.main()

    def __call__(self, cubes):
        self.cubes = cubes
        self.current += 1
        if self.current > self.max:
            self.gen = self.main()
            self.current = 1
        return next(self.gen)

    def main(self):     # generator
        yield solve.white_centre(*self.find("w", "v", "v"))
        for i in ["b", "o", "g", "r"]:
            for var in range(2):
                yield self.white_cross("w", i, "v", var)
        for i, j in [("b", "o"), ("o", "g"), ("g", "r"), ("r", "b")]:
            for var in range(2):
                yield self.corners("w", i, j, var)
        for i, j in [("b", "o"), ("o", "g"), ("g", "r"), ("r", "b")]:
            for var in range(2):
                yield self.edges("v", i, j, var)
        yield self.OLL_2look_1()
        yield self.OLL_2look_2()
        yield self.PLL_2look_1()
        yield self.PLL_2look_2()
        yield self.AUF()            # final LL adjustment

    @staticmethod
    def white_centre(pos, col):
        items = {1: {2: "X'", 0: "X"}, 2: {2: "Z", 0: "Z'"},
                 0: {2: two("X", "Z"), 0: ""}}      # nested dictionary
        return items[(c := col.index("w"))][pos[c]]

    def white_cross(self, a, b, c, var):
        pos, col = self.find(a, b, c)
        if var == 0:
            out = {0: " F' R U R'", 1: " R U R'", 2: ""}
            return turn[pos[1:]] + out[pos[0]]
        q = spin[self.find(b, "v", "v")[0][1:]]
        return q + (" F2" if col[0] == "w" else " U' R' F R")

    def corners(self, a, b, c, var):
        pos, col = self.find(a, b, c)
        if var == 0:
            out = {0: " R U R' U'", 2: " R U' R'", 1: " R U R' U'"}
            return turn[pos[1:]] + (out[col.index("w")] if pos[0] == 0 else "")
        e = 1 if col[2] == "w" else 0 if col[1] == "w" else 2
        put = {0: " R U' R' F' " + two("U") + " F", 2: " R U R'", 1: " F' U' F"}
        return spin[self.find(col[e], "v", "v")[0][1:]] + put[col.index("w")]

    def edges(self, a, b, c, var, order=("b", "o", "g", "r")):
        pos, col = self.find(a, b, c)
        if var == 0:
            algorithm = " R U R' U' F' U' F " + two("U")
            return turn[pos[1:]] + (algorithm if col[0] == "v" else "")
        q = spin[self.find(col[1], "v", "v")[0][1:]]
        e = {1: " U' L' U L F' L F L'", 0: " U R U' R' F R' F' R"}
        return q + e[0 if order[order.index(col[1]) - 1] == col[0] else 1]

    @template   #custom decorator
    def OLL_2look_1(self):     # yellow cross, orient edges
        return 3, 1

    @template
    def OLL_2look_2(self):     # yellow face, orient corners
        return 3, 2

    @template
    def PLL_2look_1(self):     # permute corners
        return 3, 2

    @template
    def PLL_2look_2(self):     # permute edges
        return 6, 3

    def AUF(self):
        a, b = self.cubes[2][0][0].sides[1:]
        c, d = self.cubes[1][0][0].sides[1:]
        return "U'" if a == d else "U" if b == c else two("U") if a != c else ""


    def find(self, a, b, c):    # sets
        cubes = np.array([[[i.sides for i in j] for j in k] for k in self.cubes])
        f = lambda s: [(s[0][i], s[1][i], s[2][i]) for i in range(s[0].size)]
        g = [f(np.where(i == cubes)) for i in (a, b, c)]
        items = set(g[0]).intersection(set(g[1])).intersection(set(g[2]))
        pos = items.pop()
        if (a, b, c).count("v") == 2:
            for i in items:
                if tuple(cubes[i[0]][i[1]][i[2]]).count("v") == 2:
                    pos = i
                    break
        orientation = list(cubes[pos[0]][pos[1]][pos[2]])
        return (pos[0], pos[2], pos[1]), orientation


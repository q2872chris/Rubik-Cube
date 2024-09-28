from math import sin, cos
from numpy import array, roll
from scipy.spatial.transform import Rotation

xyz = {
    "x": lambda a: [[1, 0, 0], [0, cos(a), -sin(a)], [0, sin(a), cos(a)]],
    "y": lambda a: [[cos(a), 0, sin(a)], [0, 1, 0], [-sin(a), 0, cos(a)]],
    "z": lambda a: [[cos(a), -sin(a), 0], [sin(a), cos(a), 0], [0, 0, 1]]
}

def roll_matrix(axis, a):
    # acquire the y/z matrices just using the x one
    x = [[1, 0, 0], [0, cos(a), -sin(a)], [0, sin(a), cos(a)]]
    shift = {"x": 0, "y": 1, "z": -1}[axis]
    return roll(roll(x, shift, 1), shift, 0)


def list_matrix(axis, angle):
    matrix = xyz[axis](angle)
    def mult(vec):
        return [[sum(matrix[j][i] * vec[i][k] for i in range(3))
                for k in range(len(vec[0]))]
                for j in range(3)]
    return mult


def numpy_matrix(axis, angle):
    matrix = array(xyz[axis](angle))
    def mult(vec):
        return matrix @ vec
    return mult


def scipy_matrix(axis, angle):
    matrix = Rotation.from_euler(axis, angle).as_matrix()
    def mult(vec):
        return matrix @ vec
    return mult

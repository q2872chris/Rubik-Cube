from math import atan2, sqrt, degrees, copysign
from scipy.spatial.transform import Rotation


def spherical_coords(position_vector):
    x, y, z = position_vector
    azimuth = degrees(atan2(x, z))
    polar = degrees(atan2(sqrt(x ** 2 + z ** 2), y)) - 90
    return azimuth, polar


def scipy_matrix(axis: str, angle: float):
    matrix = Rotation.from_euler(axis, angle).as_matrix()
    return matrix


def sign(x):
    return int(copysign(1, x))


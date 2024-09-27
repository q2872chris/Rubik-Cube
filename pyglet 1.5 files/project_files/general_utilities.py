import time
from datetime import timedelta
from math import copysign, pi, atan2, sqrt


class timer:
    def __init__(self, dp=2, msg="Time taken"):
        self.start_time = 0
        self.dp = dp
        self.msg = msg

    def start(self):
        self.start_time = time.time()

    def end(self, print_now=True):
        if print_now:
            self.print_stored_time()
        self.start_time = 0

    def print_stored_time(self):
        timer.print_time(self.start_time, time.time(), self.dp, self.msg)

    @staticmethod
    def print_time(start, end, dp=2, msg="Time taken"):
        t = timedelta(seconds=(end - start))
        print(f"{msg}: {str(t)[:dp - 6]}")


def sign(x):
    return int(copysign(1, x))


def spherical_coords(p, c=(0, 0.5, 0)):
    x, y, z = p[0] + c[0], p[1] + c[1], p[2] + c[2]
    polar = atan2(sqrt(x ** 2 + z ** 2), y) * 180 / pi
    azimuth = atan2(x, z) * 180 / pi
    return azimuth, polar - 90



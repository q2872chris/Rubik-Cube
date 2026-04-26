import time
from datetime import timedelta
from utilities.maths_utilities import sign


def extend(func):
    """Decorator, calls the next superclass's method instead of overriding."""
    def inner(self, *args, **kwargs):
        current_cls = next(base for base in type(self).__mro__
                           if base.__dict__.get(func.__name__) is inner)
        getattr(super(current_cls, self), func.__name__)(*args, **kwargs)
        func(self, *args, **kwargs)
    return inner


# Could do with functions also
def elementwise_dict_eval(obs: list[dict], values: list, ravel=False):
    # if len(values) != len(obs):
    #     values = np.repeat([values], len(obs), axis=0).ravel()
    output = [ob[value] for ob, value in zip(obs, values)]
    return sum(output, []) if ravel else output


def safe_sum(iterable):
    return sum(iterable[1:], iterable[0])


def get_quadrant(position_vector):
    x, y, z = position_vector
    return sign(x), sign(z)


class Timer:
    def __init__(self, msg="Time taken"):
        self.msg = msg
        self.start_time = 0
        self.end_time = 0

    def start(self):
        self.start_time = time.time()

    def end(self):
        t = timedelta(seconds=(time.time() - self.start_time))
        print(f"{self.msg}: {t}")



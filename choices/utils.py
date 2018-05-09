# Define own skip instead of requiring aenum
class skip:

    def __init__(self, value):
        self.value = value

    def __get__(self, instance, owner):
        return self.value


def group_name(cls):
    return '.'.join(cls.__qualname__.split('.')[-2:])


def with_prev_and_next(iterable):
    import itertools
    prev, crnt, next = itertools.tee(iterable, 3)
    crnt = itertools.islice(crnt, 1, None)
    next = itertools.islice(next, 2, None)
    return zip(prev, crnt, next)

# Define own skip instead of requiring aenum
class skip:

    def __init__(self, value):
        self.value = value

    def __get__(self, instance, owner):
        return self.value


def group_name(cls):
    return '.'.join(cls.__qualname__.split('.')[-2:])

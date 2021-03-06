import builtins
import enum
import types

from .utils import group_name, skip, with_prev_and_next


_original_build_class = builtins.__build_class__


class _ChoicesDict(enum._EnumDict):

    def __init__(self):
        super().__init__()
        self._choice_names = []
        self._group_map = {}

    def __setitem__(self, key, value):
        if isinstance(value, type) and issubclass(value, Group):
            if key in self._group_map:
                raise TypeError("Attempted to reuse key: {!r}".format(key))
            self._group_map[key] = value
            value = skip(value)
        super().__setitem__(key, value)
        if key in self._member_names or key in self._group_map:
            self._choice_names.append(key)


class ChoicesMeta(enum.EnumMeta):

    @classmethod
    def __prepare__(meta, name, bases):
        enum_dict = super().__prepare__(name, bases)
        choices_dict = _ChoicesDict()
        choices_dict.update(enum_dict)
        builtins.__build_class__ = lambda func, name, display=None: (
            _original_build_class(func, name, Group, display=display))
        return choices_dict

    def __new__(meta, name, bases, namespace):
        builtins.__build_class__ = _original_build_class
        invalid_name = set(namespace._choice_names) & {'choices'}
        if invalid_name:
            raise ValueError("Invalid choice name: {}".format(*invalid_name))
        enum = super().__new__(meta, name, bases, namespace)
        enum._choice_names_ = namespace._choice_names
        enum._group_map_ = namespace._group_map
        return enum


class ChoicesBase(enum.Enum):

    def __new__(cls, value, display=None):
        member = object.__new__(cls)
        member._value_ = value
        member._display_ = display
        return member

    @types.DynamicClassAttribute
    def display(self):
        if self._display_ is None:
            return self._name_.replace('_', ' ').title()
        return self._display_


class Choices(ChoicesBase):

    @classmethod
    def choices(cls):
        for name in cls._choice_names_:
            if name in cls._member_names_:
                choice = cls._member_map_[name]
                yield (choice.value, choice.display)
            elif name in cls._group_map_:
                group = cls._group_map_[name]
                group_choices = [(choice.value, choice.display)
                                 for choice in group]
                yield (group.display, group_choices)


class GroupMeta(enum.EnumMeta):

    @classmethod
    def __prepare__(meta, *args, display=None):
        return super().__prepare__(*args)

    def __new__(meta, name, bases, namespace, display=None):
        invalid_name = set(namespace._member_names) & {'display'}
        if invalid_name:
            message = "Invalid group choice name: {}"
            raise ValueError(message.format(*invalid_name))
        group = super().__new__(meta, name, bases, namespace)
        group._display_ = display
        return group

    def __repr__(cls):
        return '<enum {!r}>'.format(group_name(cls))

    @property
    def display(cls):
        if cls._display_ is None:
            display = cls.__name__[0]
            for prev, char, next in with_prev_and_next(cls.__name__):
                if char.isupper() and (prev.islower() or next.islower()):
                    display += ' '
                display += char
            return display + cls.__name__[-1]
        return cls._display_


class Group(ChoicesBase):

    def __repr__(self):
        return '<{}.{}: {!r}>'.format(
            group_name(type(self)), self._name_, self._value_)

    def __str__(self):
        return '{}.{}'.format(group_name(type(self)), self._name_)


Choices.__class__ = ChoicesMeta
Group.__class__ = GroupMeta


import copy
import typing

from collections.abc import Callable

from . import exceptions

# candidates to redefine:
# __getitem__
# __contains__
# __call__
# __getattr__


BINARY_OPERATIONS = {'__add__': 'add',
                     '__sub__': 'sub',
                     '__mul__': 'mul',
                     '__matmul__': 'matmul',
                     '__truediv__': 'truediv',
                     '__floordiv__': 'floordiv',
                     '__mod__': 'mod',
                     '__divmod__': 'divmod',
                     '__pow__': 'pow',
                     '__lshift__': 'lshift',
                     '__rshift__': 'rshift',
                     '__and__': 'and',
                     '__xor__': 'xor',
                     '__or__': 'or'}


BINARY_R_OPERATIONS = {f'__r{name[2:]}': op for name, op in BINARY_OPERATIONS.items()}

BINARY_I_OPERATIONS = {f'__i{name[2:]}': op for name, op in BINARY_OPERATIONS.items()}

UNARY_OPERATIONS = {'__neg__': 'neg',
                    '__pos__': 'pos',
                    '__invert__': 'invert'}

# Do not redefine conversions __bool__, __complex__, __float__, __int__
# since Python implicitly check returned types
# and produce errors like: TypeError: __complex__ returned non-complex (type Predicate)


# we can not chain redefined comparisons
# "a < b < c" is equal to "(a < b) and (b < c)"
# which translates to "b < c", because (a < b) is Predicate and always True (?)
# so, predicates can not spread over comparison chains
COMPARISON_OPERATIONS = {'__lt__': 'lt',
                         '__le__': 'le',
                         '__eq__': 'eq',
                         '__ne__': 'ne',
                         '__gt__': 'gt',
                         '__ge__': 'ge'}


def normalize_predicate(value: typing.Any) -> 'Predicate':
    if isinstance(value, Predicate):
        return value

    return Predicate('identity', data=value)


def unary_op(name):

    def method(self):
        return Predicate(name, data=self)

    return method


def binary_op(name):

    def method(self, other):
        return Predicate(name, data=(self, normalize_predicate(other)))

    return method


def binary_r_op(name):

    def method(self, other):
        return Predicate(name, data=(normalize_predicate(other), self))

    return method


def binary_i_op(name):

    def method(self, other):

        # ensure that current predicate will safe its class and attributes
        left = copy.copy(self)

        other = normalize_predicate(other)

        # that redefinition should be correct,
        # since operation — is standard operation and should be supported by Context class
        self.operation = name
        self.data = (left, other)

        return self

    return method


class MetaPredicate(type):

    def __new__(cls, class_name, bases, attrs):  # noqa: disable=C901

        if class_name.startswith('None'):
            return None

        for name, operation in BINARY_OPERATIONS.items():
            if name not in attrs:
                attrs[name] = binary_op(operation)

        for name, operation in BINARY_R_OPERATIONS.items():
            if name not in attrs:
                attrs[name] = binary_r_op(operation)

        for name, operation in BINARY_I_OPERATIONS.items():
            if name not in attrs:
                attrs[name] = binary_i_op(operation)

        for name, operation in UNARY_OPERATIONS.items():
            if name not in attrs:
                attrs[name] = unary_op(operation)

        for name, operation in COMPARISON_OPERATIONS.items():
            if name not in attrs:
                attrs[name] = binary_op(operation)

        return super().__new__(cls, class_name, bases, attrs)


class Predicate(metaclass=MetaPredicate):
    __slots__ = ('operation', 'data')

    def __init__(self,
                 operation: typing.Optional[str],
                 data: typing.Any):

        self.operation = operation
        self.data = data

    # TODO: improve __str__ and __repr
    def __str__(self):
        return f'{self.operation}({self.data})'

    def __repr__(self):
        return f'{self.operation}({self.data})'


def identity(context, data, *argv, **kwargs):  # pylint: disable=W0613
    return data


class Context:
    __slots__ = ('_prefix', '_operations')

    def __init__(self, prefix: typing.Optional[str] = None):
        if prefix is None:
            prefix = self.__class__.__name__

        self._prefix = prefix
        self._operations = {}

        self.register('identity', identity)

    def register(self, name: str, operation: Callable):
        if name in self._operations:
            raise exceptions.OperationAlreadyRegistered(name, self._operations[name])

        self._operations[name] = operation

    def bulk_register(self, operations: dict):
        for name, operation in operations.items():
            self.register(name, operation)

    def __call__(self, predicate: Predicate, *argv, **kwargs):
        # use Duck Typing for speed and flexibility

        if hasattr(predicate, 'operation') and predicate.operation in self._operations:
            return self._operations[predicate.operation](self, predicate.data, *argv, **kwargs)

        raise exceptions.UnknownOperation(predicate)

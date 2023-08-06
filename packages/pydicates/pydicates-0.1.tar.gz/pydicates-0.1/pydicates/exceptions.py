
from collections.abc import Callable


class Error(Exception):
    pass


class UnknownOperation(Error):

    def __init__(self, predicate):
        super().__init__(f'Can not determine operation for predicate {predicate}.')


class OperationAlreadyRegistered(Error):

    def __init__(self, name: str, operation: Callable):
        super().__init__(f'Operation "{name}" has already registered with callable {operation}')

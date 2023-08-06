

# TODO: add types annotations

def _and(context, data, *argv, **kwargs):
    return context(data[0], *argv, **kwargs) and context(data[1], *argv, **kwargs)


def _xor(context, data, *argv, **kwargs):
    return bool(context(data[0], *argv, **kwargs)) != bool(context(data[1], *argv, **kwargs))


def _or(context, data, *argv, **kwargs):
    return context(data[0], *argv, **kwargs) or context(data[1], *argv, **kwargs)


def _invert(context, data, *argv, **kwargs):
    return not context(data, *argv, **kwargs)


BOOLEANS = {'and': _and,
            'xor': _xor,
            'or': _or,
            'invert': _invert}


def _lt(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) <
            context(data[1], *argv, **kwargs))


def _le(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) <=
            context(data[1], *argv, **kwargs))


def _eq(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) ==
            context(data[1], *argv, **kwargs))


def _ne(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) !=
            context(data[1], *argv, **kwargs))


def _gt(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) >
            context(data[1], *argv, **kwargs))


def _ge(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) >=
            context(data[1], *argv, **kwargs))


COMPARISONS = {'lt': _lt,
               'le': _le,
               'eq': _eq,
               'ne': _ne,
               'gt': _gt,
               'ge': _ge}


def _add(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) +
            context(data[1], *argv, **kwargs))


def _sub(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) -
            context(data[1], *argv, **kwargs))


def _mul(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) *
            context(data[1], *argv, **kwargs))


def _matmul(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) @
            context(data[1], *argv, **kwargs))


def _truediv(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) /
            context(data[1], *argv, **kwargs))


def _floordiv(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) //
            context(data[1], *argv, **kwargs))


def _mod(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) %
            context(data[1], *argv, **kwargs))


def _divmod(context, data, *argv, **kwargs):
    return divmod(context(data[0], *argv, **kwargs),
                  context(data[1], *argv, **kwargs))


def _pow(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) **
            context(data[1], *argv, **kwargs))


def _lshift(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) <<
            context(data[1], *argv, **kwargs))


def _rshift(context, data, *argv, **kwargs):
    return (context(data[0], *argv, **kwargs) >>
            context(data[1], *argv, **kwargs))


def _neg(context, data, *argv, **kwargs):
    return -context(data, *argv, **kwargs)


def _pos(context, data, *argv, **kwargs):
    return +context(data, *argv, **kwargs)


MATH = {'add': _add,
        'sub': _sub,
        'mul': _mul,
        'matmul': _matmul,
        'truediv': _truediv,
        'floordiv': _floordiv,
        'mod': _mod,
        'divmod': _divmod,
        'pow': _pow,
        'lshift': _lshift,
        'rshift': _rshift,
        'neg': _neg,
        'pos': _pos}

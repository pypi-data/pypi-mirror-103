# Predicates for Python

Library for constuction predicates like `(OwnedBy('alex') | OwnedBy('alice')) & HasTag('game-design')` and applying them to other objects.

## Motivation

I tired from reimplementation of custom predicate logic in my pet projects. So, I implemented that library.

Library focus on usability, not performance. At least, for now.

## Install

```bash
pip install pydicates
```

## Use

[Minimal example](./examples/simplest.py)

```python
from pydicates import Predicate, common


def HasTag(tag):
    return Predicate('has_tag', tag)


def has_tag(context, tag, document):
    return tag in document['tags']


common.register('has_tag', has_tag)


document = {'tags': ('a', 'b', 'c', 'd')}


assert common(HasTag('a') & HasTag('c'), document)
assert not common(HasTag('a') & HasTag('e'), document)
assert common(HasTag('a') & ~HasTag('e'), document)
assert common(HasTag('a') & (HasTag('e') | HasTag('d')), document)
```

More examples can be found in [./examples](./examples) directory.

See [./examples/documents_check.py](./examples/documents_check.py) for API description.

See [./tests](./tests) for more examples.

## Limitations

- Can not chain redefined comparisons: `a < b < c` is equal to `(a < b) and (b < c)` which translates by Python to `b < c`, because `a < b` is object (Predicate) and always `True`.

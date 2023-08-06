# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydicates']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydicates',
    'version': '0.1.1',
    'description': 'Predicates for Python.',
    'long_description': "# Predicates for Python\n\nLibrary for constuction predicates like `(OwnedBy('alex') | OwnedBy('alice')) & HasTag('game-design')` and applying them to other objects.\n\n## Motivation\n\nI tired from reimplementation of custom predicate logic in my pet projects. So, I implemented that library.\n\nLibrary focus on usability, not performance. At least, for now.\n\n## Install\n\n```bash\npip install pydicates\n```\n\n## Use\n\n[Minimal example](https://github.com/Tiendil/pydicates/tree/develop/examples/simplest.py)\n\n```python\nfrom pydicates import Predicate, common\n\n\ndef HasTag(tag):\n    return Predicate('has_tag', tag)\n\n\ndef has_tag(context, tag, document):\n    return tag in document['tags']\n\n\ncommon.register('has_tag', has_tag)\n\n\ndocument = {'tags': ('a', 'b', 'c', 'd')}\n\n\nassert common(HasTag('a') & HasTag('c'), document)\nassert not common(HasTag('a') & HasTag('e'), document)\nassert common(HasTag('a') & ~HasTag('e'), document)\nassert common(HasTag('a') & (HasTag('e') | HasTag('d')), document)\n```\n\nMore examples can be found in [./examples](https://github.com/Tiendil/pydicates/tree/develop/examples) directory.\n\nSee [./examples/documents_check.py](https://github.com/Tiendil/pydicates/tree/develop/examples/documents_check.py) for API description.\n\nSee [./tests](https://github.com/Tiendil/pydicates/tree/develop/tests) for more examples.\n\n## Limitations\n\n- Can not chain redefined comparisons: `a < b < c` is equal to `(a < b) and (b < c)` which translates by Python to `b < c`, because `a < b` is object (Predicate) and always `True`.\n",
    'author': 'Aliaksei Yaletski (Tiendil)',
    'author_email': 'a.eletsky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tiendil/pydicates',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

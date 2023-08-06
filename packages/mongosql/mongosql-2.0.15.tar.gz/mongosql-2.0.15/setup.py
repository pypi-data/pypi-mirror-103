# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongosql', 'mongosql.crud', 'mongosql.handlers', 'mongosql.util']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy>=1.2,<2.0,!=1.2.9,<1.4']

setup_kwargs = {
    'name': 'mongosql',
    'version': '2.0.15',
    'description': 'A JSON query engine with SqlAlchemy as a back-end',
    'long_description': None,
    'author': 'Mark Vartanyan',
    'author_email': 'kolypto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kolypto/py-mongosql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

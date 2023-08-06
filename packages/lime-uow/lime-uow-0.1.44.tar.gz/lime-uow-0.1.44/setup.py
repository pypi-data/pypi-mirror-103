# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lime_uow',
 'lime_uow.pyodbc_resources',
 'lime_uow.resources',
 'lime_uow.sqlalchemy_resources']

package_data = \
{'': ['*']}

extras_require = \
{'pyodbc': ['pyodbc>=4.0.30,<5.0.0'],
 'sqlalchemy': ['SQLAlchemy>=1.3.19,<2.0.0']}

setup_kwargs = {
    'name': 'lime-uow',
    'version': '0.1.44',
    'description': 'Framework to support the Unit-of-Work pattern',
    'long_description': None,
    'author': 'Mark Stefanovic',
    'author_email': 'markstefanovic@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MarkStefanovic/lime-uow',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

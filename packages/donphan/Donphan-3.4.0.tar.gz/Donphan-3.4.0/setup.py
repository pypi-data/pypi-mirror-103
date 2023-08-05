# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['donphan']

package_data = \
{'': ['*']}

install_requires = \
['asyncpg>=0.18.3']

setup_kwargs = {
    'name': 'donphan',
    'version': '3.4.0',
    'description': 'Asyncronous Database ORM for Postgres',
    'long_description': 'Donphan\n=======\n\n.. image:: https://readthedocs.org/projects/donphan/badge/?version=latest\n    :target: https://donphan.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\nAscynronous database ORM for use with Postgres.',
    'author': 'bijij',
    'author_email': 'josh@josh-is.gay',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)

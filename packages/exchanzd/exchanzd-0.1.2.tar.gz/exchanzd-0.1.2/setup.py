# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exchanzd']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'exchanzd',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Hirokazu Hirono',
    'author_email': 'hirono.hirokazu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

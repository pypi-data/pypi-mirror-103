# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['casey']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'casey',
    'version': '1.0.0',
    'description': 'A simple library to support various string notation systems',
    'long_description': None,
    'author': 'Marek Sierociński',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

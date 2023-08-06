# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['propheto']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'propheto',
    'version': '0.1.0',
    'description': 'Propheto - MLOps Software Platform',
    'long_description': 'Propheto\n========\n\nMLOps software tooling for cloud environments.\n\n',
    'author': 'Dan McDade',
    'author_email': 'dan@propheto.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Propheto-io/propheto',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['christina']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'christina',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Christina Hedges',
    'author_email': 'christina.l.hedges@nasa.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

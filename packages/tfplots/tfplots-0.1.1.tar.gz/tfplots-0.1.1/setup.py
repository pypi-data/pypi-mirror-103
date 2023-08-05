# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tfplots']

package_data = \
{'': ['*']}

install_requires = \
['altair-saver>=0.5.0,<0.6.0',
 'altair>=4.1.0,<5.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'pandas>=1.2.4,<2.0.0']

setup_kwargs = {
    'name': 'tfplots',
    'version': '0.1.1',
    'description': 'Utilities for quickly plotting logged tensorflow data',
    'long_description': None,
    'author': 'Andy Jackson',
    'author_email': 'amjack100@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

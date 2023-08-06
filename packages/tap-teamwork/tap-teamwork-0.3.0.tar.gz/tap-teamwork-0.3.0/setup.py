# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_teamwork', 'tap_teamwork.tests']

package_data = \
{'': ['*'], 'tap_teamwork': ['schemas/*']}

install_requires = \
['singer-sdk>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'tap-teamwork',
    'version': '0.3.0',
    'description': 'Singer.io tap for Teamwork.com',
    'long_description': None,
    'author': 'Stephen Bailey',
    'author_email': 'stkbailey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)

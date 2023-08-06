# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libsimba', 'libsimba.auth']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['test = libsimba.simba:Simba.test']}

setup_kwargs = {
    'name': 'libsimba.py-platform',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Adam Brinckman',
    'author_email': 'abrinckm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

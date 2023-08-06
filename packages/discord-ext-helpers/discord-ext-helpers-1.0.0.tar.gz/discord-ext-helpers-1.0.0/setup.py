# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['helpers']

package_data = \
{'': ['*']}

install_requires = \
['discord.py']

setup_kwargs = {
    'name': 'discord-ext-helpers',
    'version': '1.0.0',
    'description': 'A collection of helpers to use with discord.py',
    'long_description': None,
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

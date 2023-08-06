# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modcfg']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'modcfg',
    'version': '0.1.1',
    'description': 'Yes another config lang',
    'long_description': None,
    'author': 'Bryan Hu',
    'author_email': 'bryan.hu.2020@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

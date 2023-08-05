# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mbd_pay']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'mbd-pay',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'shaoxyz',
    'author_email': 'shwb95@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

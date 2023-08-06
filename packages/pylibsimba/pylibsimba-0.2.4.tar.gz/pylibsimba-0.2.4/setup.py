# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylibsimba', 'pylibsimba.base']

package_data = \
{'': ['*']}

install_requires = \
['hdwallet>=1.1.1,<2.0.0', 'web3>=5.18.0,<6.0.0']

setup_kwargs = {
    'name': 'pylibsimba',
    'version': '0.2.4',
    'description': 'A library simplifying the use of SIMBAChain APIs',
    'long_description': None,
    'author': 'ian.harvey',
    'author_email': 'ian.harvey@simbachain.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

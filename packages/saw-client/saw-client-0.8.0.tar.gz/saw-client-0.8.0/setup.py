# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['saw_client']

package_data = \
{'': ['*']}

install_requires = \
['BitVector>=3.4.9,<4.0.0',
 'argo-client==0.0.4',
 'cryptol==2.11.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'saw-client',
    'version': '0.8.0',
    'description': 'SAW client for the SAW 0.8 RPC server',
    'long_description': None,
    'author': 'Andrew Kent',
    'author_email': 'andrew@galois.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

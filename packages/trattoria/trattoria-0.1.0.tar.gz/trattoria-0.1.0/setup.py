# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trattoria']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.19.5', 'scipy==1.5.4', 'trattoria-core==0.1.0']

setup_kwargs = {
    'name': 'trattoria',
    'version': '0.1.0',
    'description': 'The fastest streaming algorithms for your TTTR data',
    'long_description': None,
    'author': 'Guillem Ballesteros',
    'author_email': 'dev+pypi@maxwellrules.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

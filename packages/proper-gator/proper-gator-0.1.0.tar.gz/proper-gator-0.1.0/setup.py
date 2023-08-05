# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proper_gator']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'google-api-python-client>=2.0.2,<3.0.0',
 'google-auth-oauthlib>=0.4.3,<0.5.0',
 'google-auth>=1.28.0,<2.0.0',
 'pyrate-limiter>=2.3.0,<3.0.0']

entry_points = \
{'console_scripts': ['proper_gator = proper_gator.cli:cli']}

setup_kwargs = {
    'name': 'proper-gator',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Colin Burr',
    'author_email': 'cburr@industrydive.com',
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

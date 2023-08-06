# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_portal_archiver', 'data_portal_archiver.tests']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.17.1,<0.18.0',
 'internetarchive>=2.0.2,<3.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['dpa = data_portal_archiver.main:run']}

setup_kwargs = {
    'name': 'data-portal-archiver',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Lucas Bellomo',
    'author_email': 'lbellomo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

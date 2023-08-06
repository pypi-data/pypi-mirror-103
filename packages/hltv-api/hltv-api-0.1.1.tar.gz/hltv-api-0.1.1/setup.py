# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hltv_api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'lxml>=4.6.2,<5.0.0',
 'pytz>=2021.1,<2022.0']

setup_kwargs = {
    'name': 'hltv-api',
    'version': '0.1.1',
    'description': 'An unofficial async HLTV client',
    'long_description': None,
    'author': 'Daniel van Flymen',
    'author_email': 'vanflymen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

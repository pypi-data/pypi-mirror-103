# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['holdingsparser']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'lxml>=4.6.3,<5.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['holdingsparser = holdingsparser.__main__:main']}

setup_kwargs = {
    'name': 'holdingsparser',
    'version': '0.1.0a1',
    'description': 'A program that parses 13F reports filed with the SEC.',
    'long_description': None,
    'author': 'mhadam',
    'author_email': 'michael@hadam.us',
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

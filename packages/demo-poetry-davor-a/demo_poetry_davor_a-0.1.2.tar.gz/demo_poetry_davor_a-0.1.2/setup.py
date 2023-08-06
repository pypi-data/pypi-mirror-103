# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['demo_poetry_davor_a']

package_data = \
{'': ['*']}

install_requires = \
['loguru', 'psutil']

entry_points = \
{'console_scripts': ['run = main:script']}

setup_kwargs = {
    'name': 'demo-poetry-davor-a',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Jorge',
    'author_email': 'larajorge11@gmail.com',
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

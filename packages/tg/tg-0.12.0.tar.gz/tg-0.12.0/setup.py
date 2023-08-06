# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tg']

package_data = \
{'': ['*'], 'tg': ['resources/*']}

install_requires = \
['python-telegram==0.14.0']

entry_points = \
{'console_scripts': ['tg = tg.__main__:main']}

setup_kwargs = {
    'name': 'tg',
    'version': '0.12.0',
    'description': 'Terminal Telegram client',
    'long_description': None,
    'author': 'Paul Nameless',
    'author_email': 'reacsdas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

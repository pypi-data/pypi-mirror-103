# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ikutsu']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0', 'pendulum>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['ikutsu = ikutsu.ikutsu:main']}

setup_kwargs = {
    'name': 'ikutsu',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Hirokazu Hirono',
    'author_email': 'hirono.hirokazu@gmail.com',
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

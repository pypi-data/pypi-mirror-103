# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docker_snapshot', 'docker_snapshot.images']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click-aliases>=1.0.1,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'docker>=5.0.0,<6.0.0',
 'hruid>=0.0.3,<0.0.4',
 'rich>=10.1.0,<11.0.0']

entry_points = \
{'console_scripts': ['ds = docker_snapshot.main:execute_cli']}

setup_kwargs = {
    'name': 'docker-snapshot',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'occamz',
    'author_email': None,
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

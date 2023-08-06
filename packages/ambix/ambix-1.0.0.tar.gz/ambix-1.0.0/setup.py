# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ambix', 'ambix.commands']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0',
 'pendulum>=2.1.2,<3.0.0',
 'py-buzz>=2.1.3,<3.0.0',
 'redbaron>=0.9.2,<0.10.0',
 'toposort>=1.6,<2.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['ambix = ambix.cli:cli']}

setup_kwargs = {
    'name': 'ambix',
    'version': '1.0.0',
    'description': 'alembic history cleaning tool',
    'long_description': None,
    'author': 'Tucker Beck',
    'author_email': 'tucker.beck@gmail.com',
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

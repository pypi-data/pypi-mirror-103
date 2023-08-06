# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sysq']

package_data = \
{'': ['*'], 'sysq': ['data/*']}

entry_points = \
{'console_scripts': ['sysq = sysq.core:main']}

setup_kwargs = {
    'name': 'sysq',
    'version': '1.7.0',
    'description': 'demo query sys functions',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

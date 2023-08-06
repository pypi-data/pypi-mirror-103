# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fibery', 'fibery.client', 'fibery.console', 'fibery.console.commands']

package_data = \
{'': ['*'], 'fibery.console.commands': ['js/*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'pyppeteer>=0.2.5,<0.3.0',
 'requests>=2.25.1,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['fibery = fibery.console.main:main']}

setup_kwargs = {
    'name': 'fibery',
    'version': '0.2.0',
    'description': 'Python SDK for working with Fibery.io',
    'long_description': None,
    'author': 'Sergio Bershadsky',
    'author_email': 'sergio.bershadsky@gmail.com',
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

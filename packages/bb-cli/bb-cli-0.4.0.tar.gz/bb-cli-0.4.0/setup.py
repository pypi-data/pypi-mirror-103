# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bb', 'bb.cmd']

package_data = \
{'': ['*']}

install_requires = \
['dateutils>=0.6.12,<0.7.0',
 'humanize>=3.4.1,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=10.1.0,<11.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['bb = bb.main:app']}

setup_kwargs = {
    'name': 'bb-cli',
    'version': '0.4.0',
    'description': "Bitbucket's command line tool",
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
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

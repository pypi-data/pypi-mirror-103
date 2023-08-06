# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['escape_cli',
 'escape_cli.commands',
 'escape_cli.executor',
 'escape_cli.middlewares',
 'escape_cli.patchs',
 'escape_cli.static',
 'escape_cli.utils']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2,<4.0',
 'Flask>=1.1.2,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'coverage>=5.5,<6.0',
 'inquirer>=2.7.0,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pydash>=5.0.0,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'simplejson>=3.17.2,<4.0.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['escape-py = escape_cli:main']}

setup_kwargs = {
    'name': 'escape-py',
    'version': '1.0.0b1',
    'description': "Escape's Python CLI",
    'long_description': "# Python CLI\n\nEscape's Command Line Interface for Python\n\n## Install for development\n\n### Install Poetry globally\n\nPoetry is a `pip` replacement which is very close to `npm` in Node.js.\n\n`python3.9 -m pip install poetry`\n\n### Set your Poetry default venv path\n\nMore info: https://python-poetry.org/docs/configuration/#cache-dir\n\nYou can either use a global Virtual Env for all your Python projects such as:\n`poetry config virtualenvs.path ~/.venv`\n\nOr create a Virtual Env specific to your project:\n`poetry config virtualenvs.in-project true`\n\n### Main Functions\n\nMore info: https://python-poetry.org/docs/cli/\n\nBasic functions:\n\n- `poetry shell`: Source the Virtual Env of the repo\n- `poetry install`: Install all dependencies\n- `poetry install --no-dev`: Install all dependencies expect dev dependencies\n- `poetry update`: Update dependencies\n- `poetry add my-depency`: Add dependency\n\n## Install Escape-CLI in editable mode in another project\n\nTo install the CLI in the application Virtual Env on which you want to use the CLI in editable mode (meaning you will not need to reinstall it a each edit), simply run from the root of this directory:\n\n`./scripts/install-in-venv.sh ../../path/to/my/.venv/bin/activate`\n\nNote the path can be relative or absolute.\n",
    'author': 'Escape Technologies SAS',
    'author_email': 'ping@escape.tech',
    'maintainer': 'Antoine Carossio',
    'maintainer_email': 'antoine.carossio@me.com',
    'url': 'https://escape.tech/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

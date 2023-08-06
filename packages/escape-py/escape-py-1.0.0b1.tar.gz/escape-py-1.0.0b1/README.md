# Python CLI

Escape's Command Line Interface for Python

## Install for development

### Install Poetry globally

Poetry is a `pip` replacement which is very close to `npm` in Node.js.

`python3.9 -m pip install poetry`

### Set your Poetry default venv path

More info: https://python-poetry.org/docs/configuration/#cache-dir

You can either use a global Virtual Env for all your Python projects such as:
`poetry config virtualenvs.path ~/.venv`

Or create a Virtual Env specific to your project:
`poetry config virtualenvs.in-project true`

### Main Functions

More info: https://python-poetry.org/docs/cli/

Basic functions:

- `poetry shell`: Source the Virtual Env of the repo
- `poetry install`: Install all dependencies
- `poetry install --no-dev`: Install all dependencies expect dev dependencies
- `poetry update`: Update dependencies
- `poetry add my-depency`: Add dependency

## Install Escape-CLI in editable mode in another project

To install the CLI in the application Virtual Env on which you want to use the CLI in editable mode (meaning you will not need to reinstall it a each edit), simply run from the root of this directory:

`./scripts/install-in-venv.sh ../../path/to/my/.venv/bin/activate`

Note the path can be relative or absolute.

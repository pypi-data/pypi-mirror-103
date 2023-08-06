"""Main."""

import os
import sys
import click
from . import __version__, commands
from .utils import title


@click.group(invoke_without_command=True)
@click.option('-v', '--version/--no-version', 'version', default=False)
@click.option('-c', '--config', 'config_path', nargs=1, default='')
def main(version: bool, config_path: str) -> None:
    """Starting point of the Python CLI."""

    if version:
        print(__version__)
        sys.exit(0)

    if config_path:
        os.environ['ESCAPE_CUSTOM_CONFIG_PATH'] = config_path
    title()


main.add_command(commands.init)
main.add_command(commands.scan)  #type: ignore
main.add_command(commands.check)
main.add_command(commands.cover)

"""Init."""

import json
import os.path
from pathlib import Path
from importlib import resources
import click

import inquirer  # type: ignore
from loguru import logger

from escape_cli import static
from escape_cli.static import CONFIG_FILENAME


@click.command()
@logger.catch
def init() -> None:
    """Init Escape Python CLI by creating escaperc file."""

    # This is how we open static files inside packages in Python
    with resources.open_text(static, 'supported-libs.json') as f:
        supported_libs = json.load(f)

    project_questions = [inquirer.Text(name='key', message='Please enter the Escape project key')]

    project_answers = inquirer.prompt(project_questions)
    answers = {'project': project_answers}

    discover_questions = [inquirer.List(name='httpLib', choices=supported_libs['httpLib'].keys(), message='What HTTP library do you use for this project?')]

    discover_answers = inquirer.prompt(discover_questions)
    answers.update({'discover': discover_answers})

    logged_action = 'written'
    if os.path.isfile(CONFIG_FILENAME):
        with open(CONFIG_FILENAME) as f:
            existing_config = json.load(f)
            for key, val in existing_config.items():
                if key not in answers:
                    answers[key] = val
            logged_action = 'updated'

    # On the contrary this will be saved in the local folder where the CLI will be executed
    with open(CONFIG_FILENAME, 'w') as f:
        json.dump(answers, f, indent=2)
        logger.success(f'Config file {logged_action}: {Path(CONFIG_FILENAME).resolve()}')

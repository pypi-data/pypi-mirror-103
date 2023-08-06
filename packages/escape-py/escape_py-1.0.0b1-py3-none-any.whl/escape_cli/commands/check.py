#!/usr/bin/env python

"""Module that checks the collected transactions.json file."""

import json
from importlib import resources

import click
from loguru import logger
from pydash import py_

from escape_cli import static

from escape_cli.static import TRANSACTIONS_PATH


def model_check(transaction: dict, key: str, model: dict) -> None:
    """Check the `transaction[key]` if compliant with the `model` description."""

    value = transaction[key]

    if 'type' in model:
        assert isinstance(value, eval(model['type'])), f'["req"]["{key}"]: Wrong type for value "{value}". Expected "{model["type"]}", got "{type(value)}"'  # pylint: disable=eval-used

    if 'enum' in model:
        value = value.lower()
        assert value in model['enum'], f'["req"]["{key}"]: Value "{value}" is not in enum "{model["enum"]}"'

    if 'special' in model:
        if key == 'body':
            content_type = py_.get(transaction['headers'], 'Content-Type') or py_.get(transaction['headers'], 'content-type')

            if content_type in ['application/json', 'application/x-www-form-urlencoded', None]:
                assert isinstance(value, dict), f'["req"]["{key}"]: Wrong body type for Content-Type {content_type}. Expected "dict", got "{type(value)}"'
            else:
                assert isinstance(value, str), f'["req"]["{key}"]: Wrong body type for Content-Type {content_type}. Expected "str", got "{type(value)}"'

        if key == 'parameters':
            for path_params in value.values():
                assert isinstance(path_params, str), f'["req"]["{key}"]: Wrong parameter type. Expected "str", got "{type(path_params)}"'


@click.command()
@logger.catch
def check() -> None:
    """Assert that transaction.json is valid."""

    with open(TRANSACTIONS_PATH, 'r') as f:
        transactions = json.load(f)

    with resources.open_text(static, 'models.json') as f:
        models = json.load(f)

    for i, transaction_exchange in enumerate(transactions):  # transaction_exchange should be a dict {req:…, res:…}
        try:
            for transaction_type in models:  # transaction_type is either 'req' or 'res'
                assert transaction_type in transaction_exchange, f': No "{transaction_type}"'

                for key, model in models[transaction_type].items():
                    assert key in transaction_exchange[transaction_type], f'["req"]: No "{key}" in req'
                    model_check(transaction_exchange[transaction_type], key, model)

        except AssertionError as e:
            logger.warning(f'{i}: transaction{e}')

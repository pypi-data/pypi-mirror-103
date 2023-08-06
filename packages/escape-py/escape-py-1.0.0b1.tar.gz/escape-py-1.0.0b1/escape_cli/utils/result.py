"""Utils to save patching results."""

import json

from loguru import logger

from escape_cli.utils.custom_types import Transaction
from escape_cli.static.constants import TRANSACTIONS_PATH


def save_transaction(result: Transaction) -> None:
    """Save request and response informations in the transactions file."""

    # Check if the result is valid
    for key in ['req', 'res', '_identifier']:
        if key not in result.keys():
            logger.warning(f'\n{key} is not in the result')
            return

    # Instead of reloading the entire file each time, we just append the "serialized dict" + a "," to the file.
    with open(TRANSACTIONS_PATH, 'a') as f:
        f.write(f'{json.dumps(dict(result))},')

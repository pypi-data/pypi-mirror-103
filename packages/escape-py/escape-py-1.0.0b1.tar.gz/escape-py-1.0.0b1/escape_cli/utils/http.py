"""Utils to manipulate HTTP Requests."""

import datetime
from typing import Union

from loguru import logger

from simplejson import dumps


def parse_dates(dct: dict, date_format: str = '%Y-%m-%dT%H:%M:%S.%fZ') -> dict:
    """Parses string dates of a `dict` to a Python datetime `date_format`."""
    for key, value in dct.items():
        if isinstance(value, str) and value.endswith('Z'):  # TODO: Here I don't understand the regex
            try:
                dct[key] = datetime.datetime.strptime(value, date_format)
            except ValueError as e:
                logger.warning(f'Coul not parse date "{value}": {e}')

    return dct


def serialize_dates(obj: tuple[datetime.datetime, datetime.date]) -> str:
    """Serializes dates in `obj` to backend-readable date strings."""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()  # type: ignore

    raise TypeError('Type %s is not serializable' % type(obj))


def prepare_request_data(data: Union[dict, str]) -> str:  # pylint: disable=unsubscriptable-object
    """Clean `data` dictionnary and format it for to send with Python `requests` module.

    Python dicts might contains some non-json-serializable data such as NaNs which we must remove before sending to backend.
    """

    if isinstance(data, dict):
        data = {k: data[k] for k in data if not isinstance(k, (int, float))}
        data = dumps(data, default=serialize_dates, ignore_nan=True)

    return data.replace(r'\u0000', '')

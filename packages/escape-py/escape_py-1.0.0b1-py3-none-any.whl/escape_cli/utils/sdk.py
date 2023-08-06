"""Escape Intelligence SDK used to communicate with Escape Backend using project tokens. This SDK have limited capabilities:

- Edit a project
- Create, update and add observed transactions to runs
- Create alerts
"""

import json
import socket
import requests

from loguru import logger
from pydash import py_

from escape_cli.static.constants import INFOS_PATH
from escape_cli.utils.http import prepare_request_data, parse_dates, serialize_dates
from escape_cli.utils.vcs import get_vcs_infos
from escape_cli import __version__ as cli_version

HEADERS = {'content-type': 'application/json'}


def raise_for_status(response: requests.Response) -> None:
    """Raise error when HTTP code is not 200 OK."""
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f'{e}. {py_.get(response.json(), "data", default="")}')


@logger.catch
class EscapeIntelligenceSDK:

    """Escape API SDK dedicated to use in intelligence contexts.

    Authenticates using project Key.
    """

    def __init__(self, uri: str = ''):
        """Creates a new IntelligenceSDK using a project URI
        ex: uri='https://app.escape.tech/2865e0e37546e069bfa65b06d74b6e8c2b0650d5'
        TODO: Use urllib.parse.urlparse here
        """

        protocol, address = uri.split('://')
        hostname, project_key = address.split('/')

        self.base_url = f'{protocol}://{hostname}'
        self.project_key = project_key

    def update_project(self, project_data: dict, options: dict = None) -> dict:
        """Update the related project using the `project_data` given as argument."""

        options = options or {}

        response = requests.put(f'{self.base_url}/intelligence/{self.project_key}/project', headers=HEADERS, data=prepare_request_data(project_data), **options)

        raise_for_status(response)

        return response.json(object_hook=parse_dates)

    def create_run(self, options: dict = None) -> dict:
        """Create a run with `run_data` that will be automatically linked to current project."""

        options = options or {}
        run_data = {'hostname': socket.gethostname(), 'status': 'running:scan'}  # pylint: disable=no-member
        run_data.update(get_vcs_infos())
        run_data.update({'cli_version': cli_version})

        response = requests.post(f'{self.base_url}/intelligence/{self.project_key}/runs', headers=HEADERS, data=prepare_request_data(run_data), **options)

        raise_for_status(response)
        run = response.json(object_hook=parse_dates)

        with open(INFOS_PATH, 'w') as f:
            json.dump(run, f, default=serialize_dates)
            logger.success(f'Run infos saved: {INFOS_PATH}')

        return response.json(object_hook=parse_dates)

    def get_run(self, uuid: str, options: dict = None) -> dict:
        """Get a run using it's `uuid`."""
        options = options or {}

        response = requests.get(f'{self.base_url}/intelligence/{self.project_key}/runs/{uuid}', headers=HEADERS, **options)

        raise_for_status(response)

        return response.json(object_hook=parse_dates)

    def add_transactions_to_run(self, uuid: str, transactions: list, options: dict = None) -> dict:
        """Add a `transaction` to a run using it's `uuid`."""

        options = options or {}

        response = requests.post(f'{self.base_url}/intelligence/{self.project_key}/runs/{uuid}/transactions', headers=HEADERS,
                                 data=prepare_request_data({'transactions': transactions}), **options)

        raise_for_status(response)

        return response.json(object_hook=parse_dates)

    def add_endpoints_to_run(self, uuid: str, endpoints: list, options: dict = None) -> dict:
        """Add `enpoints` to a run using it's `uuid`."""

        options = options or {}

        response = requests.post(f'{self.base_url}/intelligence/{self.project_key}/runs/{uuid}/endpoints', headers=HEADERS,
                                 data=prepare_request_data({'endpoints': endpoints}), **options)

        raise_for_status(response)

        return response.json(object_hook=parse_dates)

    def add_coverage_to_run(self, uuid: str, coverage: list, options: dict = None) -> dict:
        """Add a `coverage` to a run using it's `uuid`."""

        options = options or {}

        response = requests.post(f'{self.base_url}/intelligence/{self.project_key}/runs/{uuid}/coverage', headers=HEADERS,
                                 data=prepare_request_data({'coverage': coverage}), **options)

        raise_for_status(response)

        return response.json(object_hook=parse_dates)

    def add_alerts_to_run(self, uuid: str, alert_data: dict, options: dict = None) -> dict:
        """Add an `alert` to a run using it's `uuid`."""

        options = options or {}

        response = requests.post(f'{self.base_url}/intelligence/{self.project_key}/runs/{uuid}/alerts', headers=HEADERS, data=prepare_request_data(alert_data),
                                 **options)

        raise_for_status(response)

        return response.json(object_hook=parse_dates)

    def generate_run_openapi_spec(self, uuid: str, options: dict = None) -> dict:
        """Generate and return the OpenAPI specification for the run identified by its `uuid` using the transactions it contains."""

        options = options or {}

        response = requests.patch(f'{self.base_url}/intelligence/{self.project_key}/runs/{uuid}/generate-openapi', headers=HEADERS, **options)

        raise_for_status(response)

        return response.json(object_hook=parse_dates)

    def update_run(self, uuid: str, run_data: dict, options: dict = None) -> dict:
        """Update the related project using the `project_data` given as argument."""

        options = options or {}

        response = requests.put(f'{self.base_url}/intelligence/{self.project_key}/runs/{uuid}', headers=HEADERS, data=prepare_request_data(run_data), **options)

        raise_for_status(response)

        return response.json(object_hook=parse_dates)

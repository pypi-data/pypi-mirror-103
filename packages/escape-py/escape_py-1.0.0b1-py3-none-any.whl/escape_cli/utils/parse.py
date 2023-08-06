"""Parsing modules."""

import re
import json
from uuid import UUID
from typing import Any, Union

from loguru import logger

from escape_cli.utils.custom_types import Parameter


def parse_parameters(raw_params: dict[str, Any]) -> dict[str, str]:
    """Parse potential uuid values in parameters."""

    parameters = {}
    for key in raw_params:
        value = raw_params[key]
        if isinstance(value, UUID):
            parameters[key] = value.hex
            continue

        if not isinstance(value, str):
            try:
                parameters[key] = str(value)
                continue
            except UnicodeDecodeError:
                logger.error(f'Param in url cannot be converted into string: {key}: {value}')

        parameters[key] = value

    return parameters


def parse_body(raw_body: Union[str, bytes], content_type: str) -> Union[str, dict]:
    """Parse body into json when content_type is application/json."""

    if not content_type:
        return {}

    decoded_body = raw_body.decode('utf-8') if isinstance(raw_body, bytes) else raw_body

    if 'application/json' in content_type:
        try:
            parsed_body = json.loads(decoded_body)
            return parsed_body
        except json.decoder.JSONDecodeError:
            return 'Invalid JSON: ' + decoded_body
    else:
        return decoded_body


def format_endpoint_to_open_api_spec(raw_path: str) -> str:
    """Format the path parameters according to the Open API Spec."""

    # Possible forms that can take the params in the path
    param_patterns = [r'\^?\(\?P\<[^>]+\>[^)]*\)', r'\<[^>]+\>']
    open_api_path = raw_path

    for regex in param_patterns:
        for raw_param in re.findall(regex, open_api_path):
            # Extract the name of the param in path
            param = re.findall(r'\<(?:.+:)?([^>]+)\>', raw_param)[0]

            # Update the format of the param according to the open api spec
            open_api_path = open_api_path.replace(raw_param, '{' + param + '}')

    # Remove some special characters
    if open_api_path[-1] in ['$', '/'] and open_api_path != '/':
        open_api_path = open_api_path[:-1]

    if open_api_path[0] != '/':
        open_api_path = '/' + open_api_path

    return open_api_path


def find_params(path: str, regex: str = '') -> list[Parameter]:
    """Find name, type and pattern of params in path."""

    parameters: dict[str, Parameter] = {}

    # Find type of the params in path
    for raw_param in re.findall(r'\<(.*?)\>', path):
        splitted_params = raw_param.split(':')
        name = splitted_params[-1]

        new_param: Parameter = {'name': name}
        if len(splitted_params) == 2:
            new_param['type'] = splitted_params[0]
        parameters[name] = new_param

    # Find regex of the params in path
    for (name, pattern) in re.findall(r'\(\?P<([^>]+)>([^)]+)\)', regex):

        if name not in parameters.keys():
            parameters[name] = {'name': name}

        parameters[name]['pattern'] = pattern

    return list(parameters.values())


def get_identifier(raw_route: str, method: str) -> str:
    """Format the identifier shared in common with the endpoints and the transactions."""
    method = method.lower()
    route = raw_route.strip('^/')
    return f'{method}<>/{route}'

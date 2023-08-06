"""Main."""

import json

from flask import request, Response, Flask
from escape_cli.utils.result import save_transaction
from escape_cli.utils.parse import find_params, parse_parameters, format_endpoint_to_open_api_spec, get_identifier
from escape_cli.static.constants import ENDPOINTS_PATH

from escape_cli.utils.custom_types import Endpoint, Transaction


def flask_middleware(app: Flask) -> None:
    """Add a middleware called after each request."""

    @app.before_first_request
    def detect_routes() -> None:  # pylint: disable=unused-variable
        """Detect registered routes."""

        endpoints: list[Endpoint] = []
        existing_routes = []  # avoid duplicate endpoints

        for rule in app.url_map.iter_rules():
            rule_path = str(rule)
            handler = rule.endpoint
            parameters = find_params(rule_path)
            open_api_path = format_endpoint_to_open_api_spec(rule_path)
            if open_api_path not in existing_routes:
                existing_routes.append(open_api_path)

                for method in rule.methods - {'HEAD', 'OPTIONS'}:
                    endpoints.append({
                        'openApiPath': open_api_path,
                        'method': method,
                        'parameters': parameters,
                        'handler': handler,
                        '_identifier': get_identifier(str(rule), method)})

        with open(ENDPOINTS_PATH, 'w') as f:
            json.dump(endpoints, f)

    @app.after_request
    def detect_transaction(response: Response) -> Response:  # pylint: disable=unused-variable
        """Detect transactions."""
        save_req_and_res_information(response)
        return response


def save_req_and_res_information(response: Response) -> None:
    """Fetch usefull information from requests and responses Save it in the transactions file."""

    response.direct_passthrough = False

    result: Transaction = {
        'req': {
            'protocol': request.scheme,
            'host': request.host,
            'route': request.path,
            'method': request.method,
            'parameters': parse_parameters(request.view_args) if request.view_args else {},
            'query': dict(request.args),
            'originalUrl': request.path,
            'headers': dict(request.headers),
            'cookies': dict(request.cookies),
            'httpVersion': '',
            'body': dict(request.form)},
        'res': {
            'statusCode': response.status_code,
            'messageCode': response.status.split(' ')[1],
            'headers': dict(response.headers),
            'body': response.get_json() if response.is_json else response.data.decode('utf-8')},
        '_identifier': get_identifier(str(request.url_rule), request.method)}

    save_transaction(result)

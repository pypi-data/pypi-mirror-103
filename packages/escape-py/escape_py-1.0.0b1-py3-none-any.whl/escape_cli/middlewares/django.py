"""Django middleware."""

import os
import json
from uuid import UUID
from typing import Union, Callable

from loguru import logger
from django.http import HttpRequest, HttpResponse  # type: ignore
from django.urls import get_resolver, URLPattern, URLResolver  # type: ignore

from escape_cli.static.constants import METHODS_PATH, ENDPOINTS_PATH
from escape_cli.utils.custom_types import Endpoint, Parameter, Transaction
from escape_cli.utils.result import save_transaction
from escape_cli.utils.parse import find_params, get_identifier, parse_body, parse_parameters, format_endpoint_to_open_api_spec

HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']


class GetRequestAndResponseInformation():

    """Fetch usefull information from requests and responses Save it in the transactions file."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.result: Transaction = {}
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Fetch the response after the view is called."""

        response = self.get_response(request)

        match = request.resolver_match
        if match:
            self.result['_identifier'] = get_identifier(match.route, request.method)
        else:
            logger.warning(f'Cannot resolve route of {request.path}')

        res_headers = dict(response.items())
        res_body = parse_body(response.getvalue(), res_headers['Content-Type'])

        self.result['res'] = {'statusCode': response.status_code, 'messageCode': response.reason_phrase, 'headers': dict(response.items()), 'body': res_body}
        save_transaction(self.result)

        return response

    def process_view(self, request: HttpRequest, _view_func: Callable, _view_args: list, view_kwargs: dict) -> None:
        """Fetch the request before the view is called."""

        # Used to ensure this code is ran only once
        if os.environ['ESCAPE_ENDPOINTS_MAPPED'] == 'False':
            os.environ['ESCAPE_ENDPOINTS_MAPPED'] = 'True'

            endpoints: list[Endpoint] = []

            endpoints = save_endpoints(endpoints, [get_resolver()])
            with open(ENDPOINTS_PATH, 'w') as f:
                json.dump(endpoints, f)

        req_headers = dict(request.headers)
        req_body = parse_body(request.body, request.content_type)
        req_parameters = parse_parameters(view_kwargs)

        self.result['req'] = {
            'protocol': request.scheme,
            'host': request.get_host(),
            'route': request.path,
            'method': request.method,
            'parameters': req_parameters,
            'query': dict(request.GET.items()),
            'originalUrl': request.path,
            'headers': req_headers,
            'cookies': request.COOKIES,
            'httpVersion': request.META['SERVER_PROTOCOL'].split('/')[1],
            'body': req_body}


def save_endpoints(endpoints: list[Endpoint], resolvers: list[Union[URLPattern, URLResolver]], endpoint_start: str = '', parameters: list[Parameter] = None,
                   existing_routes: list[str] = None) -> list[Endpoint]:
    """Recursive function.

    Look throw the urls and save the endpoints.
    """

    existing_routes = existing_routes or []
    parameters = parameters or []

    with open(METHODS_PATH) as f:
        methods_dict = json.load(f)

    for url in resolvers:
        new_parameters = parameters + find_params(str(url.pattern), url.pattern.regex.pattern)
        absolute_endpoint = f'{endpoint_start}{url.pattern}'.lstrip('^')
        if isinstance(url, URLResolver):
            endpoints = save_endpoints(endpoints, url.url_patterns, absolute_endpoint, new_parameters, existing_routes)
        elif isinstance(url, URLPattern):
            open_api_path = format_endpoint_to_open_api_spec(absolute_endpoint)

            if open_api_path not in existing_routes:  # Avoid duplicate endpoints
                existing_routes.append(open_api_path)

                handler = f'{url.callback.__module__}.{url.callback.__name__}'
                allowed_methods = HTTP_METHODS  # By default, all methods are allowed on every route in Django
                django_decorated = False
                if handler in methods_dict:  # But allowed methods can (very recommended) be restricted by @django.views.decorators.http.require_X decorator
                    allowed_methods = methods_dict[handler]
                    django_decorated = True

                for method in allowed_methods:
                    endpoints.append({
                        'openApiPath': open_api_path,
                        'method': method,
                        'parameters': new_parameters,
                        'handler': handler,
                        'djangoDecorated': django_decorated,
                        '_identifier': get_identifier(absolute_endpoint, method)})

    return endpoints


class UUIDEncoder(json.JSONEncoder):

    """Helper class to save value of uuid parameters."""

    def default(self, obj):  # type: ignore # pylint: disable=arguments-differ
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return super().default(obj)

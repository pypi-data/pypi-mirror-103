# pylint: disable=inherit-non-class, too-few-public-methods

"""Custom Data Type to represent Objects for the Python CLI."""

from typing import TypedDict, Union


class Parameter(TypedDict, total=False):

    """Parameter in Url."""

    name: str
    pattern: str
    type: str
    required: bool


class Endpoint(TypedDict, total=False):

    """Route Endpoint."""

    openApiPath: str
    method: str
    parameters: list[Parameter]
    handler: str
    djangoDecorated: bool
    _identifier: str


class TransactionRequest(TypedDict):

    """Api Transaction Request."""

    protocol: str
    host: str
    route: str
    method: str
    parameters: dict[str, str]
    query: dict[str, str]
    originalUrl: str
    headers: dict[str, str]
    cookies: dict[str, str]
    httpVersion: str
    body: Union[str, dict]


class TransactionResponse(TypedDict):

    """Api Transaction Response."""

    statusCode: int
    messageCode: str
    headers: dict[str, str]
    body: Union[str, dict]


class Transaction(TypedDict, total=False):

    """Api Transaction."""

    req: TransactionRequest
    res: TransactionResponse
    _identifier: str

"""Python environment module for Flask."""

import flask

from escape_cli.executor import execute
from escape_cli.middlewares import flask_middleware


def flask_patch(entrypoint: str) -> None:
    """The `filename` is the file entrypoint executed in the controlled Python environment."""

    class NewClass(flask.Flask):

        """Patched Flask class."""

        def __init__(self, *args, **kwargs) -> None:  # type: ignore
            """Overriden constructor."""
            super().__init__(*args, **kwargs)
            flask_middleware(self)

    flask.Flask = NewClass  # type: ignore

    as_module = True

    execute(entrypoint, as_module)

"""Cover."""
import os
import sys
import click
from loguru import logger

from escape_cli.static.constants import CONFIG_FILENAME, COVERAGE_NAMESPACE, DISCOVER_NAMESPACE
import escape_cli.utils.coverage as coverage
from escape_cli.utils.config import get_config, patch_and_run


@click.command()
@click.argument('entrypoint', nargs=-1, required=True, type=str)
@logger.catch
def cover(entrypoint: str) -> None:
    """Start a Cover."""

    config = get_config(os.environ.get('ESCAPE_CUSTOM_CONFIG_PATH', CONFIG_FILENAME), DISCOVER_NAMESPACE)
    if not config:
        return

    coverage_config = config[DISCOVER_NAMESPACE].get(COVERAGE_NAMESPACE, {})

    result = patch_and_run(' '.join(entrypoint), config)
    if not result:
        return

    coverage_data = coverage.run_coverage(result['transactions'], result['endpoints'], coverage_config)
    _, filtered_coverage, coverage_stats, _ = coverage_data

    try:
        coverage.display_coverage_reports(filtered_coverage, coverage_stats, coverage_config)
    except ValueError as err:
        logger.error(err)
        sys.exit(1)

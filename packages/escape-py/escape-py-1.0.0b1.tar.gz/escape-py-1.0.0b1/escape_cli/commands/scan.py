"""Scan."""

import os
import sys
import click
from loguru import logger

import escape_cli.utils.coverage as coverage
from escape_cli.utils.sdk import EscapeIntelligenceSDK
from escape_cli.static.constants import CONFIG_FILENAME, COVERAGE_NAMESPACE, DISCOVER_NAMESPACE, PROJECT_NAMESPACE
from escape_cli.utils.config import get_config, patch_and_run


@click.command()
@click.argument('entrypoint', nargs=-1, required=True, type=str)
@logger.catch
def scan(entrypoint: str) -> None:
    """Start a Scan."""

    config = get_config(os.environ.get('ESCAPE_CUSTOM_CONFIG_PATH', CONFIG_FILENAME), DISCOVER_NAMESPACE)
    if not config:
        return

    project_uri = config[PROJECT_NAMESPACE]['key']
    coverage_config = config[DISCOVER_NAMESPACE].get(COVERAGE_NAMESPACE, {})

    # Create run
    logger.info('Creating run')
    client = EscapeIntelligenceSDK(project_uri)
    run = client.create_run()  # pylint: disable=no-member
    logger.info(f'Run created with uuid {run["uuid"]}')

    os.environ['ESCAPE_RUN_UUID'] = run['uuid']
    os.environ['ESCAPE_COMMAND_INVOKED'] = 'scan'

    try:
        result = patch_and_run(' '.join(entrypoint), config)
        if not result:
            return

        coverage_data = coverage.run_coverage(result['transactions'], result['endpoints'], coverage_config)
        coverage_result, filtered_coverage, coverage_stats, enriched_endpoints = coverage_data

        # Send the transactions to the backend
        logger.info('Saving HTTP messages into the DB')
        client.add_transactions_to_run(run['uuid'], transactions=result['transactions'])

        logger.info('Generating OpenAPI specification')
        client.generate_run_openapi_spec(run['uuid'])

        logger.info('Saving the coverage in the DB')
        client.add_coverage_to_run(run['uuid'], coverage=coverage_result)

        logger.info('Saving the endpoints in the DB')
        client.add_endpoints_to_run(run['uuid'], endpoints=enriched_endpoints)

        logger.info('Saving run metadata')
        client.update_run(run['uuid'], {'status': 'success:scan', **coverage_stats})
        coverage.display_coverage_reports(filtered_coverage, coverage_stats, coverage_config)

    # Exit nicely if coverage is failed
    except Exception as err:
        client.update_run(run['uuid'], {'status': 'failed:scan', **coverage_stats})
        logger.error(err)
        sys.exit(1)

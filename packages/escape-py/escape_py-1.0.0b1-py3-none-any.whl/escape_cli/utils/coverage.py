"""Compute the converage at the end of the process."""
import os
import re
from typing import Any, Dict, List, Tuple
from datetime import datetime

from termcolor import cprint

CoverageResults = Tuple[list, List[Dict[str, Any]], Dict[str, float], list]


def compute_coverage_from_transactions(transactions: list, endpoints: list, options: dict) -> dict:
    """This function is responsible for computing the raw coverage object This is a list of descriptors with the following structure :

    - path -> the path with the format open api
    - method -> the method of the endpoint
    - statuses -> the list of statuses covered by tests for this endpoint
    - covered -> a boolean describing if this route is covered by at least one test
    - filtered -> a boolean describing if the route is filtered by user options
    """

    coverage = {}

    ignored_paths = options.get('ignoredPaths', [])

    def is_filtered(path: str) -> bool:
        """Determined if coverage result is filtered or not."""
        filtered = False
        for ignored_path in ignored_paths:
            matches = re.findall(re.compile(ignored_path), path)
            if len(matches) > 0:
                filtered = True
                break
        return filtered

    for endpoint in endpoints:
        statuses = [transaction['res']['statusCode'] for transaction in transactions if transaction['_identifier'] == endpoint['_identifier']]
        statuses = list(dict.fromkeys(statuses))  # Remove duplicate keys
        coverage[endpoint['_identifier']] = {
            'path': endpoint['openApiPath'],
            'method': endpoint['method'],
            'statuses': statuses,
            'covered': bool(statuses),
            'filtered': is_filtered(endpoint['openApiPath'])}

    return coverage


def serialize_coverage(raw_coverage: dict) -> Tuple[List[Dict[str, Any]], Dict[str, float]]:
    """Prepare the coverage result for reporting.

    - compute the coverage rate
    """

    # Turn the row coverage into a list for computation efficiency
    raw_coverage_list = raw_coverage.values()

    filtered_coverage = list(filter(lambda entry: entry['filtered'] is False, raw_coverage_list))
    filtered_coverage.sort(key=lambda entry: entry['path'])

    n_endpoints_covered = 0
    n_endpoints = len(filtered_coverage)

    for entry in filtered_coverage:
        if entry['covered']:
            n_endpoints_covered += 1

    coverage_stats = {'n_endpoints': n_endpoints, 'n_endpoints_covered': n_endpoints_covered, 'coverage_rate': n_endpoints_covered / n_endpoints}

    return filtered_coverage, coverage_stats


def _center_between(text: str, padding_char: str, n_columns: int) -> str:
    """Util for displaying a centered text."""
    border_size = (n_columns - len(text)) // 2
    result = padding_char*border_size + text + padding_char*border_size
    if len(result) < n_columns:
        result += padding_char
    return padding_char*border_size + text + padding_char*border_size


def display_coverage_reports(data: list, stats: dict, options: dict) -> None:
    """Display the reports of the coverage based on reporters specified in options."""

    n_columns = os.get_terminal_size().columns
    sep = '=' * n_columns

    global_color = 'green'
    should_raise = False
    threshold = options.get('threshold', None)
    reporters = options.get('reporters', ['text', 'text-summary'])
    coverage_percentage = stats['coverage_rate'] * 100

    if threshold:
        below_coverage = stats['coverage_rate'] < threshold

        global_color = 'red' if below_coverage else 'green'
        should_raise = below_coverage

    # title
    cprint(_center_between(' Coverage report provided by Escape ', '=', n_columns), global_color, attrs=['bold'])
    cprint(f'Generated on : {datetime.now().isoformat()}', 'white', attrs=['bold'])
    cprint(sep, global_color, attrs=['bold'])

    if 'text' in reporters:
        # endpoints
        print()

        current_fragment = None

        def eventually_update_current_fragment(entry_path: str, current_fragment: str = None) -> str:
            """Print a line separator for root path changes in the report."""
            fragments = entry_path.split('/')
            print(entry_path)
            fragments = fragments or ['']
            if fragments[0] != current_fragment:
                current_fragment = fragments[0]
                section_title = f' /{current_fragment} '
                cprint('-'*5 + section_title + '-' * (n_columns - 5 - len(section_title)), 'white')
            return current_fragment

        for entry in data:
            current_fragment = eventually_update_current_fragment(entry['path'], current_fragment)
            color = 'green' if entry['covered'] else 'red'
            cprint(f'{entry["method"]} {entry["path"]} : {", ".join(str(status) for status in entry["statuses"])}', color)

        print()

    # stats
    if 'text-summary' in reporters:
        cprint('='*5 + ' Summary ' + '=' * (n_columns - 5 - len(' Summary ')), global_color, attrs=['bold'])
        cprint(f'Routes covered : {stats["n_endpoints_covered"]}/{stats["n_endpoints"]} => {round(coverage_percentage, 2)}%', global_color)
        cprint('Per status :', global_color)
        cprint(sep, global_color, attrs=['bold'])

    if should_raise:
        raise ValueError(f'The route coverage is below expectation of {threshold}%. Received {round(coverage_percentage, 2)}%')


def run_coverage(transactions: list, endpoints: list, config: dict) -> CoverageResults:
    """Execute coverage computation and serialization."""
    coverage_result = compute_coverage_from_transactions(transactions, endpoints, config)
    filtered_coverage, coverage_stats = serialize_coverage(coverage_result)

    enriched_endpoints = endpoints.copy()
    for enpoint in enriched_endpoints:
        enpoint['coverage'] = coverage_result[enpoint['_identifier']]

    return list(coverage_result.values()), filtered_coverage, coverage_stats, enriched_endpoints

"""Constants."""

import os

CONFIG_FILENAME = '.escaperc.json'
PROJECT_NAMESPACE = 'project'
DISCOVER_NAMESPACE = 'discover'
COVERAGE_NAMESPACE = 'coverage'
ESCAPE_DIR = os.path.join(os.path.expanduser('~'), '.config', 'escape')
TRANSACTIONS_PATH = os.path.join(ESCAPE_DIR, 'transactions.json')
INFOS_PATH = os.path.join(ESCAPE_DIR, 'infos.json')
ENDPOINTS_PATH = os.path.join(ESCAPE_DIR, 'endpoints.json')
METHODS_PATH = os.path.join(ESCAPE_DIR, 'methods.json')

"""Small util file for retrieving vsc infos."""
import subprocess
from typing import Dict
from loguru import logger


def get_vcs_infos() -> Dict[str, str]:
    """Execute git command in a subprocess for retreving commit infos.

    Return a dict with versioning infos for git projects, and an empty dict otherwise
    """
    try:
        infos = subprocess.check_output(['git', 'log', '-n', '1', '--pretty=tformat:%H,%s,%aI,%ae']).strip().decode('ascii').split(',')
        branch_name = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('ascii')
        return {'commit_hash': infos[0], 'commit_msg': infos[1], 'commit_date': infos[2], 'commit_author': infos[3], 'current_branch': branch_name}
    except:  # pylint: disable=bare-except
        logger.warning('No VCS informations found. Assuming this is not a git repository')
        return {}

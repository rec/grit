from __future__ import absolute_import, division, print_function, unicode_literals

from . Dict import compose_on_keys
from . File import HOME, get_json
from . GitRoot import ROOT
from . Call import git

import os

# TODO: this should be a consequence of the default project.
DEFAULT_PROJECT_USER = 'ripple'

_KEYS = 'GIT_USER', 'USER', 'PROJECT_USER'

def get_project(**kwds):
    for line in git('remote', '-v', **kwds).splitlines():
        parts = line.split()
        if parts[0] == 'origin':
            return parts[1].split('/')[1].split('.')[0]


def _make_settings():
    dicts = [
        get_json(HOME, '.grit', '.grit'),
        os.environ,
    ]
    if ROOT:
        dicts.insert(0, get_json(ROOT, '.grit'))
    settings = compose_on_keys(_KEYS, dicts)
    settings['PROJECT'] = get_project()

    return settings

SETTINGS = _make_settings()
globals().update(SETTINGS)

USER = globals().get('GIT_USER') or USER
PROJECT_USER = globals().get('PROJECT_USER', DEFAULT_PROJECT_USER)

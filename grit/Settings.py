from __future__ import absolute_import, division, print_function, unicode_literals

from . Dict import compose_on_keys
from . File import HOME, get_json
from . GitRoot import ROOT

import os

DEFAULT_PROJECT = 'rippled'

# TODO: this should be a consequence of the default project.
DEFAULT_PROJECT_USER = 'ripple'

_KEYS = 'GIT_USER', 'PROJECT', 'USER', 'PROJECT_USER'

def _make_settings():
    dicts = [
        get_json(HOME, '.grit', '.grit'),
        os.environ,
    ]
    if ROOT:
        dicts.insert(0, get_json(ROOT, '.grit'))

    return compose_on_keys(_KEYS, dicts)

SETTINGS = _make_settings()
globals().update(SETTINGS)

USER = globals().get('GIT_USER') or USER
PROJECT = globals().get('PROJECT', DEFAULT_PROJECT)
PROJECT_USER = globals().get('PROJECT_USER', DEFAULT_PROJECT_USER)

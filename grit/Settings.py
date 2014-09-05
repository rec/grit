from __future__ import absolute_import, division, print_function, unicode_literals

from grit.File import raw_json
from grit.GitRoot import ROOT

import os

_KEYS = 'PROJECT', 'USER', 'PROJECT_USER'
_HOME = os.path.expanduser('~')
_DICTS = (
    raw_json(ROOT, '.grit'),
    raw_json(_HOME, '.grit', '.grit'),
    raw_json(_HOME, '.grit'),
    os.environ,
)

def _add_keys(keys):
    settings = {}

    for key in _KEYS:
        for i, d in enumerate(_DICTS):
            value = d.get(key)
            if value:
                globals()[key] = value
                settings[key] = value
                break
    return settings


SETTINGS = _add_keys(_KEYS)
PROJECT_USER = PROJECT_USER or USER

from __future__ import absolute_import, division, print_function, unicode_literals

from grit.Dict import compose_on_keys
from grit.File import HOME, get_json
from grit.GitRoot import ROOT

import os

_KEYS = 'PROJECT', 'USER', 'PROJECT_USER'
_DICTS = (
    get_json(ROOT, '.grit'),
    get_json(HOME, '.grit', '.grit'),
    get_json(HOME, '.grit'),
    os.environ,
)

SETTINGS = compose_on_keys(_KEYS, _DICTS)
globals().update(SETTINGS)

PROJECT_USER = PROJECT_USER or USER

from __future__ import absolute_import, division, print_function, unicode_literals

from grit.Dict import compose_on_keys
from grit.File import HOME, get_json
from grit.GitRoot import ROOT

import os

DEFAULT_PROJECT = 'BiblioPixel'

# TODO: this should be a consequence of the default project.
DEFAULT_PROJECT_USER = 'rec'

_KEYS = 'GIT_USER', 'PROJECT', 'USER', 'PROJECT_USER'
_DICTS = (
    get_json(ROOT, '.grit'),
    get_json(HOME, '.grit', '.grit'),
    os.environ,
)

SETTINGS = compose_on_keys(_KEYS, _DICTS)
globals().update(SETTINGS)

USER = globals().get('GIT_USER') or USER
PROJECT = globals().get('PROJECT', DEFAULT_PROJECT)
PROJECT_USER = globals().get('PROJECT_USER', DEFAULT_PROJECT_USER)

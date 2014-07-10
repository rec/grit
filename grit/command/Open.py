from __future__ import absolute_import, division, print_function, unicode_literals

import os
import platform
import random

from grit import Call
from grit import Git
from grit import Settings

HELP = """
    grit open [filename]

Open the filename as a Github URL in the browser.

Selects the first file that starts with filename.  If filename is missing,
opens the current directory in the browser.
"""

SAFE = True

_OPEN_COMMANDS = {
    'Darwin': 'open',
    'Linux': 'xdg-open',
}

_URL = 'https://github.com/{user}/{project}/tree/{branch}/{path}'

def open(filename=''):
    plat = platform.system()
    if not plat in _OPEN_COMMANDS:
        raise ValueError("Can't open a URL for platform.system() = " + plat)
    branch = Git.branch()
    full_path = os.getcwd()
    if filename:
        path, f = os.path.split(filename)
        full_path = os.path.join(full_path, path)
        if not os.path.exists(full_path):
            raise ValueError("Path %s doesn't exist." % full_path)
        if f:
            for p in os.listdir(full_path):
                if p.startswith(f):
                    full_path = os.path.join(full_path, p)
                    break
            else:
                raise ValueError("Can't find file matching " + filename)

    url = _URL.format(
        branch=Git.branch(),
        path=os.path.relpath(full_path, Git.root()),
        project=Settings.PROJECT,
        user=Settings.USER)
    Call.call('%s %s' % (_OPEN_COMMANDS[plat], url))

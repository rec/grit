from __future__ import absolute_import, division, print_function, unicode_literals

import re

VERSION = re.compile(r'\d+\.\d+\.\d+(?:-\w\d?)')

from grit import File
from grit import Git
from grit import Project

HELP = """
grit v[ersion] [<version-number>]
    Without an argument, prints the current project version number.
    With an argument, replaces the original version number with the argument.
"""

SAFE = True

def version(version_number=None):
    files = Project.settings('version')['files']
    if not version_number:
        for f in files:
            s = File.search(f, VERSION)
            if s:
                print(s)
                return
        print('ERROR: no version number found.')
    else:
        for f in files:
            File.subn(f, VERSION, version_number)
        Git.git('commit', '-am', 'Set version to %s' % version_number)

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re
import semver

VERSION = re.compile(r'\d+\.\d+\.\d+(?:-\w\d*)')

from grit.Args import ARGS
from grit import CommandList
from grit import File
from grit import Git
from grit import GitRoot
from grit import Project

HELP = """
grit v[ersion] [<version-number>]
    Without an argument, prints the current project version number.
    With an argument, replaces the original version number with the argument.
"""

SAFE = True

def version(version_number=None):
    root = GitRoot.root()
    files = Project.settings('version')['files']

    for f in files:
        old_version = File.search(f, VERSION)
        if old_version:
            break
    else:
        raise Exception('ERROR: no version number found.')

    if version_number == old_version:
        raise Exception('Version number is already %s' % old_version)
    if not version_number:
        version_number = semver.increment_string(old_version)
    if not CommandList.confirm('update version %s to %s' %
                               (old_version, version_number)):
        return
    for f in files:
        File.subn(os.path.join(root, f), VERSION, version_number)
    Git.git('commit', '-am', 'Set version to %s' % version_number)

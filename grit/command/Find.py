from __future__ import absolute_import, division, print_function, unicode_literals

import os
from os import getcwd
from os.path import basename, dirname, isdir, join

from grit import Call
from grit import File
from grit import Git
from grit import Project
from grit import Settings
from grit.command import Test
from grit.command import Remotes

HELP = """

    grit find prefix [-]

Prints the next directory in the current git project that contains a file that
starts with this prefix.

With optional -, prints the previous directory.

"""

SAFE = True

def _match(root, prefix):
    for dirpath, dirnames, filenames in os.walk(root):
        for d in dirnames:
            if d.startswith(prefix):
                yield os.path.join(dirpath, d)
        if not os.path.basename(dirpath).startswith(prefix):
            for f in filenames:
                if f.startswith(prefix):
                    yield dirpath
                    break

def find(prefix, suffix=''):
    root = Git.root()
    if not root:
        raise ValueError('There is no git repository here.')
    if prefix == '-':
        prefix, suffix = suffix, prefix
    forward = suffix != '-'
    if not prefix:
        raise ValueError('No file specified for find')
    settings = Project.settings('find')
    find_root = os.path.join(root, settings['find_root'])
    matches = sorted(list(_match(find_root, prefix)))

    if not matches:
        raise ValueError("Can't find files matching prefix " + prefix)
    try:
        index = matches.index(os.getcwd())
    except ValueError:
        print(matches[0] if forward else matches[-1])
    else:
        print(matches[(index + (1 if forward else -1)) % len(matches)])
#

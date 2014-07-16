from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

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
                d = os.path.join(dirpath, d)
                yield d, d
        if not os.path.basename(dirpath).startswith(prefix):
            for f in filenames:
                if f.startswith(prefix):
                    yield dirpath, os.path.join(f)
                    break

def _print_match(match, display_root):
    print(os.path.relpath(match[1], display_root), file=sys.stderr)
    print(match[0])

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
    display_root = os.path.join(root, settings['display_root'])
    matches = sorted(list(_match(find_root, prefix)))

    if not matches:
        raise ValueError("Can't find files matching prefix " + prefix)
    try:
        index = matches.index(os.getcwd())
    except ValueError:
        _print_match(matches[0] if forward else matches[-1], display_root)
    else:
        _print_match(matches[(index + (1 if forward else -1)) % len(matches)],
                     display_root)
#

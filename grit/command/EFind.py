from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

from grit import Call, File, GitRoot, Project
from grit.String import startswith
from grit.command import Test

HELP = """
grit efind prefix [original-file] [-]
    Prints the next directory in the current git project that contains a file
    that starts with this prefix.

    Specialized for emacs.

    With optional -, prints the previous directory.
"""

SAFE = True

def _match(root, prefix):
    for dirpath, dirnames, filenames in os.walk(root):
        for d in dirnames:
            if d.startswith(prefix):
                yield d, os.path.join(dirpath, d)
        if not startswith(os.path.basename(dirpath), (prefix)):
            for f in filenames:
                if startswith(f, prefix):
                    yield dirpath, os.path.join(dirpath, f)
                    break

def _print_match(match, display_root):
    print(os.path.relpath(os.path.join(*match), display_root), file=sys.stderr)
    print(match[0])

def find(*args):
    root = GitRoot.ROOT
    if not root:
        raise ValueError('There is no git repository here.')
    args = list(args)
    is_forward = '-' not in args
    if not is_forward:
        args.remove('-')

    if not args:
        raise ValueError('No file specified for find')

    if len(args) < 2:
        args.append(os.getcwd())

    prefix, current = args
    settings = Project.settings('find')
    find_root = os.path.join(root, settings['find_root'])
    display_root = os.path.join(root, settings['display_root'])
    matches = sorted(list(_match(find_root, prefix)))

    if not matches:
        raise ValueError("Can't find files matching prefix " + prefix)
    try:
        index = matches.index(os.getcwd())
    except ValueError:
        _print_match(matches[0] if is_forward else matches[-1], display_root)
    else:
        _print_match(matches[(index + (1 if is_forward else -1)) % len(matches)],
                     display_root)

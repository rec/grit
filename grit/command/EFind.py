from __future__ import absolute_import, division, print_function, unicode_literals

import bisect, sys, os

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

def match(root, prefix):
    paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        for d in dirnames:
            if d.startswith(prefix):
                paths.append(os.path.join(dirpath, d))
        for f in filenames:
            if startswith(f, prefix):
                paths.append(os.path.join(dirpath, f))
    return sorted(paths)


def efind(*args):
    args = list(args)
    is_forward = '-' not in args
    if not is_forward:
        args.remove('-')

    if '+' in args:
        args.remove('+')

    if not args:
        raise ValueError('No file specified for find')

    if len(args) < 2:
        args.append(os.getcwd())

    prefix, current = args
    current = current and os.path.abspath(current)

    root = GitRoot.root(current)
    if not root:
        raise ValueError('There is no git repository here.')

    settings = Project.settings('find')
    find_root = os.path.join(root, settings['find_root'])
    display_root = os.path.join(root, settings['display_root'])
    matches = match(find_root, prefix)

    if not matches:
        open('/tmp/error.txt', 'w').write('failed to find prefix ' + prefix + ' current ' + current)
        return

    if is_forward:
        index = bisect.bisect_right(matches, current)
    else:
        index = bisect.bisect_left(matches, current) - 1
    print(matches[index % len(matches)])

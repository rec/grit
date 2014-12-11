from __future__ import absolute_import, division, print_function, unicode_literals

from grit import Git
from grit.Args import ARGS
from grit.command.Rename import rename
from grit.command.Delete import delete

HELP = """
grit swap <branch1> <branch2>
    Swap <branch1> with <branch2>.

Both branches must exist.

"""

SAFE = True

SUFFIX = '-grit-tmp'

def swap(a, b):
    missing = set((a, b)) - set(Git.branches())
    if missing:
        raise Exception(
            'Non-existent branch%s: %s' %
            ('' if len(missing) == 1 else 'es', ' '.join(missing)))

    temp = a + '-' + b
    rename(a, temp)
    rename(b, a)
    rename(temp, b)

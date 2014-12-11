from __future__ import absolute_import, division, print_function, unicode_literals

from grit import Git
from grit.command import Delete
from grit.command import Fresh
from grit.Args import ARGS

HELP = """
grit rename <old-branch> <new-branch>
    Rename <old-branch> to <new-branch>.

Causes an error if <new-branch> exists unless -f is true.
"""

SAFE = True

def rename(old, new=None):
    if not new:
        old, new = Git.branch(), old
    if new in Git.branches():
        if not ARGS.force:
            raise Exception('The branch %s already exists.' % new)
        Delete.delete(new)
    Fresh.fresh(new, old)
    Delete.delete(old)

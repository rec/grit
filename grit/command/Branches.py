from __future__ import absolute_import, division, print_function, unicode_literals

import os

from grit import Call
from grit import Git
from grit import Project
from grit import Settings

BRANCH_COMMAND = 'git branch'

HELP = """
grit branches [prefix]
    List all git repositories and branches.

    If the current directory is contained in a git repository, list all branches
    in all repositories parallel to the current directory.

    If you aren't in a git repository, list all git branches in directories
    contained in the current directory.

    If prefix is set, only display branches in repositories that start with that
    prefix.

    The current branch in each repository is marked with a star (*).

    A branch which has a current pull request out is marked with an
    exclamation mark (!).
"""

SAFE = True

def branches(prefix='', *args):
    root = Git.root_container()
    pulls = set(Git.pull_branches(Settings.USER))

    if Project.settings('branches')['compact']:
        fname = ['']

        def before(f):
            fname[0] = os.path.basename(f)

        def callback(data):
            parts = ' '.join(p for p in ' '.join(data.splitlines()).split() if p)
            for p in pulls:
                parts = parts.replace(' ' + p, ' !' + p)

            parts = parts.replace('* ', '*')
            print('%-12s  %s' % (fname[0] + ':', parts))

        Call.for_each_directory(
            BRANCH_COMMAND, path=root, select=Git.select(prefix), before=before,
            callback=callback)
    else:
        def before(f):
            print('\n%s:' % os.path.basename(f))
        Call.for_each_directory(
            BRANCH_COMMAND, path=root, select=Git.select(prefix), before=before)

    if args:
        print('ERROR: arguments %s ignored' % ', '.join(args))

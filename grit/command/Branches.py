from __future__ import absolute_import, division, print_function, unicode_literals

import os

from grit.Args import ARGS
from grit import Call
from grit import Git
from grit import GitRoot
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
    root = GitRoot.root_container()
    pulls = Git.pull_branches()

    if not ARGS.expanded:
        fname = ['']

        def before(f):
            fname[0] = os.path.basename(f)

        def callback(data):
            parts = filter(None, data.splitlines())
            for i, p in enumerate(parts):
                branch = p.split()[-1]
                if branch in pulls:
                    branch += '(%s)' % pulls[branch]
                if p.startswith('*'):
                    branch = '*' + branch
                parts[i] = branch
            print('%-12s  %s' % (fname[0] + ':', ' '.join(parts)))

        Call.for_each_directory(
            BRANCH_COMMAND,
            path=root,
            select=GitRoot.select(prefix),
            before=before,
            callback=callback)
    else:
        def before(f):
            print('\n%s:' % os.path.basename(f))
        Call.for_each_directory(
            BRANCH_COMMAND,
            path=root,
            select=GitRoot.select(prefix),
            before=before)

    if args:
        print('ERROR: arguments %s ignored' % ', '.join(args))

from __future__ import absolute_import, division, print_function, unicode_literals

import os

from grit import Call
from grit import Git
from grit import Settings
from grit.command import Start
from grit.command import Test

HELP = """
grit clone <branch> [directory]
    Clones an existing branch of the current project.

    If the branch name is purely numeric, it's a pull request.

    If the branch name contains a :, it's a remote branch.  For account names,
    you can use either the full name or the remote nickname.

    If the directory name is not given, it adds a numeric suffix to the current
    directory.
"""

_ERROR = """
Unknown pull #%s.
Active pulls are %s.
"""

_ERROR_BRANCH = """
Unknown branch %s for user %s.
Existing branches are %s.
"""

_USER_COMMANDS = """
git fetch origin {branch}
git checkout {branch}
"""

_OTHER_COMMANDS = """
git fetch {user} {branch}
git checkout -b {branch} {user}/{branch}
"""

def parse_branch(branch):
    try:
        pull = int(branch)
    except:
        pass
    else:
        pulls = Git.pulls()
        if pull not in pulls:
            raise ValueError(_ERROR % (pull, ' '.join(sorted(pulls))))
        branch, _ = pulls[pull]
    if ':' in branch:
        return branch.split(':', 1)
    else:
        return Settings.USER, branch

def clone(branch, directory=''):
    user, branch = parse_branch(branch)
    cmds = _USER_COMMANDS if user == Settings.USER else _OTHER_COMMANDS
    cmds = cmds.format(branch=branch, user=user)
    branches = Git.branches(user)
    if branch not in branches:
        raise ValueError(_ERROR_BRANCH % (branch, user, ' '.join(branches)))

    directory = Start.clone(directory)
    Call.for_each(cmds, cwd=directory)

    # Test.run_test(directory)

from __future__ import absolute_import, division, print_function, unicode_literals

from grit import Call
from grit import Git
from grit import Settings
from grit.command import Remote

HELP = """
grit import <branch>
    Brings a branch into this client.

    If the branch name contains a :, it's a remote branch.  For account names,
    you can use either the full name or the remote nickname.
"""

_REMOTE = """
git fetch {user} {branch}
git checkout -b {branch} {user}/{branch}"""

SAFE = True

_LOCAL = 'git checkout {branch}'

_BRANCH_ERROR = 'User "{user}" has no branch "{branch}"'

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

def run_import(branch, **kwds):
    user, branch = parse_branch(branch)
    if branch not in Git.branch1es(user):
        raise ValueError(_BRANCH_ERROR.format(**locals()))
    if user == Settings.USER:
        command = _LOCAL
    else:
        Remote.remote(user, **kwds)
        command = _REMOTE
    Call.for_each(command.format(**locals()), **kwds)

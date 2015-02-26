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

def parse_branch(branch):
    try:
        pull_number = int(branch)
    except:
        pass
    else:
        pulls = Git.pulls()
        if pull_number not in pulls:
            raise ValueError(_ERROR % (pull, ' '.join(sorted(pulls))))
        pull = pulls[pull_number]
        branch = pull.branch
    if ':' in branch:
        return branch.split(':', 1)
    else:
        return Settings.USER, branch

def run_import(branch, **kwds):
    user, branch = parse_branch(branch)
    if branch not in Git.branch1es(user):
        raise ValueError(_BRANCH_ERROR.format(**locals()))
    if user == Settings.USER:
        Git.git('checkout', branch)
    else:
        Remote.remote(user, **kwds)
        Git.git('fetch', user, branch)
        Git.git('checkout', '-b', '/'.join([user, branch]))

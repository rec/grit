from __future__ import absolute_import, division, print_function, unicode_literals

from grit import Call
from grit.Args import ARGS
from grit import Git

HELP = """
grit amend
     Amend the last commit to include all changed files in this repo, keeping
     the original commit message.
"""

_AMEND = 'git commit --amend --no-edit -a'
_PUSH_F = 'git push -f'

def SAFE():
    print('Current branch is %s.' % Git.branch())


def amend():
    Call.call(_AMEND)
    if ARGS.force:
        Call.call(_PUSH_F)

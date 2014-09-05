from __future__ import absolute_import, division, print_function, unicode_literals

from grit import Call
from grit.Args import ARGS

HELP = """
grit amend
     Amend the last commit to include all changed files in this repo, keeping
     the original commit message.
"""

_AMEND = 'git commit --amend --no-edit -a'
_PUSH_F = 'git push -f'

SAFE = False

def amend():
    Call.call(_AMEND)
    if ARGS.push:
        Call.call(_PUSH_F)

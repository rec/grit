from __future__ import absolute_import, division, print_function, unicode_literals

from grit import Call

HELP = """
grit amend
     Amend the last commit to include all changed files in this repo, keeping
     the original commit message.
"""

_AMEND = 'git commit --amend --no-edit -a'
_PUSH_F = 'git push -f'

def amend(command=''):
    push = False
    if command:
        push = 'push'.startswith(command)
        if not push:
            raise Exception("Don't understand command", command,
                            "Available choices are: push")
    Call.call(_AMEND)
    if push:
        Call.call(_PUSH_F)

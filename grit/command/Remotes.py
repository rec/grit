from __future__ import absolute_import, division, print_function, unicode_literals

from grit import Call
from grit import Project
from grit import Settings

HELP = """
Add all the remotes listed in the project's remotes.json file.
"""

_REMOTE = """
git remote add {nickname} git@github.com:{user}/{project}.git
"""

SAFE = True

def remotes(cwd=None):
    code, value = Call.call_value('git remote', cwd=cwd)
    if code:
        raise Exception('No remotes, error code ' + str(code))

    remotes = set(value.split())
    for nickname, user in Project.settings('remotes').items():
        if nickname not in remotes:
            remote = _REMOTE.format(
                nickname=nickname, user=user, project=Settings.PROJECT)
            Call.call(remote, cwd=cwd)

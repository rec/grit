from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import urllib2

from grit import Call
from grit import Project
from grit import Settings

_REMOTE = """
git remote add {nickname} git@github.com:{user}/{project}.git
"""

SAFE = True

HELP = """
grit r[emote] <user> [<nickname>]

    Adds a remote branch for <user> named <nickname> (which defaults to <user>
    if it's empty.
"""

def _existing_remotes(cwd):
    return set(Call.call_raw('git remote', cwd=cwd).split())

def _add_remote(user, nickname, cwd):
    remote = _REMOTE.format(
        user=user, nickname=nickname, project=Settings.PROJECT)
    Call.call(remote, cwd=cwd)

def remote(user, nickname='', cwd=None):
    if user == 'all':
        assert not nickname
        remotes = Project.settings('remotes').items()
    else:
        remotes = [(nickname, user or user)]
    existing = _existing_remotes(cwd)
    for nickname, user in remotes:
        if nickname not in existing:
            _add_remote(user, nickname, cwd=cwd)

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import urllib2

from grit import Call
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
    nickname = nickname or user
    if nickname not in _existing_remotes(cwd):
        _add_remote(user, nickname, cwd)

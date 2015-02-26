from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import urllib2

from grit import Call
from grit import Project
from grit import Settings
from grit.Singleton import singleton

_REMOTE = """
git remote add {nickname} git@github.com:{user}/{project}.git
"""

SAFE = True

HELP = """
grit r[emote] <user> [<nickname>]

    Adds a remote branch for <user> named <nickname> (which defaults to <user>
    if it's empty.
"""

def existing_remotes(cwd):
    return set(Call.call_raw('git remote', cwd=cwd).split())

def add_remote(user, nickname, cwd=None, existing=None):
    existing = existing or existing_remotes(cwd)
    if nickname in existing:
        return
    remote = _REMOTE.format(
        user=user, nickname=nickname, project=Settings.PROJECT)
    Call.call(remote, cwd=cwd)

def remote(user='all', nickname='', cwd=None):
    if user == 'all':
        assert not nickname
        remotes = Project.settings('remotes').items()
    else:
        remotes = [(nickname, user or user)]
    existing = existing_remotes(cwd)
    for nickname, user in remotes:
        if nickname not in existing:
            add_remote(user, nickname, cwd=cwd, existing=existing)
    return remotes

@singleton
def remotes():
    return remote()

@singleton
def inverse():
    return dict((v, k) for (k, v) in remotes())

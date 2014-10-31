from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import random
import re

from grit import Git
from grit.command import Remote
from grit.command import Delete
from grit import Project
from grit import Settings

HELP = """
grit release
    Make a release branch.
"""

_MATCHER = re.compile(
    '(?:git branch new_branch_name|HEAD position was|HEAD position) '
    '([0-9a-f]{7})', re.MULTILINE)

SAFE = False

def _get_tag(line):
    m = _MATCHER.search(line)
    if m:
        return m.group(1)

def release(*requests):
    requests = list(requests)
    settings = Project.settings('git')  # TODO: This is empty and shouldn't be.
    base_branch = settings.get('base_branch', 'develop')
    next_branch = settings.get('next_branch', 'develop-next')
    pulls = Git.pulls()
    remotes = Remote.remote()
    inverse = dict((v, k) for (k, v) in remotes)

    if 'continue' in requests:
        requests.remove('continue')
    else:
        Delete.delete(next_branch)
        Git.copy_from_origin(base_branch, next_branch)

    for i, request in enumerate(requests):
        if request.isdigit():
            req = pulls.get(int(request))
            if req:
                requests[i] = req[0]
            else:
                raise ValueError('No such pull request #' + request)

    for request in requests:
        user, branch = request.split(':')
        nickname = inverse[user]
        if user == Settings.USER:
            nickname = 'origin'
        Git.git('fetch', nickname, branch)
        b1 = Git.git('checkout', nickname + '/' + branch)
        tag1 = _get_tag(b1)

        Git.git('rebase', '--preserve-merges', 'origin/' + next_branch)
        b2 = Git.git('checkout', next_branch)
        tag2 = _get_tag(b2)
        if (not tag2 or tag1):
            raise ValueError("Didn't find any tags")
        Git.git('merge', '--ff-only', tag2 or tag1)
        Git.git('push')

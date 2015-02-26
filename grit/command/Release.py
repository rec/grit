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

PASS = 'Passed'
NO_PASS = set(['API Change', 'Hold', 'Rebase', 'Submitted', 'Tx Change'])

def _get_tag(line):
    m = _MATCHER.search(line)
    if m:
        return m.group(1)

def _pull_accepted(pull):
    return PASS in pull.labels and not NO_PASS.intersection(pull.labels)

def release(*requests):
    requests = list(requests)
    settings = Project.settings('git')  # TODO: This is empty and shouldn't be.
    base_branch = settings.get('base_branch', 'develop')
    next_branch = settings.get('next_branch', 'develop-next')
    pulls = Git.pulls()
    remotes = Remote.remote()
    inverse = dict((v, k) for (k, v) in remotes)
    Git.rebase_abort()

    if 'continue' in requests:
        requests.remove('continue')
    else:
        Delete.delete(next_branch)
        Git.copy_from_remote(base_branch, next_branch)

    if 'all' in requests:
        requests = []
        for number, pull in sorted(Git.pulls().items()):
            if PASS in pull.labels and not NO_PASS.intersection(pull.labels):
                requests.append(pull.number)
        print(requests)
        return

    for i, request in enumerate(requests):
        pull = ''
        if request.isdigit():
            pull = int(request)
            req = pulls.get(pull)
            if req:
                request = req[0]
            else:
                raise ValueError('No such pull request #' + request)
        user, branch = Git.split_branch(request)
        requests[i] = user, branch, pull

    for request in requests:
        user, branch, pull = request
        print('------------------------------------------------' )
        print('%s:%s %s' % (user, branch, pull))
        try:
            nickname = inverse[user]
        except KeyError:
            Remote.add_remote(user, user)
            nickname = user
        if user == Settings.USER:
            nickname = 'origin'
        Git.git('fetch', nickname, branch)
        b1 = Git.git('checkout', nickname + '/' + branch)
        tag1 = _get_tag(b1)
        other_tag1 = Git.commit_id()
        assert tag1 == other_tag1

        Git.git('rebase', '--preserve-merges', 'origin/' + next_branch)
        b2 = Git.git('checkout', next_branch)
        tag2 = _get_tag(b2)
        if (not tag2 or tag1):
            raise ValueError("Didn't find any tags")
        Git.git('merge', '--ff-only', tag2 or tag1)
        Git.git('push')

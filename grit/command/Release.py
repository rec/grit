from __future__ import absolute_import, division, print_function, unicode_literals

import os
import random
import re
import time

from grit import Git
from grit import Project
from grit import Settings
from grit import String
from grit.Singleton import singleton
from grit.command import Delete
from grit.command import Open
from grit.command import Remote
from grit.command import Version

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

@singleton
def base_branch():
    return Project.settings('git').get('base_branch', 'develop')

@singleton
def next_branch():
    return Project.settings('git').get('next_branch', 'develop')

def _pull_accepted(pull):
    return PASS in pull.labels and not NO_PASS.intersection(pull.labels)

def git(*args):
    return Git.git(*args, print=None)

@Git.transaction
def _pull_request(pull):
    if pull.user == Settings.USER:
        nickname = 'origin'
    else:
        try:
            nickname = Remote.inverse()[pull.user]
        except KeyError:
            Remote.add_remote(pull.user, pull.user)
            nickname = pull.user

    commits = []
    git('fetch', nickname, pull.branch)
    git('checkout', nickname + '/' + pull.branch)
    git('rebase', '--preserve-merges', 'origin/' + next_branch())
    commit_id = Git.commit_id()

    git('checkout', next_branch())
    git('merge', '--ff-only', commit_id)
    git('push')

def _make_pulls(branches):
    if not branches:
        for number, pull in sorted(Git.pulls().items()):
            if _pull_accepted(pull):
                branches.append(number)

    pulls = Git.pulls()
    for branch in branches:
        branch = int(branch)
        try:
            yield pulls[branch]
        except KeyError:
            raise ValueError('No such pull request #' + branch)

def _print_short_pulls(message, pulls):
    if pulls:
        print(message)
        print('\n'.join(str(p) for p in pulls))

def _print_pulls(message, pulls):
    if pulls:
        print(message, String.join_words(pulls))

def release(*pulls):
    Git.rebase_abort()

    def remove_option(option):
        if option in pulls:
            pulls.remove(option)
            return True

    pulls = list(pulls)
    add_version = not remove_option('noversion')
    from_fresh = not remove_option('continue')
    open_commits = not remove_option('noopen')

    if from_fresh:
        Delete.delete(next_branch())
        Git.copy_from_remote(base_branch(), next_branch())

    pulls = list(_make_pulls(pulls))
    if not pulls:
        raise Exception('No pulls ready!')

    _print_pulls('Building release branch for', pulls)
    print()
    success = []
    failure = []
    exceptions = []
    for p in pulls:
        try:
            print(p.number, '...', sep='', end='')
            _pull_request(p)
        except Exception as e:
            failure.append(p.number)
            print('FAILED')
        else:
            print('ok')
            success.append(p.number)

    commits = Open.get_commits()
    _print_pulls('\Proposed new develop branch', commits, 'for pulls', success)
    _print_pulls('FAILED:', failure)

    if success:
        if add_version:
            Version.version()
            git('push')

        time.sleep(1)  # Make sure github gets it.

        if open_commits:
            Open.open('commits')
        if False:  # open_pull
            for p in success:
                Open.open(str(p))

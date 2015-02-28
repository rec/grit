from __future__ import absolute_import, division, print_function, unicode_literals

import os
import random
import re
import time

from grit import Cache
from grit import ChangeLog
from grit import Git
from grit import Project
from grit import Settings
from grit import String
from grit.Args import ARGS
from grit.Cache import cached
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

@cached
def base_branch():
    return Project.settings('git').get('base_branch', 'develop')

@cached
def next_branch():
    return base_branch() + '-next'

@cached
def working_branch():
    return base_branch() + '-working'

def _pull_accepted(pull):
    return PASS in pull.labels and not NO_PASS.intersection(pull.labels)

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
    printer = print if ARGS.verbose else None
    def git(*args):
        Git.git(*args, print=printer)

    git('fetch', nickname, pull.branch)
    git('checkout', nickname + '/' + pull.branch)
    git('rebase', '--preserve-merges', working_branch())
    commit_id = Git.commit_id()

    git('checkout', working_branch())
    git('merge', '--ff-only', commit_id)

def _make_pulls(branches):
    branches = list(branches)
    if not branches:
        for number, pull in sorted(Git.pulls().items()):
            if _pull_accepted(pull):
                branches.append(number)

    pulls = Git.pulls()
    try:
        return [pulls[int(b)] for b in branches]
    except KeyError:
        raise ValueError('Bad pull request in ' + str(branches))

def _print_long_pulls(message, pulls):
    if pulls:
        print(message)
        print('\n'.join(str(p) for p in pulls))

def _print_pulls(message, pulls):
    if pulls:
        print(message, String.join_words(pulls))

def _release(pulls):
    previous_pulls = set(ChangeLog.status()[1])
    if previous_pulls == set(p.number for p in pulls):
        if not ARGS.force:
            print('No change from', ChangeLog.status_line())
            return

    print(previous_pulls, pulls)

    Git.rebase_abort()
    Git.git('clean', '-f')
    Git.git('reset', '--hard', 'HEAD')

    Delete.delete(working_branch())
    Git.copy_from_remote(base_branch(), working_branch())

    _print_long_pulls('Building release branch for', pulls)
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

    if success:
        Version.version_commit(
            version_number=None, success=success, failure=failure)

    if success or not failure:
        commit_id = Git.commit_id()
        Git.force_checkout(next_branch())
        Git.git('reset', '--hard', commit_id)
        Git.git('push', '-f')

    commits = Open.get_commits()
    plural = '' if len(commits) == 1 else 's'
    _print_pulls('Proposed new develop branch %s for pull%s' %
                 (commits, plural), success)
    _print_pulls('FAILED:', failure)


def release(*branches):
    while True:
        _release(_make_pulls(branches))
        if branches or not ARGS.period:
            break
        time.sleep(ARGS.period)
        Cache.clear()

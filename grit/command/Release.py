from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import random
import re

from grit import Git
from grit import Project
from grit import Settings
from grit.Singleton import singleton
from grit.command import Delete
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

@Git.transaction
def _pull_request(pull):
    print('------------------------------------------------' )
    print(pull)
    if pull.user == Settings.USER:
        nickname = 'origin'
    else:
        try:
            nickname = Remote.inverse()[pull.user]
        except KeyError:
            Remote.add_remote(pull.user, pull.user)
            nickname = pull.user

    commits = []
    Git.git('fetch', nickname, pull.branch)
    Git.git('checkout', nickname + '/' + pull.branch)
    Git.git('rebase', '--preserve-merges', 'origin/' + next_branch())
    commit_id = Git.commit_id()

    Git.git('checkout', next_branch())
    Git.git('merge', '--ff-only', commit_id[:6])
    Git.git('push')

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

def _print_pulls(message, pulls):
    if pulls:
        print(message)
        print('\n'.join(str(p) for p in pulls))

def release(*pulls):
    Git.rebase_abort()
    pulls = list(pulls)
    add_version = 'noversion' not in pulls
    if not add_version:
        pulls.remove('noversion')

    if 'continue' in pulls:
        pulls.remove('continue')
    else:
        Delete.delete(next_branch())
        Git.copy_from_remote(base_branch(), next_branch())

    pulls = list(_make_pulls(pulls))
    if not pulls:
        raise Exception('No pulls ready!')

    _print_pulls('Building release branch for:', pulls)
    print()
    success = []
    failure = []
    exceptions = []
    for p in pulls:
        try:
            _pull_request(p)
        except Exception as e:
            failure.append([p, e])
        else:
            success.append(p)

    _print_pulls('\nSuccessfully pulled:', success)

    for pull, e in failure:
        print('%d FAILED: %s' % (pull.number, str(e)))

    if add_version and success:
        Version.version()
        Git.git('push')

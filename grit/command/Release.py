from __future__ import absolute_import, division, print_function, unicode_literals

import operator
import os
import random
import re
import time

from grit import Cache
from grit import Call
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
from grit.command import Slack
from grit.command import Version

HELP = """
grit release
    Make a release branch.
"""

_MATCHER = re.compile(
    '(?:git branch new_branch_name|HEAD position was|HEAD position) '
    '([0-9a-f]{7})', re.MULTILINE)

SAFE = False

@cached
def base_branch():
    return Project.settings('git').get('base_branch', 'develop')

def _print_pulls(message, pulls):
    if pulls:
        print(message, String.join_words(pulls) + '.')

@Git.transaction
def _pull_request(pull, working_branch):
    if pull.user == Settings.USER:
        nickname = 'origin'
    else:
        try:
            nickname = Remote.inverse()[pull.user]
        except KeyError:
            Remote.add_remote(pull.user, pull.user)
            nickname = pull.user

    keywords = {
        'nickname': nickname,
        'pull_branch': pull.branch,
        'working_branch': working_branch,
        'print': print if ARGS.verbose else None,
    }

    Call.runlines(
        """git fetch {nickname} {pull_branch}
           git checkout {nickname}/{pull_branch}
           git rebase --preserve-merges {working_branch}""",
        **keywords)

    # Store the commit ID at this point so we can merge back to it.
    keywords['commit_id'] = Git.commit_id()
    Call.runlines(
        """git checkout {working_branch}
           git merge --ff-only {commit_id}""",
        **keywords)

def _release(pulls, working_branch, next_branch, selector_name):
    Git.complete_reset()
    Delete.do_delete([working_branch], print=None)
    Git.copy_from_remote(base_branch(), working_branch, push=False)

    pulls.sort(key=operator.attrgetter('number'))

    if pulls:
        print('%s: Building release branch for %s:' % (
            String.timestamp(), selector_name))
        print('  ' + '\n  '.join(str(p) for p in pulls))
        print()

    success = []
    failure = []
    exceptions = []
    for pull in pulls:
        try:
            print(pull.number, '...', sep='', end='')
            _pull_request(pull, working_branch)
        except Exception as e:
            failure.append(pull.number)
            print('ERROR...', end='')
        else:
            success.append(pull.number)
    if pulls:
        print()
        print()

    Version.version_commit(
        version_number=None, success=success, failure=failure)

    commit_id = Git.commit_id()

    Git.force_checkout(next_branch)
    Git.git('reset', '--hard', commit_id)
    Git.git('push', '-f')

    commits = Open.get_commits()
    plural = '' if len(commits) == 1 else 's'
    _print_pulls('Proposed new develop branch %s for pull%s' %
                 (commits, plural), success)
    _print_pulls('FAILED:', failure)
    if success or failure:
        print('---------------------------------------------')
        print()
    else:
        print(String.timestamp(), ': no pulls ready.')

class PullSelector(object):
    def __init__(self, setting):
        self.name = setting['name']
        self.passes = set(setting['passed']).intersection
        self.fails = set(setting['failed']).intersection
        try:
            self.needed = set(setting['needed']).intersection
        except KeyError:
            self.needed = None
        self.pull_dict = {}

    def accept(self, pull):
        return (self.passes(pull.labels) and
                not self.fails(pull.labels) and
                not (self.needed and not self.needed(pull.labels)))

    def branch(self, category):
        return '%s-%s' % (self.name, category)

    def update_pulls(self, base_commit):
        pulls = [p for p in Git.pulls().values() if self.accept(p)]
        pull_dict = dict((p.number, p.commit_id) for p in pulls)
        pull_dict['base_commit'] = base_commit
        pull_dict, self.pull_dict = self.pull_dict, pull_dict
        if self.pull_dict != pull_dict:
            _release(
                pulls, self.branch('working'), self.branch('next'), self.name)
            return True


SETTINGS = Project.settings('release')
SELECTORS = [PullSelector(s) for s in SETTINGS.get('selectors', [])]

def release():
    previous_pulls = {}
    while True:
        base_commit = Git.commit_id(upstream=True, branch=base_branch())
        success = False
        for selector in SELECTORS:
            success = selector.update_pulls(base_commit) or success

        if success:
            Slack.slack()
        else:
            print(String.timestamp(short=True) + ': no change.')
        if ARGS.period:
            time.sleep(ARGS.period)
            Cache.clear()
        else:
            break

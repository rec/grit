from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import subprocess
import urllib2
from functools import wraps

from grit.Args import ARGS
from grit.Cache import cached
from grit import Call
from grit import File
from grit import GitRoot
from grit import Project
from grit import Settings

DEBUG = False

def git(*args, **kwds):
    return Call.run(('git',) + args, **kwds)

def branch(git=git):
    return git('status').splitlines()[0].split()[-1]

def remove_local_branch(branch, git=git, **kwds):
    branches = [i.strip() for i in git('branch', **kwds).splitlines()]
    if len(branches) <= 1:
        raise ValueError("Can't delete single local branch " + branch)
    if '* ' + branch in branches:
        # It's the current branch - rotate branches.
        rotate_local_branch(git=git, **kwds)
    git('branch', '-D', branch, **kwds)

def remove_origin_branch(branch, **kwds):
    git('push', 'origin', '--delete', branch, **kwds)

def rotate_local_branch(reverse=False, **kwds):
    branches = git('branch', **kwds).splitlines()
    if len(branches) > 1:
        for i, b in enumerate(branches):
            if b.startswith('*'):
                index = (i + (-1 if reverse else 1)) % len(branches)
                branch = branches[index].strip()
                git('checkout', branch)
                return branch

API = 'https://api.github.com'

def api(*parts):
    url = '/'.join((API, ) + parts)

    try:
        if ARGS.verbose:
            print('Opening URL', url)
        stream = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        e.msg = '%s: %s' % (e.msg, url)
        raise
    return json.load(stream)

def default_api(*parts):
    return api(parts[0], Settings.PROJECT_USER, Settings.PROJECT, *parts[1:])

def split_branch(branch):
    if ':' in branch:
        return branch.split(':')
    return Settings.PROJECT_USER, branch

class Pull(object):
    def __init__(self, pull):
        self.number = pull['number']
        self.user, self.branch = split_branch(pull['head']['label'])
        self.title = pull['title']
        self.commit_id = pull['head']['sha']
        self.updated_at = pull['updated_at']

    @property
    def labels(self):
        return labels()[self.number]

    def __str__(self):
        return '%s. %s:%s: %s' % (
            self.number, self.user, self.branch, self.title)

    def __repr__(self):
        return 'Pull(%s)' % str(self)

@cached
def pulls():
    result = {}
    for p in default_api('repos', 'pulls'):
        pull = Pull(p)
        result[pull.number] = pull
    return result

@cached
def issues():
    return default_api('repos', 'issues')

@cached
def labels():
    result = {}
    for issue in issues():
        result[issue['number']] = [lab['name'] for lab in issue['labels']]
    return result

def transaction(f):
    """A decorator to roll back git if things fail."""
    @wraps(f)
    def wrapper(*args, **kwds):
        commit = commit_id()
        try:
            f(*args, **kwds)
        except:
            rebase_abort()
            git('reset', '--hard', commit)
            raise

    return wrapper


def pull_branches(user=Settings.USER):
    result = {}
    for number, pull in pulls().items():
        if user and pull.user == user:
            result[pull.branch] = number

    return result

def branches():
    result = []
    for b in api('repos', Settings.USER, Settings.PROJECT, 'branches'):
        result.append(b['name'])
    return result

def copy_from_remote(from_branch, to_branch, remote='upstream', push=True):
    git('checkout', from_branch)
    git('pull', remote, from_branch)
    git('checkout', '-b', to_branch)
    if push:
        git('push', '--set-upstream', 'origin', to_branch)

def rebase_abort():
    try:
        git('rebase', '--abort', print=None)
    except:
        pass

def complete_reset():
    rebase_abort()
    git('clean', '-f')
    git('reset', '--hard', 'HEAD')


def commit_id(short=True, upstream=False, branch):
    branch = branch or Project.settings.get('base_branch', 'develop')
    if upstream:
        git('fetch', 'upstream', branch)
        id = git('show-ref', 'upstream/' + branch).split()[0]
    else:
        id = git('rev-parse', 'HEAD')
    return id[:8] if short else id

def force_checkout(branch):
    try:
        # git('checkout', branch, print=None)
        git('checkout', branch)
    except:
        git('checkout', '-b', branch)
        git('push', '--set-upstream', 'origin', branch)

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import subprocess
import urllib2
from functools import wraps

from grit.Args import ARGS
from grit.Singleton import singleton
from grit import Call
from grit import File
from grit import GitRoot
from grit import Settings

DEBUG = False

def git(*args, **kwds):
    command = ('git',) + args
    command_disp = ' '.join(command)
    if ARGS.verbose:
        print('$', command_disp)
    error, results = Call.call_value(
        command, stderr=subprocess.STDOUT, **kwds)
    if error:
        raise ValueError("Can't %s, error=%s" % (command_disp, error))
    if ARGS.verbose:
        print(results)
    return results

def branch(git=git):
    return git('status').splitlines()[0].split()[-1]

def remove_local_branch(branch, git=git):
    branches = [i.strip() for i in git('branch').splitlines()]
    if len(branches) <= 1:
        raise ValueError("Can't delete single local branch " + branch)
    if '* ' + branch in branches:
        # It's the current branch - rotate branches.
        rotate_local_branch(git=git)
    git('branch', '-D', branch)

def remove_origin_branch(branch, git=git):
    git('push', 'origin', '--delete', branch)

def rotate_local_branch(reverse=False, **kwds):
    branches = git('branch').splitlines()
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

    @property
    def labels(self):
        return labels()[self.number]

    def __str__(self):
        return '%s. %s:%s: %s' % (
            self.number, self.user, self.branch, self.title)

    def __repr__(self):
        return 'Pull(%s)' % str(self)

@singleton
def pulls():
    result = {}
    for p in default_api('repos', 'pulls'):
        pull = Pull(p)
        result[pull.number] = pull
    return result

@singleton
def issues():
    return default_api('repos', 'issues')

@singleton
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
            git('reset', '--hard', commit[:6])
            raise

    return wrapper


def pull_branches(user=Settings.USER):
    result = {}
    for number, pull in pulls().items():
        u, b = split_branch(pull.branch)
        if user and u == user:
            result[b] = number

    return result

def branches(user=Settings.USER):
    result = []
    for b in api('repos', user, Settings.PROJECT, 'branches'):
        result.append(b['name'])
    return result

def copy_from_remote(from_branch, to_branch, remote='upstream'):
    git('checkout', from_branch)
    git('pull', remote, from_branch)
    git('checkout', '-b', to_branch)
    git('push', '--set-upstream', 'origin', to_branch)

def rebase_abort():
    try:
        git('rebase', '--abort')
    except:
        pass

def commit_id():
    return git('rev-parse', 'HEAD')

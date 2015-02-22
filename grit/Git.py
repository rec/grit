from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import subprocess
import urllib2

from grit.Args import ARGS
from grit import Call
from grit import File
from grit import GitRoot
from grit import Settings

DEBUG = False

def git(*args, **kwds):
    command = ('git',) + args
    if ARGS.verbose:
        print('$', ' '.join(command))
    error, results = Call.call_value(
        command, stderr=subprocess.STDOUT, **kwds)
    if error:
        raise ValueError("Can't %s, error=%s" % (command, error))
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

def api(*parts, **kwds):
    url = '/'.join((API, ) + parts)

    try:
        if ARGS.verbose:
            print('Opening URL', url)
        stream = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        e.msg = '%s: %s' % (e.msg, url)
        raise
    return json.load(stream)

def pulls():
    result = {}
    for p in api('repos', Settings.PROJECT_USER, Settings.PROJECT, 'pulls'):
        result[p['number']] = p['head']['label'], p['title']
    return result

def split_branch(branch):
    if ':' in branch:
        return branch.split(':')
    return Settings.PROJECT_USER, branch

def pull_branches(user=Settings.USER):
    result = {}
    for number, (branch, _) in pulls().items():
        u, b = split_branch(branch)
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
        git('rebase --abort')
    except:
        pass

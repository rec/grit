from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import urllib2

from grit import Call
from grit import File
from grit import GitRoot
from grit import Settings

def git(*args, **kwds):
    command = ' '.join(('git',) + args)
    error, results = Call.call_value(command, **kwds)
    if error:
        raise ValueError("Can't %s, error=%s" % (command, error))
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
                git('checkout', branches[index])
                return

API = 'https://api.github.com'

def api(*parts):
    url = '/'.join((API, ) + parts)
    try:
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

def pull_branches(user):
    result = {}
    for number, (branch, _) in pulls().items():
        u, b = branch.split(':')
        if u == user:
            result[b] = number
    return result

def branches(user):
    result = []
    for b in api('repos', user, Settings.PROJECT, 'branches'):
        result.append(b['name'])
    return result

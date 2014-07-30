from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import urllib2

from grit import Call
from grit import File
from grit import Settings

def is_git_dir(path):
    git = os.path.join(path, '.git')
    return os.path.isdir(git)

def root(path=None):
    """Returns the git root recursively containing this directory, if any."""
    path = path or os.getcwd()
    original_path = None
    last_path = None
    while path != last_path:
        if is_git_dir(path):
            return path
        last_path = path
        path = os.path.dirname(path)

def root_container(path=None):
    new_path = root(path)
    return (new_path and os.path.dirname(new_path)) or path

def select(prefix=''):
    def selector(f):
        return is_git_dir(f) and os.path.basename(f).startswith(prefix)
    return selector

def branch(**kwds):
    error, results = Call.call_value('git status', **kwds)
    if error:
        raise ValueError("Can't get git status, error = " + error)
    return results.splitlines()[0].split()[-1]

API = 'https://api.github.com'

def api(*parts):
    url = '/'.join((API, ) + parts)
    return json.load(urllib2.urlopen(url))

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

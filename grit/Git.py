from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import urllib2

from grit import Call
from grit import File
from grit import GitRoot
from grit import Settings

def branch(**kwds):
    error, results = Call.call_value('git status', **kwds)
    if error:
        raise ValueError("Can't get git status, error = " + error)
    return results.splitlines()[0].split()[-1]

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

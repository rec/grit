from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import subprocess

def _get_directory():
    try:
        d = os.path.expanduser('~/.grit-d/cache')
        if not os.path.isdir(d):
            os.makedirs(d)
        return d
    except:
        return ''

CACHE_DIRECTORY = _get_directory()

def _filename(name):
    return os.path.join(CACHE_DIRECTORY, '%s.json' % name)

def get(name, default=None):
    try:
        return json.load(open(_filename(name)))
    except:
        return default

def put(name, value):
    try:
        json.dump(value, open(_filename(name), 'w'))
    except:
        print('Unable to store defaults', name)

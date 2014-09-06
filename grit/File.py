from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os

from os.path import exists, isabs, join, dirname

from grit import String

HOME = os.path.expanduser('~')
GRIT_ROOT = dirname(dirname(__file__))
JSON_SUFFIX = '.json'

def root_relative(*path):
    if isabs(path[0]):
        return join(*path)
    else:
        return join(GRIT_ROOT, *path)

def get_json(*path):
    path = root_relative(*path)
    try:
        data = open(path)
    except IOError:
        return {}
    try:
        return json.load(data)
    except ValueError as e:
        print(dir(e), e.args, e.message)
        e.args = 'In file %s: %s' % (path, e.args[0]),
        raise e

def add_suffix(path, suffix=JSON_SUFFIX):
    if path and path[-1].endswith(suffix):
        return path
    return path[:-1] + (path[-1] + suffix,)

def try_read(*path):
    try:
        with open(root_relative(*path)) as f:
            return f.read()
    except:
        return ''

def each(path=None, select=None):
    path = path or os.getcwd()
    for p in sorted(os.listdir(path), cmp=String.compare_version):
        filepath = join(path, p)
        if not select or select(filepath):
            yield filepath

def next_version(name):
    if not exists(name):
        return name
    base, _ = String.split_version(name)
    if not exists(name):
        return base

    version = 2
    while True:
        name = base + str(version)
        if not exists(name):
            return name
        version += 1

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os

from os.path import exists, isabs, join, dirname

from grit import String

ROOT = dirname(dirname(__file__))
JSON_SUFFIX = '.json'

def root_relative(*path):
    if isabs(path[0]):
        return join(*path)
    else:
        return join(ROOT, *path)

def get_json(*path):
    path = root_relative(*path)
    if not path.endswith(JSON_SUFFIX):
        path += JSON_SUFFIX
    try:
        return json.load(open(root_relative(path)))
    except IOError:
        return {}

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

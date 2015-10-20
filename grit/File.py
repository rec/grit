from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import re
import shutil

from tempfile import NamedTemporaryFile

from os.path import exists, isabs, join, dirname

from . import String

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

def subn(name, pattern, repl, count=None):
    with NamedTemporaryFile(dir=os.path.dirname(name), delete=False) as t:
        tmp_name = t.name
        with open(name) as f:
            for line in f.readlines():
                if count is None:
                    line = re.sub(pattern, repl, line)
                elif count > 0:
                    line, subs = re.subn(pattern, repl, line, count=count)
                    count -= subs
                t.write(line)

    os.remove(name)
    shutil.move(tmp_name, name)

def search(name, pattern):
    with open(name) as f:
        for line in f.readlines():
            match = re.search(pattern, line)
            if match:
                return match.group()

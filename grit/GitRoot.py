from __future__ import absolute_import, division, print_function, unicode_literals

import os

def is_git_dir(path):
    return os.path.isdir(os.path.join(path, '.git'))

def root(path=None):
    """Returns the git root recursively containing this directory, if any."""

    path = path or os.getcwd()
    original_path = path
    last_path = None
    while path != last_path:
        if is_git_dir(path):
            return path
        last_path = path
        path = os.path.dirname(path)


ROOT = root()

def root_container(path=None):
    new_path = root(path)
    return (new_path and os.path.dirname(new_path)) or path

def select(prefix=''):
    def selector(f):
        return is_git_dir(f) and os.path.basename(f).startswith(prefix)
    return selector

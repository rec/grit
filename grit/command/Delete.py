from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import urllib2

from grit.Args import ARGS
from grit import Git

SAFE = False

HELP = """
grit delete branch [branch ...]

    Deletes branches both locally and in your origin.
    Use with caution.
"""

PRINT = print

def do_delete(branches, print=print):
    pulls = set(branches) & set(Git.pull_branches())
    if pulls:
        raise Exception("Can't delete pull branches: " + ' '.join(pulls))

    success = set()
    for b in branches:
        try:
            Git.remove_local_branch(b, print=print)
            success.add(b)
        except:
            print and print('No local branch %s.' % b)
        try:
            Git.remove_origin_branch(b, print=print)
            success.add(b)
        except:
            print and print('No origin branch %s.' % b)

    return success, set(branches) - success


def delete(*branches):
    if not branches:
        raise ValueError('No branches specified to delete.')
    success, fail = do_delete(branches, print if ARGS.verbose else None)
    if success:
        print('Deleted: ', ' '.join(sorted(success)))
    if fail:
        print('Failed to delete: ', ' '.join(sorted(fail)))

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import urllib2

from grit import Git

SAFE = False

HELP = """
grit delete branch [branch ...]

    Deletes branches both locally and in your origin.
    Use with caution.
"""

def do_delete(branches, print=print):
    pulls = set(branches) & set(Git.pull_branches())
    if pulls:
        raise Exception("Can't delete pull branches: " + ' '.join(pulls))

    for b in branches:
        try:
            Git.remove_local_branch(b, print=print)
        except:
            print and print('No local branch %s.' % b)
        try:
            Git.remove_origin_branch(b, print=print)
        except:
            print and print('No origin branch %s.' % b)

def delete(*branches):
    do_delete(branches)

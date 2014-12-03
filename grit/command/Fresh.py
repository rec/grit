from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import urllib2

from grit import Git
from grit import Project

SAFE = True

HELP = """
grit fresh branch [base_branch ...]

    Make a fresh branch.
"""
def fresh(branch, base_branch=None):
    base_branch = base_branch or Git.branch()
    Git.copy_from_remote(base_branch, branch, 'origin')

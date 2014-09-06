from __future__ import absolute_import, division, print_function, unicode_literals

import os
from os.path import basename, dirname, isdir, join

from grit import Call
from grit import File
from grit import Git
from grit import Project
from grit import Settings
from grit.String import banner
from grit.command import Pulls
from grit.command import Remote
from grit.command import Test

SAFE = False

HELP = """
grit rm <branch>
    Deletes both local and remote versions of a branch.
"""

_CLONE = """
git clone git@github.com:{user}/{project}.git --branch {branch} {directory}
"""

def rm(*branches):
    assert branches, "You didn't specify any branches to remove."
    base_branch = Project.settings('clone').get('base_branch', 'develop')
    assert (base_branch not in branches), (
        "You can't delete the base branch, %s." % base_branch)
    for branch in branches:
        if branch == Git.branch():
            Call.call('git checkout %s' % base_branch)
        Call.call('git branch -d %s' % branch)
        Call.call('git push origin :%s' % branch)

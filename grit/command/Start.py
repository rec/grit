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
from grit.command import Test

HELP = """
grit start <branch> [<directory>]
    Starts a fresh branch of the current project.

    Goes to the directory above the git directory containing the current path,
    clones a copy of the current project under the name directory, checks out
    the branch name given, adds git remotes, then runs some tests.

    The list of tests and the list of git remotes is found in the settings
    directory for your project.

    If the directory name is not given, it adds a numeric suffix to the current
    directory.
"""

_CLONE = """
git clone git@github.com:{user}/{project}.git --branch {branch} {directory}
"""

_REMOTE = """
git remote add {nickname} git@github.com:{user}/{project}.git
"""

def remotes(cwd=None):
    value = Call.call_raw('git remote', cwd=cwd)
    remotes = set(value.split())
    for nickname, user in Project.settings('remotes').items():
        if nickname not in remotes:
            remote = _REMOTE.format(
                nickname=nickname, user=user, project=Settings.PROJECT)
            Call.call(remote, cwd=cwd)

def clone(directory):
    settings = Project.settings('clone')
    branch = settings['base_branch']

    root = Git.root(os.getcwd())
    if root:
        directory = directory or basename(root)
        root = dirname(root)
    else:
       directory = directory or Settings.PROJECT
       root = os.getcwd()

    directory = File.next_version(join(root, directory))
    settings.update(
        branch=branch,
        directory=directory,
        project=Settings.PROJECT,
        user=Settings.USER,
    )
    # Call git clone.
    Call.for_each(_CLONE.format(**settings), cwd=root)
    banner('Created', branch, ', directory', directory)
    remotes(cwd=directory)
    return directory

_ERROR = """
Branch "%s" already exists.
Existing branches are: %s."""

def start(branch, directory=''):
    branches = Git.branches(Settings.USER)
    if branch in branches:
        raise ValueError(_ERROR % (branch, ' '.join(branches)))

    directory = clone(directory)
    Call.call_raw('git checkout -b ' + branch, cwd=directory)
    Test.run_test(directory)
    banner('Checked out new branch', branch)

from __future__ import absolute_import, division, print_function, unicode_literals

import os

from grit import Call
from grit import File
from grit import Git
from grit import GitRoot
from grit import Project
from grit import Settings
from grit.String import banner
from grit.command import Remote
from grit.command import Test

SAFE = False

HELP = """
grit start <branch> [<directory>]
    Starts a fresh branch of the current project.

    Goes to the directory above the git directory containing the current path,
    clones a copy of the current project under the name directory, checks out
    the branch name given, then runs some tests.

    The list of tests is found in the settings directory for your project.

    If the directory name is not given, it adds a numeric suffix to the current
    directory.
"""

_CLONE = """
git clone git@github.com:{user}/{project}.git --branch {branch} {directory}
"""

def clone(directory):
    settings = Project.settings('clone')
    branch = settings.get('base_branch', 'develop')

    root = GitRoot.root(os.getcwd())
    if root:
        directory = directory or os.path.basename(root)
        root = os.path.dirname(root)
    else:
       directory = directory or Settings.PROJECT
       root = os.getcwd()

    directory = File.next_version(os.path.join(root, directory))
    settings.update(
        branch=branch,
        directory=directory,
        project=Settings.PROJECT,
        user=Settings.USER,
    )
    # Call git clone.
    if Call.call(_CLONE.format(**settings).strip(), cwd=root):
        raise ValueError('Failed to start new directory')

    banner('Created', branch + ', directory', directory)
    return directory

_ERROR = """
Branch "%s" already exists.
Existing branches are: %s."""

def start(branch, directory=''):
    branches = Git.branches(Settings.USER)
    if branch in branches:
        raise ValueError(_ERROR % (branch, ' '.join(branches)))

    directory = clone(directory)
    Remote.remote('all', cwd=directory)
    Remote.remote('upstream', Settings.PROJECT, directory)
    Call.call_raw('git checkout -b ' + branch, cwd=directory)
    Test.run_test(directory)
    banner('Checked out new branch', branch)

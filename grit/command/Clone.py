from __future__ import absolute_import, division, print_function, unicode_literals

import os
from os.path import basename, dirname, isdir, join

from grit import Call
from grit import File
from grit import Git
from grit import Project
from grit import Settings
from grit.command import Test

HELP = """
grit clone [branch] [directory]
    Gets a fresh clone of the current project containing a new branch.

    Goes to the directory above the git directory containing the current path,
    clones a copy of the current project under the name directory, checks out
    the branch name given, adds git remotes, then runs some tests.

    The list of tests and the list of git remotes is found in the settings
    directory for your project.

    If the directory name is not given, it adds a numeric suffix to the current
    directory.

    If the branch is not given, it defaults to the base_branch of your project
    (probably "develop").

    If the branch name contains a :, it's a remote branch.  For account names,
    you can use either the full name or the remote nickname.
"""

_CLONE = """
git clone git@github.com:{user}/{project}.git --branch {base_branch} {directory}
"""

_BRANCH = 'git checkout {new_flag} {branch}'

def remotes(cwd=None):
    value = Call.call_raw('git remote', cwd=cwd)
    remotes = set(value.split())
    for nickname, user in Project.settings('remotes').items():
        if nickname not in remotes:
            remote = _REMOTE.format(
                nickname=nickname, user=user, project=Settings.PROJECT)
            Call.call(remote, cwd=cwd)

def clone(branch='', directory=''):
    settings = Project.settings('clone')
    base_branch = settings['base_branch']
    branch = branch or base_branch

    if ':' in branch:
        user, branch = branch.split(':', 1)
    else:
        user = None

    project = Settings.PROJECT

    root = Git.root(os.getcwd())
    if root:
        directory = directory or basename(root)
        root = dirname(root)
    else:
       directory = directory or project
       root = os.getcwd()

    directory = File.next_version(join(root, directory))
    settings.update(
        branch=branch,
        directory=directory,
        project=project,
        user=Settings.USER,
    )
    Call.for_each(_CLONE.format(**settings), cwd=root)
    branches = Git.branch(cwd=directory)

    remotes(cwd=directory)

    br = _OLD_BRANCH if branch == base_branch else _NEW_BRANCH
    Call.for_each(br.format(**settings), cwd=directory)
    print('***** Created %s, branch %s *****' % (directory, branch))
    Test.run_test(directory)
    print('***** Tested %s, branch %s *****' % (directory, branch))
#

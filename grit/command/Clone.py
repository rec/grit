from __future__ import absolute_import, division, print_function, unicode_literals

import os
from os.path import basename, dirname, isdir, join

from grit import Call
from grit import File
from grit import Git
from grit import Project
from grit import Settings
from grit.command import Test
from grit.command import Remotes

HELP = """

    grit clone [branch] [directory]

Gets a fresh clone of the current project containing a new branch.

Goes to the directory above the git directory containing the current path,
clones a copy of the current project under the name directory, checks out the
branch name given, adds git remotes, then runs some tests.

The list of tests and the list of git remotes is found in the settings directory
for your project.

If the directory name is not given, it adds a numeric suffix to the current
directory.

If the branch is not given, it defaults to the base_branch of your project
(probably "develop").

"""

_CLONE = """
git clone git@github.com:{user}/{project}.git --branch {base_branch} {directory}
"""

_NEW_BRANCH = """
git checkout -b {branch}
git push --set-upstream origin {branch}
"""

_OLD_BRANCH = 'git checkout {branch}'

def clone(branch='', directory=''):
    settings = Project.settings('clone')
    base_branch = settings['base_branch']
    branch = branch or base_branch

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
    Remotes.remotes(cwd=directory)

    br = _OLD_BRANCH if branch == base_branch else _NEW_BRANCH
    Call.for_each(br.format(**settings), cwd=directory)
    print('***** Created %s, branch %s *****' % (directory, branch))
    Test.run_test(directory)
#

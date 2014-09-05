from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

from grit import Call
from grit import File
from grit import GitRoot
from grit import Project
from grit.CommandList import CommandList

SAFE = True

MAIN_HELP = """
grit cd [command]
    A command to help change directories.

    Often passed to the shell's cd command, like this:
        $ cd `grit cd +`
"""

ROOT_HELP = """
grit {cd}^
grit {cd}6
    Print the top-level directory in this git project.
"""

FORWARD_HELP = """
grit {cd}+ [<prefix>]
grit {cd}= [<prefix>]
    Print the the next git project sibling to this one.
    Only considers directories that start with prefix, if it's set.
"""

BACK_HELP = """
grit {cd}- [<prefix>]
grit {cd}_ [<prefix>]
    Go to the previous git project sibling to this one.
    Only considers directories that start with prefix, if it's set.
"""

HELP = '\n'.join(
    [MAIN_HELP, ROOT_HELP, FORWARD_HELP, BACK_HELP]).format(cd='cd ')

def _move_root(forward, prefix=''):
    root = GitRoot.ROOT
    container = GitRoot.root_container()
    roots = sorted(File.each(path=container, select=GitRoot.select(prefix)))

    if roots:
        try:
            index = roots.index(root)
        except ValueError:
            print(roots[0] if forward else roots[-1])
            return
        index += (1 if forward else -1)
        path = roots[index % len(roots)]
        sub = os.path.join(path, os.path.relpath(os.getcwd(), root))
        print((sub if os.path.exists(sub) else path) or '.')
    else:
        print('.')

def root():
    print(GitRoot.ROOT)

def forward(prefix=''):
    _move_root(True, prefix)

def back(prefix=''):
    _move_root(False, prefix)

COMMAND_LIST = {
    '^': (root, ROOT_HELP.format(cd=''), True),
    '6': (root, ROOT_HELP.format(cd=''), True),
    '+': (forward, FORWARD_HELP.format(cd=''), True),
    '=': (forward, FORWARD_HELP.format(cd=''), True),
    '-': (back, BACK_HELP.format(cd=''), True),
    '_': (back, BACK_HELP.format(cd=''), True),
    }

_COMMANDS = CommandList(**COMMAND_LIST)

def cd(command='^', *args):
    if command in _COMMANDS.registry:
        _COMMANDS.run(command, *args)
    else:
        forward(*args)

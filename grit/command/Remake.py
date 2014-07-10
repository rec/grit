from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import random

from grit import Call
from grit import Project
from grit import Git

HELP = """

    grit remake

Rebuild the build files (Makefile, Sconstruct or vcxproj) for this project.

"""

SAFE = True

def remake():
    remake = Project.settings('remake').get('remake')
    if remake:
        Call.call(remake, cwd=Git.root())
        print('Project file remade.')

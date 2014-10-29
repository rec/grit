from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import random

from grit.Args import ARGS
from grit import Call
from grit import Git

HELP = """
grit rotate
    Rotate branches in your client.

    Use the --reverse/-r flag to rotate backward.
"""

SAFE = True

def rotate():
    Git.rotate_local_branch(ARGS.reverse)

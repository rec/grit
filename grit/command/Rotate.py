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

def rotate(count='1'):
    count = int(count)
    if not count:
        raise ValueError('Rotate by 0!')
    if count < 0:
        count = -count
        ARGS.reverse = not ARGS.reverse
    for c in range(count):
        branch = Git.rotate_local_branch(ARGS.reverse)

    print('Branch is now %s.' % branch)

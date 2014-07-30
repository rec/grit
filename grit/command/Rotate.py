from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import random

from grit.Args import ARGS
from grit import Call

HELP = """
grit rotate
    Rotate branches in your client.

    Use the --reverse/-r flag to rotate backward.
"""

SAFE = True

def rotate():
    branches = Call.call_raw('git branch').splitlines()
    if len(branches) > 1:
        for i, b in enumerate(branches):
            if b.startswith('*'):
                index = (i + (-1 if ARGS.reverse else 1)) % len(branches)
                Call.call_raw('git checkout ' + branches[index])
                return

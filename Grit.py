#!/usr/bin/env python3

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import traceback

from grit.Args import ARGS
from grit.command import COMMANDS

if __name__ == '__main__':
    try:
        COMMANDS.run_safe(*ARGS.command)
    except:
        print(traceback.format_exc(), file=sys.stderr)
        print('.')

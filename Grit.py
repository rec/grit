#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import traceback

from grit.Args import ARGS

from grit.command import Amend
from grit.command import Branches
from grit.command import Clone
from grit.command import CD
from grit.command import Delete
from grit.command import Explode
from grit.command import Find
from grit.command import Fresh
from grit.command import Import
from grit.command import Help
from grit.command import New
from grit.command import Open
from grit.command import Pulls
from grit.command import Release
from grit.command import Remake
from grit.command import Remote
from grit.command import Rename
from grit.command import Rotate
from grit.command import Settings
from grit.command import Slack
from grit.command import Start
from grit.command import Swap
from grit.command import Test
from grit.command import Version

from grit.CommandList import CommandList

import os
import sys

_COMMANDS = CommandList(
    Amend, Branches, Clone, Delete, Explode, Help, Import, Find, Fresh, New,
    Open, Pulls, Release, Remake, Rename, Remote, Rotate, Settings, Slack,
    Start, Swap, Test, Version)

_COMMANDS.register(**CD.COMMAND_LIST)

Help.set_commands(_COMMANDS)

if __name__ == '__main__':
    try:
        _COMMANDS.run_safe(*ARGS.command)
    except:
        print(traceback.format_exc(), file=sys.stderr)
        print('.')

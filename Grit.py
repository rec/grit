#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import traceback

from grit import Args

from grit.command import Amend
from grit.command import Branches
from grit.command import Clone
from grit.command import CD
from grit.command import Find
from grit.command import Import
from grit.command import Help
from grit.command import New
from grit.command import Open
from grit.command import Pulls
from grit.command import Remake
from grit.command import Remote
from grit.command import Rm
from grit.command import Rotate
from grit.command import Settings
from grit.command import Start
from grit.command import Test

from grit.CommandList import CommandList

import os
import sys

_COMMANDS = CommandList(
    Amend, Branches, Clone, Help, Import, Find, New, Open, Pulls,
    Remake, Remote, Rm, Rotate, Settings, Start, Test)

_COMMANDS.register(**CD.COMMAND_LIST)

Help.set_commands(_COMMANDS)

if __name__ == '__main__':
    try:
        _COMMANDS.run_safe(*Args.get_args())
    except:
        print(traceback.format_exc(), file=sys.stderr)
        print('.')

#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import traceback

from grit.command import Amend
from grit.command import Branches
from grit.command import Clone
from grit.command import CD
from grit.command import Find
from grit.command import Help
from grit.command import New
from grit.command import Open
from grit.command import Pulls
from grit.command import Remake
from grit.command import Remotes
from grit.command import Test

from grit.CommandList import CommandList

import os
import sys

_COMMANDS = CommandList(
    Amend, Branches, Clone, Help, Find, New, Open, Pulls, Remake, Remotes, Test)

_COMMANDS.register(**CD.COMMAND_LIST)

Help.set_commands(_COMMANDS)

if __name__ == '__main__':
    try:
        _COMMANDS.run_safe(*(sys.argv[1:] or ['branches']))
    except:
        print(traceback.format_exc(), file=sys.stderr)
        print('.')
#

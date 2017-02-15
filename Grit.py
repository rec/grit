#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import os, sys, traceback

from grit.Args import ARGS

from grit.command import (
    Amend, Branches, Clone, CD, Delete, Explode, Find, Fresh, Import, Help,
    New, Open, Pulls, Release, Remake, Remote, Rename, Rm, Rotate, Settings,
    Slack, Start, Swap, Test, Version)

from grit.CommandList import CommandList


_COMMANDS = CommandList(
    Amend, Branches, Clone, Delete, Explode, Help, Import, Find, Fresh, New,
    Open, Pulls, Release, Remake, Rename, Remote, Rm, Rotate, Settings, Slack,
    Start, Swap, Test, Version)

_COMMANDS.register(**CD.COMMAND_LIST)

Help.set_commands(_COMMANDS)

if __name__ == '__main__':
    try:
        _COMMANDS.run_safe(*ARGS.command)
    except:
        print(traceback.format_exc(), file=sys.stderr)
        print('.')

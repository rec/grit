from .. CommandList import CommandList as _CommandList

from . import (
    Amend,
    Branches,
    Clone,
    Delete,
    Explode,
    EFind,
    Find,
    Fresh,
    Import,
    Help,
    New,
    Open,
    Pulls,
    Release,
    Remake,
    Remote,
    Rename,
    Rotate,
    Settings,
    Slack,
    Start,
    Swap,
    Test,
    Version)

COMMANDS = _CommandList(*(v for (k, v) in globals().items()
                          if not k.startswith('_')))

from . import CD

COMMANDS.register(**CD.COMMAND_LIST)
Help.set_commands(COMMANDS)

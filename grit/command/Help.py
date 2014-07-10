from __future__ import absolute_import, division, print_function, unicode_literals

HELP = """

    grit help [command...]

Show help on grit commands.
"""

_COMMANDS = None

SAFE = True

def set_commands(commands):
    global _COMMANDS
    _COMMANDS = commands

def help(*commands):
    bad_commands = []
    for c in commands:
        try:
            print(_COMMANDS.get(c)[1])
        except:
            bad_commands.append(c)
    if bad_commands:
        print("Didn't understand commands:", ', '.join(bad_commands))
    if bad_commands or not commands:
        print('Valid commands are:', ', '.join(sorted(_COMMANDS.registry)))


#

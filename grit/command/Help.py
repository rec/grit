from __future__ import absolute_import, division, print_function, unicode_literals

HELP = """
grit help [ [command...] | all]
    Shows help on grit commands.
"""

_COMMANDS = None

SAFE = True

def set_commands(commands):
    global _COMMANDS
    _COMMANDS = commands

def help(*commands):
    if len(commands) == 1 and commands[0] == 'all':
        commands = sorted(_COMMANDS.keys())

    bad_commands = []
    already_seen = set()
    for c in commands:
        try:
            function, help, _ = _COMMANDS.get(c)
        except:
            bad_commands.append(c)
            raise
        else:
            if function not in already_seen:
                already_seen.add(function)
                print(help)
    if bad_commands:
        print("Didn't understand commands:", ', '.join(bad_commands))
    if bad_commands or not commands:
        print('Valid commands are:', ', '.join(sorted(_COMMANDS.registry)))

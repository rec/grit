from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os, platform, sys

# See https://stackoverflow.com/questions/7445658
CAN_CHANGE_COLOR = (
    hasattr(sys.stderr, 'isatty')
    and sys.stderr.isatty()
    and platform.system() != 'Windows'
    #and not os.environ.get('INSIDE_EMACS')
)

print('CAN_CHANGE_COLOR', CAN_CHANGE_COLOR)

# See https://en.wikipedia.org/wiki/ANSI_escape_code
BLUE, GREEN, RED, YELLOW = 94, 92, 91, 93

def add_mode(text, *modes):
    if CAN_CHANGE_COLOR:
        modes = ';'.join(str(m) for m in modes)
        return '\033[%sm%s\033[0m' % (modes, text)
    else:
        return text

def blue(text):
    return add_mode(text, BLUE)

def green(text):
    return add_mode(text, GREEN)

def red(text):
    return add_mode(text, RED)

def yellow(text):
    return add_mode(text, YELLOW)

def warn(text, print=print):
    print('%s %s' % (red('WARNING:'), text))

# Prints command lines using environment substitutions
def print_coms(coms, env):
    if type(coms) is str:
        coms=list(coms)
    for key in coms:
        cmdline = env.subst(env[key], 0,
            env.File('<target>'), env.File('<sources>'))
        print (green(cmdline))

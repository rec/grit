from __future__ import absolute_import, division, print_function, unicode_literals

import argparse

VERSION = '0.1'

parser = argparse.ArgumentParser(
    description='GRIT: workflow rationalization for Git.',
)

parser.add_argument(
    '--case_insensitive', '-i',
    action='store_true',
    help='If true, searches are case insensitive.',
)

parser.add_argument(
    '--yes', '-y',
    action='store_true',
    help='If true, don\'t ask for confirmation.',
)

parser.add_argument(
    'command',
    default='branches',
    nargs='?'
    )

parser.add_argument(
    'argument',
    default=None,
    nargs='?'
    )

ARGS = parser.parse_args()

def get_args():
    return [ARGS.command, ARGS.argument] if ARGS.argument else [ARGS.command]

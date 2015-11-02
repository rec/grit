from __future__ import absolute_import, division, print_function, unicode_literals

import argparse

VERSION = '0.1'

parser = argparse.ArgumentParser(
    description='GRIT: workflow rationalization for Git.',
)

parser.add_argument(
    '--all_projects', '-a',
    action='store_true',
    help='If true, search all branches, not just branches for this project.',
)

parser.add_argument(
    '--case_insensitive', '-i',
    action='store_true',
    help='If true, searches are case insensitive.',
)

parser.add_argument(
    '--expanded', '-e',
    action='store_true',
    help='If true, use relaxed, multi-line displays.',
)

parser.add_argument(
    '--force', '-f',
    action='store_true',
    help='If true, force-push after amending.',
)

parser.add_argument(
    '--period', '-p',
    default=0,
    type=int,
    help='For looping functions, how many seconds to wait before repeating.',
)

parser.add_argument(
    '--reverse', '-r',
    action='store_true',
    help='If true, rotate and other searches are in reverse order.',
)

parser.add_argument(
    '--verbose', '-v',
    action='store_true',
    help=('Report more information about which commands are executed and the '
          'results.'),
)

parser.add_argument(
    '--yes', '-y',
    action='store_true',
    help='If true, don\'t ask for confirmation.',
)

parser.add_argument(
    'command',
    default=['branches'],
    nargs='*'
    )

ARGS = parser.parse_args()

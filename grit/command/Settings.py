from __future__ import absolute_import, division, print_function, unicode_literals

from grit.Settings import SETTINGS

HELP = """
grit settings
   Prints the project settings.
"""

SAFE = True

def settings():
    for i in SETTINGS.items():
        print('='.join(i))

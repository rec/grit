from __future__ import absolute_import, division, print_function, unicode_literals

import os

from grit import Git
from grit import GitRoot

SAFE = False

HELP = """
grit explode

  Makes a single commit for each uncommitted file.
"""

def explode():
    root = GitRoot.root()
    for line in Git.git('status', '--porcelain').splitlines():
        mode, filename = line.split(None, 1)
        filenames = filename.split(' -> ')
        try:
            if mode == '??':
                Git.git('add', *filenames, cwd=root)
            Git.git('commit', '-m', '[fold] %s' % filenames[0], *filenames,
                    cwd=root)
        except Exception as e:
            print("ERROR: couldn't commit filename %s." % filename)
            print("ERROR:", e)

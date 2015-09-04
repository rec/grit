#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import os, sys

from grit import GitRoot

if __name__ == '__main__':
    print(GitRoot.root((sys.argv[1:] or [os.getcwd()])[0]))

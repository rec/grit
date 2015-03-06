from __future__ import absolute_import, division, print_function, unicode_literals

from functools import wraps
from weakref import WeakSet

from grit.Args import ARGS

class Cache(object):
    CACHED = WeakSet()

    def __init__(self, function):
        self.function = function
        self.none = object()
        self.clear()
        self.CACHED.add(self)

    def clear(self):
        self.value = self.none

    def __call__(self):
        if self.value is self.none:
            self.value = self.function()
        return self.value

cached = Cache

def clear():
    if ARGS.verbose:
        print('Clearing all caches.')
    for c in Cache.CACHED:
        c.clear()

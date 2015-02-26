from __future__ import absolute_import, division, print_function, unicode_literals

from functools import wraps

def singleton(f):
    """Evaluate a function once, lazily, and cache the result."""
    result = []

    @wraps(f)
    def wrapper():
        if not result:
            result.append(f())
        return result[0]
    return wrapper

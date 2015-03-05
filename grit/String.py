from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import re

from grit.Args import ARGS

_DIGIT_SPLITTER = re.compile(r'^(.*?)(\d*)$')

def split_version(name):
    match = _DIGIT_SPLITTER.match(name)
    name, digits = match.groups() if match else (name, '')
    return name, int(digits or '1')

def compare_version(x, y):
    return cmp(split_version(x), split_version(y))

def try_attr(obj, name):
    attr = getattr(obj, name, None)
    return attr() if attr else obj

def split_safe(s, attribute='split'):
    return try_attr(s, attribute)

def banner(*parts):
    print('\n*** %s ***\n' % ' '.join(parts))

def startswith(a, b):
    if ARGS.case_insensitive:
        a, b = a.lower(), b.lower()
    return a.startswith(b)

def join_words(words):
    words = list(words)
    if not words:
        return ''
    if len(words) == 1:
        return str(words[0])
    return '%s and %s' % (', '.join(str(i) for i in words[:-1]), words[-1])

def timestamp():
    return datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S')

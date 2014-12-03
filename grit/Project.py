from __future__ import absolute_import, division, print_function, unicode_literals

import os

from grit import File
from grit import Settings

ROOT = File.root_relative('projects')

PATH = (
    (File.HOME, '.grit', Settings.PROJECT),
    (ROOT, Settings.PROJECT),
    (File.HOME, '.grit', 'default'),
    (ROOT, 'default'),
)

def data(*names):
    for p in PATH:
        r = File.try_read(*(p + names))
        if r:
            return r

def settings(*names):
    names = File.add_suffix(names)
    settings = {}
    for p in reversed(PATH):
        settings.update(File.get_json(*(p + names)))

    return settings

def files(*names):
    result = set()
    for p in PATH:
        full_path = os.path.join(*(p + names))
        try:
            result.update(os.listdir(full_path))
        except:
            pass
    return result

from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from grit import File
from grit import Settings

DEFAULT_ROOT = File.root_relative('projects', 'default')
ROOT = File.root_relative('projects', Settings.PROJECT)

PATH = (
    (File.HOME, '.grit', Settings.PROJECT),
    ('projects', Settings.PROJECT),
    (File.HOME, '.grit', 'default'),
    ('projects', 'default'),
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

#

from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from grit import File
from grit import Settings

DEFAULT_ROOT = File.root_relative('projects', 'default')
ROOT = File.root_relative('projects', Settings.PROJECT)

def data(*names):
    return (File.try_read('projects', Settings.PROJECT, *names) or
            File.try_read('projects', 'default', *names))

def settings(*names):
    settings = File.get_json(DEFAULT_ROOT, *names)
    settings.update(File.get_json(ROOT, *names))

    return settings

#

from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import subprocess

from grit import File

DIRECT_CALL = True

def try_attr(obj, name):
    attr = getattr(obj, name, None)
    return attr() if attr else obj

def call(command, callback=None, **kwds):
    cmd = try_attr(command, 'split')
    returncode = 0
    error = ''
    if callback:
        try:
            callback(subprocess.check_output(cmd, **kwds))
        except subprocess.CalledProcessError as e:
            returncode = e.returncode
            error = e.output
    else:
        returncode = subprocess.call(cmd, **kwds)
    if returncode:
        print('ERROR:'
              ' command =', command.strip(),
              ' code =', returncode)
        error and print(error)
    return returncode

def call_value(command, **kwds):
    cmd = try_attr(command, 'split')
    try:
        return 0, subprocess.check_output(cmd, **kwds)
    except subprocess.CalledProcessError as e:
        print('ERROR:'
              ' command =', command.strip(),
              ' code =', returncode)
        e.output and print(e.output)
        return e.returncode, ''

def for_each(commands, before=None, after=None, **kwds):
    for command in filter(None, try_attr(commands, 'splitlines')):
        before and before(command)
        if call(command, **kwds):
            after and after(command)

def for_each_directory(
        command, select=None, path=None, before=None, after=None, **kwds):
    for f in File.each(path=path, select=select):
        before and before(f)
        call(command, cwd=f, **kwds)
        after and after(f)
#

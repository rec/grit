from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import subprocess

from grit.Args import ARGS
from grit import File
from grit import String

DIRECT_CALL = True

def call_raw(command, **kwds):
    cmd = String.split_safe(command)
    try:
        return subprocess.check_output(cmd, **kwds)
    except subprocess.CalledProcessError as e:
        raise ValueError('Couldn\'t execute "%s", errorcode=%s' %
                         ' '.join(cmd), e.returncode)

def call(command, callback=None, print=print, **kwds):
    cmd = String.split_safe(command)
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
    if returncode and print:
        print('ERROR:'
              ' command =', ' '.join(cmd),
              ' code =', returncode)
        error and print(error)
    return returncode

def call_value(command, print=print, **kwds):
    cmd = String.split_safe(command)
    try:
        return 0, subprocess.check_output(cmd, **kwds)
    except subprocess.CalledProcessError as e:
        if print:
            print('ERROR2:'
                  ' command =', ' '.join(cmd),
                  ' code =', e.returncode)
            e.output and print(e.output)
        return e.returncode, ''

def run(command, print=print, **kwds):
    command_disp = ' '.join(command)
    if ARGS.verbose and print:
        print('$', command_disp)
    error, results = call_value(
        command, stderr=subprocess.STDOUT, print=print, **kwds)
    if error:
        raise ValueError("Can't %s, error=%s" % (command_disp, error))
    if ARGS.verbose and print:
        print(results)
    return results

def runlines(lines, print=print, **substitutions):
    for line in String.splitlines(lines.format(**substitutions)):
        run(line.split(), print=print)

def for_each(commands, before=None, after=None, **kwds):
    for command in filter(None, String.split_safe(commands, 'splitlines')):
        before and before(command)
        if call(command, **kwds):
            after and after(command)

def for_each_directory(
        command, select=None, path=None, before=None, after=None, **kwds):
    for f in File.each(path=path, select=select):
        before and before(f)
        call(command, cwd=f, **kwds)
        after and after(f)

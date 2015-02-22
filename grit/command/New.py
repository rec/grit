from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import random

from grit import Call
from grit import CppGuards
from grit import GitRoot
from grit import Project
from grit import Settings

from grit.command import Remake

HELP = """
grit new filename [...filename]
    Create new files using the project templates.
"""

SAFE = True

def _get_guard(f):
    try:
        return CppGuards.get_guard(f)
    except:
        return ''

def _existing_templates():
    suffix = '.template'
    templates = sorted(Project.files('new'), key=len, reverse=True)
    return [t[:-len(suffix)] for t in templates if t.endswith(suffix)]

def new(*files):
    if not files:
        raise Exception('No files specified for "new" command.')
    existing_templates = _existing_templates()

    templates = []
    for f in files:
        if os.path.exists(f):
            raise Exception(f + ' already exists!')
        for t in existing_templates:
            if f.endswith(t):
                template = Project.data('new', '%s.template' % t)
                break
        else:
            raise ValueError('No template for ' + f)
        templates.append([f, template])

    settings = Project.settings('new')
    namespace = settings.get('namespace', Settings.PROJECT),
    root = GitRoot.ROOT
    include_root = os.path.join(root, settings['include_root'])
    for f, template in templates:
        body, extension = os.path.splitext(f)
        if extension.startswith('.'):
            extension = extension[1:]
        name = os.path.basename(body)
        fname = os.path.dirname(os.path.abspath(name))
        path_to_file = os.path.relpath(fname, include_root)
        output = template.format(
            guard=_get_guard(f),
            path_to_file=path_to_file,
            name=name,
            namespace=namespace)
        name = '%s.%s' % (body, extension)
        with open(name, 'w') as f:
            f.write(output)
        Call.call('git add ' + name)
        print(name, 'written and git added.')
    Remake.remake()

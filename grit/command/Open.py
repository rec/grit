from __future__ import absolute_import, division, print_function, unicode_literals

import os
import platform
import random

from grit import Call
from grit import Git
from grit import GitRoot
from grit import Settings
from grit.String import startswith
from grit.command import Pulls
from grit.command import Remote

HELP = """
grit open [filename]
    Open the filename as a Github URL in the browser.

    Selects the first file that starts with filename.  If filename is missing,
    opens the current directory in the browser.
"""

"""

open
open root [upstream] [alias]
open Filename
open commit
open diff
open pull

"""

SAFE = True

_OPEN_COMMANDS = {
    'Darwin': 'open',
    'Linux': 'xdg-open',
}

_URL = 'https://github.com/{user}/{project}/tree/{branch}/{path}'
_COMMIT = 'https://github.com/{user}/{project}/commits/{branch}'
_PULL = 'https://github.com/{project_user}/{project}/pull/{number}'
_NEW_PULL = 'https://github.com/{user}/{project}/compare/{branch}?expand=1'
_DIFF = 'https://github.com/{user}/{project}/compare/{branch}'

def open_url(url):
    Call.call('%s %s' % (_OPEN_COMMANDS[platform.system()], url))

def open_path(branch, path,
             project=Settings.PROJECT,
             user=Settings.USER):
    url = _URL.format(branch=branch, path=path, project=project, user=user)
    open_url(url)


def get_format_string(name, user, context):
    if not name:
        return

    if 'commits'.startswith(name):
        return _COMMIT

    if 'diffs'.startswith(name):
        return _DIFF

    if 'pulls'.startswith(name):
        if user == Settings.PROJECT_USER:
            return Pulls.pull_urls()[0]

        if user == Settings.USER:
            branch_name = '%s:%s' % (user, Git.branch())
            for number, (bname, _) in Git.pulls().items():
                if bname == branch_name:
                    context['number'] = number
                    return _PULL
            else:
                return _NEW_PULL

        raise ValueError("Can't pull for user %s." % user)

    if 'root'.startswith(name):
        name = GitRoot.root()

    full_path = os.getcwd()
    if name:
        path, f = os.path.split(name)
        full_path = os.path.join(full_path, path)
        if not os.path.exists(full_path):
            raise ValueError("Path %s doesn't exist." % full_path)
        if f:
            for p in os.listdir(full_path):
                if startswith(p, f):
                    full_path = os.path.join(full_path, p)
                    break
            else:
                raise ValueError("Can't find file matching " + name)

    if user != Settings.USER:
        context['branch'] = 'develop'
    context['path'] = os.path.relpath(full_path, GitRoot.ROOT)
    return _URL

def open(name='', user=''):
    if not platform.system() in _OPEN_COMMANDS:
        raise ValueError("Can't open a URL for platform.system() = " + plat)

    if user and 'upstream'.startswith(user):
        user = Settings.PROJECT_USER
    elif name > 1 and 'upstream'.startswith(name):
        user = Settings.PROJECT_USER
        name = ''
    elif user:
        for nickname, account in Remote.remote():
            if nickname == account:
                user = account
                break
    else:
        user = Settings.USER

    context = {
        'branch': Git.branch(),
        'user': user,
        'project_user': Settings.PROJECT_USER,
        'project': Settings.PROJECT,
    }

    fmt = get_format_string(name, user, context)
    open_url(fmt.format(**context))

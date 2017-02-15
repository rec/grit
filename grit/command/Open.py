from __future__ import absolute_import, division, print_function, unicode_literals

import os
import platform
import random

from grit import Call
from grit import Git
from grit import GitRoot
from grit import Project
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
PULL = 'https://github.com/{project_user}/{project}/pull/{number}'
_NEW_PULL = 'https://github.com/{user}/{project}/compare/{branch}?expand=1'
_DIFF = 'https://github.com/{user}/{project}/compare/{branch}'

def open_url(url):
    Call.call('%s %s' % (_OPEN_COMMANDS[platform.system()], url))

def get_context(user=None):
    return {
        'branch': Git.branch(),
        'user': user or Settings.USER,
        'project_user': Settings.PROJECT_USER,
        'project': Settings.PROJECT,
    }


import re

GIT_URL_MATCHER = re.compile(r'(\w+)@(\w+\.\w+):(\w+)/(\w+)\.git').match


def open_path(branch, path,
             project=Settings.PROJECT,
             user=Settings.USER):
    url = _URL.format(branch=branch, path=path, project=project, user=user)
    open_url(url)

def get_commits(user=None):
    return _COMMIT.format(**get_context(user))

def get_format_string(name, user, context):
    if name and 'commits'.startswith(name):
        return _COMMIT

    if name and 'diffs'.startswith(name):
        return _DIFF

    if name.isdigit():
        context['number'] = int(name)
        return PULL

    if name and 'pulls'.startswith(name):
        if user == Settings.PROJECT_USER:
            return Pulls.pull_urls()[0]

        if user == Settings.USER:
            branch_name = '%s:%s' % (user, Git.branch())
            for number, pull in Git.pulls().items():
                if pull.branch == branch_name:
                    context['number'] = number
                    return PULL
            else:
                return _NEW_PULL

        raise ValueError("Can't pull for user %s." % user)

    if name and 'root'.startswith(name):
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

    context['path'] = os.path.relpath(full_path, GitRoot.ROOT)
    return _URL



def get_remotes():
    remotes = {}
    for line in Call.run(['git', 'remote', '-v']).splitlines():
        name, url, direction = line.split()
        account, site, user, project = GIT_URL_MATCHER(url).groups()
        assert account == 'git' and site == 'github.com'
        remotes[name] = user, project

    return remotes


def get_url(name='', user=''):
    if not platform.system() in _OPEN_COMMANDS:
        raise ValueError("Can't open a URL for platform.system() = " + plat)

    remotes = get_remotes()
    origin = remotes.get('origin') or remotes.get('upstream')
    upstream = remotes.get('upstream') or remotes.get('origin')
    context = {
        'branch': Git.branch(),
        'user': origin[0],
        'project_user': upstream[0],
        'project': origin[1],
    }
    fmt = get_format_string(name, user, context)
    return fmt.format(**context)


def open(name='', user=''):
    open_url(get_url(name, user))

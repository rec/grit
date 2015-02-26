from __future__ import absolute_import, division, print_function, unicode_literals

from collections import namedtuple

from grit.Args import ARGS
from grit import Git
from grit import Settings

HELP = """
git p[ulls] [s[hort]]
    List all the outstanding pull requests for the current project.

    If the optional "short" argument is passed in, fit each pull into one line.
"""

_PULL_URL = 'https://github.com/{project_user}/{project}/pulls'
_PULL_HREF = '/{project_user}/{project}/pull/'

SAFE = True

_FORMATS = '#%s. %-24s  %s', '#%d. %s\n    %s\n'
def _to_string(number, branch, title):
    return _FORMATS[ARGS.expanded] % (number, branch, title)

def pull_urls():
    settings = {'project': Settings.PROJECT,
                'project_user': Settings.PROJECT_USER}
    return _PULL_URL.format(**settings), _PULL_HREF.format(**settings)

def pulls():
    for number, p in reversed(sorted(Git.pulls().items())):
        print(_to_string(number, p.branch, p.title))

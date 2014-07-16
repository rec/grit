from __future__ import absolute_import, division, print_function, unicode_literals

import bs4
from collections import namedtuple
import requests

from grit import Settings
from grit.command import Open

HELP = """
List all the outstanding pull requests for the current project.

   git p[ulls] [o[pen]]

If the optional "open" argument is passed in, open the pull page in the browser
instead.

"""

_PULL_URL = 'https://github.com/{project_user}/{project}/pulls'
_PULL_HREF = '/{project_user}/{project}/pull/'

SAFE = True

class Pull(namedtuple('Pull', 'user branch number description')):
    FORMAT = '#%s: %-24s  %s'

    def __str__(self):
        br = '%s:%s' % (self.user, self.branch)
        return self.FORMAT % (self.number, br, self.description)

def _pull_urls():
    settings = {'project': Settings.PROJECT,
                'project_user': Settings.PROJECT_USER}
    return _PULL_URL.format(**settings), _PULL_HREF.format(**settings)


def get_pulls():
    url, pull_href = _pull_urls()
    soup = bs4.BeautifulSoup(requests.get(url).text)
    pulls = []
    for s in soup.find_all('a', attrs='js-navigation-open'):
        href = s.attrs.get('href', '')
        if href.startswith(pull_href):
            pulls.append([href[len(pull_href):], s.text])

    branches = []
    for s in soup.find_all('span', attrs='css-truncate-target'):
        if ':' in s.text:
            branches.append(s.text.strip().split(':', 1))
    return [Pull(*(b + p)) for b, p in zip(branches, pulls)]

def open_pulls():
    url, _ = _pull_urls()
    Open.open_url(url)

def pulls(arg=''):
    if arg:
        if 'open'.startswith(arg):
            open_pulls()
        else:
            raise ValueError("Can't understand pull argument '%s'" % arg)
    else:
        for p in get_pulls():
            print(p)
 #

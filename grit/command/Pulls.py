from __future__ import absolute_import, division, print_function, unicode_literals

import bs4
from collections import namedtuple
import requests

from grit import Settings

HELP = """
List all the outstanding pull requests for the current project.
"""

_PULL_URL = 'https://github.com/{project_user}/{project}/pulls'
_PULL_HREF = '/{project_user}/{project}/pull/'

SAFE = True

class Pull(namedtuple('Pull', 'user branch number description')):
    FORMAT = '#%s: %-24s  %s'

    def __str__(self):
        br = '%s:%s' % (self.user, self.branch)
        return self.FORMAT % (self.number, br, self.description)

def get_pulls():
    settings = {'project': Settings.PROJECT,
                'project_user': Settings.PROJECT_USER}

    url = _PULL_URL.format(**settings)
    pull_href = _PULL_HREF.format(**settings)
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

def pulls():
    for p in get_pulls():
        print(p)
 #

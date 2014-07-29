from __future__ import absolute_import, division, print_function, unicode_literals

import bs4
from collections import namedtuple
import requests

from grit import Cache
from grit import Settings
from grit.command import Open

HELP = """
git p[ulls] [o[pen]]
    List all the outstanding pull requests for the current project.

    If the optional "open" argument is passed in, open the pull page in the
    browser instead.
"""

_PULL_URL = 'https://github.com/{project_user}/{project}/pulls'
_PULL_HREF = '/{project_user}/{project}/pull/'

SAFE = True

def _to_string(number, user, branch, description):
    return '#%s: %-24s  %s' % (number, ('%s:%s' % (user, branch)), description)

def _pull_urls():
    settings = {'project': Settings.PROJECT,
                'project_user': Settings.PROJECT_USER}
    return _PULL_URL.format(**settings), _PULL_HREF.format(**settings)

def get_soup(url):
    return bs4.BeautifulSoup(requests.get(url).text)

def get_pull_branch(href):
    url = 'https://github.com' + href
    soup = get_soup(url)
    current_branch = soup.find_all('span', {'class':'current-branch'})[1]
    result = [s.text for s in current_branch.find_all('span')]
    if len(result) == 1:
        result.insert(0, Settings.PROJECT_USER)
    return result

def get_pulls():
    cached_pulls = Cache.get('pulls') or {}
    url, pull_href = _pull_urls()
    soup = get_soup(url)
    pulls = {}
    for s in soup.find_all(attrs='issue-title-link'):
        href = s.attrs.get('href', '')
        if href.startswith(pull_href):
            number = str(int(href.split('/')[-1]))
            if number in cached_pulls:
                pulls[number] = cached_pulls[number]
            else:
                user, branch = get_pull_branch(href)
                pulls[number] = [user, branch, s.text.strip()]

    Cache.put('pulls', pulls)
    return pulls

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
        for number, parts in sorted(get_pulls().items()):
            print(_to_string(number, *parts))
 #

from __future__ import absolute_import, division, print_function, unicode_literals

import operator
import datetime

from grit import Git
from grit import Project
from grit.command import Open
from grit.command import Remote

HELP = """
grit slack [days]

  Print slackers.

"""

SAFE = True

def get_previous_business_day(days, date=None):
    date = date or datetime.datetime.today()
    while days:
        if date.weekday() < 5:
            days -= 1
        date -= datetime.timedelta(days=1)
    return date.isoformat()

def slack(days=3):
    days = int(days)
    inverse = Remote.inverse()
    slack = Project.settings('slack')

    previous = get_previous_business_day(days)
    def match(issue):
        if i['updated_at'] >= previous:
            return False
        for label in i['labels']:
            if label['name'] == 'Passed':
                return False
        return True

    slackers = [i for i in Git.issues() if match(i)]
    if not slackers:
        return;
    print('\nSlackers:')

    for issue in sorted(slackers, key=operator.itemgetter('updated_at')):
        try:
            user = '@' + slack[inverse[issue['user']['login']]]
            update = issue['updated_at'][:10]
            url = Open.get_url(str(issue['number']))
            print('  %-15s: %s (%s)' % (user, url, update))
        except Exception as e:
            print('ERROR:', e)
            raise
    print()

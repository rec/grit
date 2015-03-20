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
    date = date or datetime.datetime.utcnow()
    while True:
        if days <= 0:
            break
        if date.weekday() < 5:
            days -= 1
        date -= datetime.timedelta(days=1)
    return date.isoformat()

def slack(days=2):
    days = int(days)
    inverse = Remote.inverse()
    slack_names = Project.settings('slack')
    def slack(user):
        return '@' + slack_names[user]

    label_names = dict((v, k) for (k, v) in Project.settings('labels').items())

    def labels_to_names(labels):
        return ' '.join(
            slack(label_names[i]) for i in labels if i in label_names)

    previous = get_previous_business_day(days)
    def match(issue):
        if issue['updated_at'] >= previous:
            # print('too new:', issue['number'], issue['updated_at'], previous)
            return False
        for label in issue['labels']:
            if label['name'] in ('Passed', 'Hold'):
                # print('passed:', issue['number'])
                return False
        # print('slack:', issue['number'])
        return True

    if False:
        import json
        json.dump(Git.issues(), open('/tmp/git-issues.json', 'w'),
                  sort_keys=True, indent=4, separators=(',', ': '))
    slackers = [i for i in Git.issues() if match(i)]
    if not slackers:
        return;
    print('\nPull requests that are over %d business day%s stale:' % (
          days, '' if days == 1 else 's'))

    labels = Git.labels()
    for issue in sorted(slackers, key=operator.itemgetter('updated_at')):
        try:
            user = slack(inverse[issue['user']['login']]) + ':'
            update = issue['updated_at'][:10]
            url = Open.get_url(str(issue['number']))
            lab = labels_to_names(labels[issue['number']])
            print('  %s (%s): %s (%s)' % (url, update, user, lab))
        except Exception as e:
            print('ERROR:', e)
            raise
    print()

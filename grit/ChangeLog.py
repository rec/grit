from __future__ import absolute_import, division, print_function, unicode_literals

from grit.Singleton import singleton
from grit import Project

def filename():
    return Project.settings('version')['changelog']

@singleton
def changelog():
    lines = open(filename()).readlines()
    while lines and not lines[-1].strip():
        lines.pop()
    return lines

def write():
    open(filename(), 'w').writelines(changelog())

def status_line():
    return changelog()[-1]

def status(line=None):
    line = line or status_line()
    try:
        version, pulls = line.split(':')
    except:
        return
    results = []
    for p in pulls.replace('.', '').split():
        try:
            results.append(int(p))
        except:
            continue
    return version, results

def add_status_line(version, success, failure):
    parts = [version + ': ']
    for pulls, msg in [[success, 'Includes'], [failure, 'FAILED']]:
        if pulls:
            parts.extend(['%s pulls ' % msg, String.join_words(pulls), '. '])
    try:
        append = changelog()[-1].split(':')[0] != version
    except:
        append = True
    line = ''.join(parts).strip() + '\n'
    if append:
        changelog().append(line)
    else:
        changelog()[-1] = line
    write()

from __future__ import absolute_import, division, print_function, unicode_literals

from grit import Call
from grit import Git
from grit import Project
from grit import Settings

HELP = """

    grit test

Run the test for the current project.
"""

def run_test(cwd=None):
    test = Project.data('test.sh').strip()
    if not test:
        raise ValueError('No test!')
    Call.for_each(test.format(project=Settings.PROJECT), cwd=cwd)

def test():
    run_test(Git.root())
#

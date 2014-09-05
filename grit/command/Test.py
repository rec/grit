from __future__ import absolute_import, division, print_function, unicode_literals

from grit import Call
from grit import GitRoot
from grit import Project
from grit import Settings

from grit.String import banner

HELP = """
grit t[est]
    Run the tests for the current project.
"""

def run_test(cwd=None):
    test = Project.data('test.sh').strip()
    if not test:
        raise ValueError('No test!')
    Call.for_each(test.format(project=Settings.PROJECT), cwd=cwd)

def test():
    banner('Testing', Settings.PROJECT)
    run_test(GitRoot.ROOT)
    banner('Testing complete for', Settings.PROJECT)

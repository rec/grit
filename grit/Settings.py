from __future__ import absolute_import, division, print_function, unicode_literals

import os

PROJECT = os.environ.get('PROJECT', 'rippled')
USER = os.environ.get('GIT_USER') or os.environ.get('USER')
PROJECT_USER = os.environ.get('PROJECT_USER', 'ripple')

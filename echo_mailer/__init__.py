from __future__ import absolute_import

import os

from .main import *

name = "echo_mailer"


def init_echo_emailer():
    __home = str(Path.home())
    __config_dir = os.path.join(__home, '.echo_mailer')
    __config_file = os.path.join(__config_dir, 'config.json')

    if not os.path.exists(__config_dir):
        os.mkdir(__config_dir)
        # change mode to 700
        os.chmod(__config_dir, 0o700)

    if not os.path.exists(__config_file):
        with open(__config_file, 'w') as f:
            f.write('{}')
            f.write('\n')
        # change mode to 600
        os.chmod(__config_file, 0o600)


init_echo_emailer()

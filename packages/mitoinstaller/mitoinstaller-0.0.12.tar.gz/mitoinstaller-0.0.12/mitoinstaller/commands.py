"""
Contains useful commands for interacting
with the command line directly
"""

import subprocess
import sys

def install_pip_packages(*packages):
    """
    This function installs the given packages in a single pass
    using pip, through the command line.

    https://stackoverflow.com/questions/12332975/installing-python-module-within-code
    """

    sys_call = [sys.executable, "-m", "pip", "install"]

    for package in packages:
        sys_call.append(package)

    # Do we want want a check_call?
    subprocess.check_call(sys_call)

def upgrade_mito_installer():
    """
    Upgrades the mito installer package itself
    """
    import sys
    import subprocess

    # Do we want want a check_call?
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'mitoinstaller', '--upgrade', '--no-cache-dir'])

def exit_with_error(action, error=None):
    # Action should either be install or upgarde

    full_error = f'\n\nSorry, looks like we hit a problem during {action}.\n' + \
        ('' if error is None else ("It seems we " + error + "\n")) + \
        'We\'re happy to help you fix it, just shoot an email to jake@sagacollab.com.\n'

    print(full_error)
    exit(1)
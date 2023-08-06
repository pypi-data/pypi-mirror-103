"""
The Mito Installer package contains utils for installing
Mito within your Python enviornment.

Long term, we aim to meet:
1. This package has minimal dependencies, both for speed of download and the ultimate portability.
2. The installation attempts to fail as early as possible, and to give the user as much help
   help as possible while doing so.
"""
from mitoinstaller.install import install
from mitoinstaller.upgrade import upgrade
from mitoinstaller.user_install import get_user_field

def main():
    """
    The main function of the Mito installer, this function is responsible
    for either installing mitosheet or upgrading mitosheet.

    To install Mito (for the first time):
    python -m mitoinstaller install

    To upgrade Mito:
    python -m mitoinstaller upgrade
    """
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = ''

    if command == 'install':
        install()
    elif command == 'upgrade':
        upgrade()
    else:
        # If the user runs an invalid command, we attempt to guess if they
        # want to install or upgrade Mito, based on if it already has been
        # installed 
        install_finished = get_user_field('install_finished')
        if install_finished:
            print("Proper usage if `python -m mitoinstaller install` or `python -m mitoinstaller upgrade`\n\nMito is already installed, so try running the command `python -m mitoinstaller upgrade`\n")
        else:
            print("Proper usage if `python -m mitoinstaller install` or `python -m mitoinstaller upgrade`\n\nMito is not currently installed, so try running the command `python -m mitoinstaller install`\n")    

if __name__ == '__main__':
    main()
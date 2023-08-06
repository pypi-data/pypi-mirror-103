"""
Append these to print statements to set
them to a certain color. As this does
not currently work on windows, we simply set them
to empty strings
"""
import platform

if platform.system() == 'Darwin':
    RED_TEXT = '\033[1;31;40m'
    GREEN_TEXT = '\033[1;32;40m'
    NORMAL_TEXT = '\033[0;37;40m'
else:
    RED_TEXT = ''
    GREEN_TEXT = ''
    NORMAL_TEXT = ''
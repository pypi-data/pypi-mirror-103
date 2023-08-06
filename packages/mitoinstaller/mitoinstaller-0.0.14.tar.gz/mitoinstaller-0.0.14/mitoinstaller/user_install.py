import os
import uuid
import json
from mitoinstaller import __version__

# Where all global .mito files are stored
MITO_FOLDER = os.path.expanduser("~/.mito")

# The path of the user_install.json file, which contains
# relevant information to the install of mito
USER_INSTALL_PATH = os.path.join(MITO_FOLDER, 'user_install.json')

def get_random_id():
    """
    Creates a new random ID for the user, which for any given user,
    should only happen once.
    """
    return str(uuid.uuid1())


USER_INSTALL_DEFAULTS = {
    # The version of the installer that initially created this file
    'initial_installer_version': __version__,
    'static_user_id_install': get_random_id(),
    'install_finished': False,
}

def set_user_field(field, value):
    """
    Updates the value of a specific field in user_install.json
    """
    with open(USER_INSTALL_PATH, 'r') as user_file_old:
        old_user_json = json.load(user_file_old)
        old_user_json[field] = value
        with open(USER_INSTALL_PATH, 'w+') as f:
            f.write(json.dumps(old_user_json))

def get_user_field(field):
    """
    Returns the value stored at field in the user_install.json file
    """
    try:
        with open(USER_INSTALL_PATH) as f:
            return json.load(f)[field]
    except: 
        return None

def create_user_install():
    """
    Creates the user install file at the user install path, which
    is a file that contains information that is useful for the 
    mito installer.
    """
    if not os.path.exists(MITO_FOLDER):
        os.mkdir(MITO_FOLDER)

    if not os.path.exists(USER_INSTALL_PATH):
        with open(USER_INSTALL_PATH, 'w+') as f:
            # Take special care if we're in CI, so we don't generate
            # hundreds of account
            if 'CI' in os.environ and os.environ['CI'] is not None:
                USER_INSTALL_DEFAULTS['static_user_id_install'] = 'github_action'
            
            f.write(json.dumps(USER_INSTALL_DEFAULTS))
    
def get_static_user_id_install():
    return get_user_field('static_user_id_install')
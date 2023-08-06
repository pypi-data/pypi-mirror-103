"""
Upgrades the mitosheet package.
"""

from mitoinstaller.commands import exit_with_error, install_pip_packages
from mitoinstaller.log_utils import log, log_upgrade_failed, identify
from mitoinstaller.user_install import get_static_user_id_install, create_user_install

def upgrade_step_create_user_install():
    static_user_id_install = get_static_user_id_install()

    # If the user has no static install ID, create one
    if static_user_id_install is None:
        create_user_install()    
        # Reread the ID, as it is now defined
        static_user_id_install = get_static_user_id_install()
    
    identify()
    log('upgrade_started')

def upgrade_step_upgrade_mitosheet():
    install_pip_packages('mitosheet')

def upgrade_step_rebuild_jupyterlab():
    from jupyterlab import commands
    commands.build()

def upgrade_step_finish_upgrade():
    log('upgrade_finished')


UPGRADE_STEPS = [
    {
       'step_name': 'create user install JSON file',
       'execute':  upgrade_step_create_user_install
    }, 
    {
       'step_name': 'upgrade mitosheet',
       'execute':  upgrade_step_upgrade_mitosheet
    }, 
    {
        'step_name': 'rebuild JupyterLab',
        'execute': upgrade_step_rebuild_jupyterlab
    },
    {
        'step_name': 'finish upgrade',
        'execute': upgrade_step_finish_upgrade
    },
]

def upgrade():
    """
    Actually upgrades the mitosheet package
    """
    for upgrade_step in UPGRADE_STEPS:
        try:
            upgrade_step['execute']()
        except:
            error_message = "failed to " + upgrade_step['step_name']
            log_upgrade_failed(error_message)
            exit_with_error('upgrade', error_message)

    print('Mito has finished upgrading. Relaunch JupyterLab to complete the upgrade. \n\nRun the command:\tjupyter lab\n')
    
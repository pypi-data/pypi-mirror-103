"""
Upgrades the mitosheet package.
"""
import sys
import subprocess

from mitoinstaller.commands import exit_with_error
from mitoinstaller.log_utils import log, log_upgrade_failed

def upgrade_step_upgrade_mitosheet():
    log('upgrade_started')
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'mitosheet', '--upgrade'])

def upgrade_step_rebuild_jupyterlab():
    from jupyterlab import commands
    commands.build()

def upgrade_step_finish_upgrade():
    log('upgrade_finished')


UPGRADE_STEPS = [
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
    
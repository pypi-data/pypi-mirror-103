"""
We specify the installer as a list of steps that 
must run in order, for the installer.
"""
from mitoinstaller.commands import install_pip_packages, upgrade_mito_installer, exit_with_error
from mitoinstaller.log_utils import analytics, log, log_install_failed, identify
from mitoinstaller.user_install import (create_user_install, get_static_user_id_install, set_user_field)


def install_step_create_user_install():
    static_user_id_install = get_static_user_id_install()

    # If the user has no static install ID, create one
    if static_user_id_install is None:
        create_user_install()    
        # Reread the ID, as it is now defined
        static_user_id_install = get_static_user_id_install()
    
    identify()
    log('install_started')

# NOTE: this should be the same as the install requires in the 
# setup.py script in mitosheet
INSTALL_REQUIRES = [
    'jupyterlab>=2.0,<3.0,!=2.3.0,!=2.3.1', # there are css incompatabilities on version 2.3.1 and 2.3.0
    'ipywidgets>=7.0.0',
    'pandas>=1.1.0',
    'matplotlib>=3.3',
    'analytics-python'
]

def install_step_install_dependencies():
    install_pip_packages(*INSTALL_REQUIRES)


def install_step_install_mitosheet():
    install_pip_packages('mitosheet')


def install_step_install_jupyter_widget_manager():
    from jupyterlab import commands
    commands.install_extension('@jupyter-widgets/jupyterlab-manager@2')


def install_step_rebuild_jupyterlab():
    from jupyterlab import commands
    commands.build()


def install_step_upgrade_mitoinstaller():
    upgrade_mito_installer()


def install_step_finish_install():
    # Mark that we finished install
    set_user_field('install_finished', True)
    log('install_finished')
    


INSTALL_STEPS = [
    {
        'step_name': 'create user install JSON file',
        'execute': install_step_create_user_install
    },
    {
        'step_name': 'install dependencies',
        'execute': install_step_install_dependencies
    },
    {
        'step_name': 'install mitosheet',
        'execute': install_step_install_mitosheet
    },
    {
        'step_name': 'install @jupyter-widgets/jupyterlab-manager@2',
        'execute': install_step_install_jupyter_widget_manager
    },
    {
        'step_name': 'rebuild JupyterLab',
        'execute': install_step_rebuild_jupyterlab
    },
    {
        'step_name': 'upgrade mitoinstaller',
        'execute': install_step_upgrade_mitoinstaller
    },
    {
        'step_name': 'finish install',
        'execute': install_step_finish_install
    },
]

def install():
    for install_step in INSTALL_STEPS:
        try:
            install_step['execute']()
        except:
            error_message = "failed to " + install_step['step_name']
            log_install_failed(error_message)
            exit_with_error('install', error_message)

    print('Mito has finished installing. Relaunch JupyterLab to render your first mitosheet. \n\nRun the command:\tjupyter lab\n')
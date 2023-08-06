"""
The Mito Installer package contains utils for installing
Mito within your Jupyter enviornment. It takes special care
to guide the user 


Some thoughts:
1. We will have _no_ dependencies installed with the mitoinstaller package, for two reasons:
    1. First, speed. It'll be small and self-contained, so we can get it done as quick as possible
    2. Second, conflicts! The whole goal is to handle whatever package enviornemtn we find, and
       the more we install stuff the more likely to run into issues
2. Fail as early as possible, with as much information as possible. For example, we'd like to check 
   if the user has node before continuning installing. So we do this up font
"""

def install_pip_packages(*packages):
    """
    See answer here: https://stackoverflow.com/questions/12332975/installing-python-module-within-code
    """
    import subprocess
    import sys

    sys_call = [sys.executable, "-m", "pip", "install"]

    for package in packages:
        sys_call.append(package)

    # TODO: we don't want a check_call, but note the use of sys.executable!
    subprocess.check_call(sys_call)


def upgrade_mito_installer():
    import sys
    import subprocess

    print("UPGRADING")
    # TODO: we don't want a check_call, but note the use of sys.executable!
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'mitoinstaller', '--upgrade'])

def main():

    # First, we check that the user has node
    # TODO: take this from Jupyter Lab? We could check that the user has node
    # first, or we could take the code

    install_requires = [
        'jupyterlab>=2.0,<3.0,!=2.3.0,!=2.3.1', # there are css incompatabilities on version 2.3.1 and 2.3.0
        'ipywidgets>=7.0.0',
        'pandas>=1.1.0',
        'matplotlib>=3.3',
        # We don't need to lock an analytics-python version, as this library
        # is stabilized and mature
        'analytics-python'
    ]

    install_pip_packages(*install_requires)
    
    # Then, after installing all the dependecies, we install mitosheet
    install_pip_packages('mitosheet')

    # TODO: then, here, we should use the command line to install node js
    
    from jupyterlab import commands

    # Install the extension
    commands.install_extension('@jupyter-widgets/jupyterlab-manager@2')

    # Then, we rebuild Jupyter Lab
    commands.build()

    # Attempt to upgrade the package from within itself
    upgrade_mito_installer()

    # Then, prompt the user to launch jupyter lab
    print("Now, run the command 'jupyter lab'")



if __name__ == '__main__':
    main()
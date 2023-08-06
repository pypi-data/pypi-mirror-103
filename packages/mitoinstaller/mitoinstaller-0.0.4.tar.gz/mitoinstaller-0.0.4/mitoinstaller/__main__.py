"""
The Mito Installer package contains utils for installing
Mito within your Jupyter enviornment. It takes special care
to guide the user 


Some thoughts:
1. We will have _no_ dependencies installed with the mitoinstaller package, for two reasons:
    1. First, speed. It'll be small and self-contained, so we can get it done as quick as possible
    2. Second, conflicts! The whole goal is to handle whatever package enviornemtn we find, and
       the more we install stuff the more likely to run into issues
"""

def install_pip_package(package):
    """
    See answer here: https://stackoverflow.com/questions/12332975/installing-python-module-within-code
    """
    import subprocess
    import sys

    # TODO: we don't want a check_call, but note the use of sys.executable!
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():

    install_requires = [
        'jupyterlab>=2.0,<3.0,!=2.3.0,!=2.3.1', # there are css incompatabilities on version 2.3.1 and 2.3.0
        'ipywidgets>=7.0.0',
        'pandas>=1.1.0',
        'matplotlib>=3.3',
        # We don't need to lock an analytics-python version, as this library
        # is stabilized and mature
        'analytics-python'
    ]

    for package in install_requires:
        print(f'Installing {package}')
        install_pip_package(package)
    
    # Then, after installing all the dependecies, we install mitosheet
    install_pip_package('mitosheet')
    
    print("DONE!")
    return
    from jupyterlab import commands

    # Then, we rebuild Jupyter Lab
    commands.build()



if __name__ == '__main__':
    main()
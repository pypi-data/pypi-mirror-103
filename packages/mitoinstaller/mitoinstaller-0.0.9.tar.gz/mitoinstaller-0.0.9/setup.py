from distutils.core import setup
from mitoinstaller import __version__

setup(
    name='mitoinstaller',
    version=__version__,
    packages=['mitoinstaller',],
    install_requires=['analytics-python'],
    license='TODO',
    long_description='TODO',
)

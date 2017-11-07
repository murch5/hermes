from distutils.core import setup
from io_util.__init__ import __version__ as version

setup(
    name='io_util',
    version=version,
    packages=['io_util'],
    url='',
    license='',
    author='Ryan',
    author_email='',
    description='Input/Output Utility functions', requires=['pandas']
)

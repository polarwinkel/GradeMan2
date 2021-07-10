import os

os.chdir('build')

from distutils.core import setup
import py2exe
import app

setup(console=['GradeMan2Tray.py'])

# run with:
# py2exeInstall.py py2exe

import os, sys

import packaging
import packaging.version
import packaging.specifiers
import packaging.requirements

import setuptools
from distutils.core import setup
import py2exe
# TODO: Copy stuff to work-directory, clean up after finish
os.chdir('work')
sys.path.append(os.getcwd()+'\\GradeMan2')
import app

options={"py2exe": {"includes": ["pkg_resources._vendor.appdirs", 'packaging.specifiers', 'packaging.requirements', 'markdown']}}

setup(console=['GradeMan2Tray.py'], options=options)

# run with:
# py2exeInstall.py py2exe
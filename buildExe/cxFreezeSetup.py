import sys
from cx_Freeze import setup, Executable
import os, sys

sys.path.append(os.getcwd().replace('\\','/')+'/GradeMan2')
import app


os.chdir('build')

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ['os', 'app'], "excludes": []}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "GradeMan2",
    version = "2.0.0",
    author = "Dirk Winkel",
    description = "GradeMan2 Unterrichtsmanager und Notenassistent",
    options = {"build_exe": build_exe_options},
    executables = [Executable("GradeMan2Tray.py", base=base)]
)

# run with:
# cxFreezeSetup.py build

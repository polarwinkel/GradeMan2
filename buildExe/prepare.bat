mkdir work
xcopy ..\GradeMan2Tray.py work\
xcopy ..\GradeMan2 work\GradeMan2\ /E

pip install py2exe cx_freeze
pip install flask waitress markdown jinja2 pyyaml wxWidgets

# GradeMan2

Lehrer- und Notenassistent

## What is this

GradeMan2 is the all-new version of the GradeMan schoon management system for teachers.

## Public-Beta!

GradeMan2 is still in beta-state!

I use it in production already and all important features are running smoothly for me, yet some comfort-features are still missing.

Feel free to test it or even use it in production, I will appreciate any bug-reports! Just don't ask for missing features from the old GradeMan-version yet.

## How to run/test this

- clone the repository
- run the app.py:
    - on the desktop: Run `tray.py` to have the GradeMan2-Server in your system tray
    - on the server: I recommend to start it by executing `gunicorn --bind 0.0.0.0:5000 app:app`
    - for development: run `app.py`

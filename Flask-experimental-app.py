#!/usr/bin/python3
#coding: utf-8
'''
experimental Flask wsgi-interface for GradeMan2
'''

import os
import sqlite3
from flask import Flask, render_template, request, send_from_directory
import json
from jinja2 import Template

from modules import dbio, mdTeX2html

# global settings:

app = Flask(__name__, static_url_path='/static/')

dbfile = "grademan.sqlite3"
webServerPort = 8085

@app.route('/', methods=['GET'])
def index():
    '''show index-page'''
    db = dbio.GmDb(dbfile)
    relroot = './'
    with open('templates/base.tpl') as f:
        basetemplate = Template(f.read())
    with open('templates/nav.tpl') as f:
        nav = Template(f.read())
    with open('templates/index.tpl') as f:
        tmpl = Template(f.read())
    m = db.getMemos()
    mjson = json.dumps(m)
    t = db.getTimetable()
    tjson = json.dumps(t)
    c = db.getClasses()
    cjson = json.dumps(c)
    content = '<h1>!!! EXPERIMENTAL !!!</h1>'
    content += '<p>The Flask wsgi-interface is just for testing and development.</p>'
    content += '<p>TODO: remove Flask interface or migrate some day</p>'
    content += tmpl.render(mjson=mjson, tjson=tjson, cjson=cjson)
    return render_template('base.tpl', relroot=relroot, nav=nav.render(relroot=relroot), content=content)

@app.route('/static/<path:path>', methods=['GET'])
def sendStatic():
    if self.path.endswith('.css'):
        return send_from_directory('', path)

@app.route('/mdtex2html', methods=['POST'])
def post_mdtex2html():
    postvars = request.data
    print(postvars)
    try:
        return mdTeX2html.convert(postvars.decode("utf-8"))
    except Exception as e:
        return 'ERROR: Could not convert the mdTeX to HTML:' + str(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

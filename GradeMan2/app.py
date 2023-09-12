#!/usr/bin/python3
#coding: utf-8
'''
Flask wsgi-interface for GradeMan2
'''

import os, sys
import sqlite3
from flask import Flask, render_template, request, send_from_directory, make_response, jsonify
import json
from jinja2 import Template
from base64 import b64encode, b64decode, decodebytes
from io import BytesIO
from PIL import Image
import mdtex2html

from modules import dbio, settingsio

# global settings:

home = os.path.expanduser('~')
conffile=home+'/.GradeMan2conf.yaml'
port=4202

# start-stuff:
app = Flask(__name__)
settings = settingsio.settingsIo(conffile)
dbfile = settings.get('dbfile')
host = settings.get('host')
debug = settings.get('debug')
extensions = settings.get('extensions') # python-markdown extensions

# routes:

@app.route('/', methods=['GET'])
def index():
    '''show index-page'''
    # TODO: return settings if first run (no database)
    db = dbio.GmDb(dbfile)
    m = db.getMemos()
    t = db.getTimetable()
    c = db.getClasses()
    return render_template('index.html', relroot='./', mjson=m, tjson=t, cjson=c)

@app.route('/static/<path:path>', methods=['GET'])
def sendStatic(path):
    return send_from_directory('', path)

@app.route('/class/', methods=['GET'])
def newClass():
    c = {'cid':'', 'name':'', 'subject':'', 'graduate':'', 'memo':''}
    lShort = '[]'
    memo = ''
    return render_template('class.html', relroot='../', c=c, memo=memo, lShortJson=lShort)

@app.route('/class/<int:cid>', methods=['GET'])
def sendClass(cid):
    db = dbio.GmDb(dbfile)
    c = None
    if cid >= 0:
        c = db.getClass(cid)
        lShort = db.getClassLessonsShort(cid)
    if c == None: # offer new class if not found in db
        c = {'cid':'', 'name':'', 'subject':'', 'graduate':'', 'memo':''}
        lShort = '[]'
    memo = mdtex2html.convert(c['memo'], extensions)
    return render_template('class.html', relroot='../', c=c, memo=memo, lShortJson=lShort, dateHalfYear=settings.get('dateHalfYear'))

@app.route('/lesson/', methods=['GET'])
def newLesson():
    db = dbio.GmDb(dbfile)
    l = {'lid':'', 'date':'', 'cid':'', 'topic':'', 'count':'', 'memo':'', 'details':''}
    c = db.getClasses()
    return render_template('lesson.html', relroot='../', ljson=l, cjson=c)

@app.route('/lesson/class/<int:cid>', methods=['GET'])
def newClassLesson(cid):
    db = dbio.GmDb(dbfile)
    l = {'lid':'', 'date':'', 'cid':cid, 'topic':'', 'count':'', 'memo':'', 'details':''}
    c = db.getClasses()
    return render_template('lesson.html', relroot='../../', ljson=l, cjson=c)

@app.route('/lesson/<int:lid>', methods=['GET'])
def sendLesson(lid):
    db = dbio.GmDb(dbfile)
    l = db.getLesson(lid)
    c = db.getClasses()
    return render_template('lesson.html', relroot='../', ljson=l, cjson=c)

@app.route('/student/', methods=['GET'])
def newStudent():
    db = dbio.GmDb(dbfile)
    s = {'sid':'', 'givenname':'', 'familyname':'', 'gender':'', 'memo':''}
    img = ''
    memo = ''
    classes = db.getClasses()
    sclasses = db.getStudentClasses(s['sid'])
    return render_template('student.html', relroot='../', s=s, memo=memo, img=img, sjson=s, classes=classes, sclasses=sclasses)

@app.route('/student/<int:sid>', methods=['GET'])
def sendStudent(sid):
    db = dbio.GmDb(dbfile)
    s = db.getStudent(sid)
    if s is None:
        return render_template('404.html', relroot='../'), 404
    if s['img'] is not None:
        img = b64encode(s['img']).decode('utf-8')
    else:
        img = ''
    del s['img']
    memo = mdtex2html.convert(s['memo'], extensions)
    classes = db.getClasses()
    sclasses = db.getStudentClasses(sid)
    return render_template('student.html', relroot='../', s=s, memo=memo, img=img, sjson=s, classes=classes, sclasses=sclasses)

@app.route('/setStudentImg/<int:sid>', methods=['GET'])
def sendSetStudentImg(sid):
    return render_template('setStudentImg.html', relroot='../', sid=sid)

@app.route('/data', methods=['GET'])
def sendData():
    db = dbio.GmDb(dbfile)
    c = db.getClasses()
    return render_template('data.html', relroot='./', cjson=c)

@app.route('/mdTeXCheatsheet', methods=['GET'])
def sendMdTeXCheatSheet():
    return render_template('mdTeXCheatsheet.html', relroot='./')

@app.route('/settings', methods=['GET'])
def sendSettings():
    return render_template('settings.html', relroot='./', settings=settings.getJson())

@app.route('/getStudentImg/<int:sid>', methods=['GET'])
@app.route('/getStudentImg/<int:sid>.jpg', methods=['GET'])
def sendStudentImg(sid):
    '''send a student image as jpeg-file'''
    db = dbio.GmDb(dbfile)
    s = db.getStudent(sid)
    if s==None or s['img'] == None:
        return render_template('404.html', relroot='../'), 404
    img = (s['img'])
    response = make_response(img)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set('Content-Disposition', '', filename='%s.jpg' % sid)
    return response

@app.route('/getStudentImg/small/<int:sid>', methods=['GET'])
@app.route('/getStudentImg/small/<int:sid>.jpg', methods=['GET'])
def sendSmallStudentImg(sid):
    '''send a small student image as jpeg-file'''
    db = dbio.GmDb(dbfile)
    s = db.getStudent(sid)
    if s==None or s['img'] == None:
        return render_template('404.html', relroot='../'), 404
    img = (s['img'])
    stream = BytesIO(img)
    im = Image.open(stream)
    im.thumbnail((105, 135))
    with BytesIO() as output:
        im.save(output, format='jpeg')
        img = output.getvalue()
    response = make_response(img)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set('Content-Disposition', '', filename='%s.jpg' % sid)
    return response

@app.route('/json/<path:what>', methods=['GET'])
# TODO: split this up to separate routes
def sendJson(what):
    db = dbio.GmDb(dbfile)
    if what=='students':
        out = db.getStudents()
    elif what=='classes':
        out = db.getClasses()
    elif what.startswith('classStudents/'):
        cid = what[14:]
        if cid.isnumeric():
            out = db.getClassStudents(cid)
    elif what.startswith('classLesson/'):
        cid = what[12:]
        if cid.isnumeric():
            ll = db.getClassLessons(cid)
            l = {}
            l['lid'] = str(ll[-1]['lid'])
            l['date'] = str(ll[-1]['date'])
            l['topic'] = str(ll[-1]['topic'])
            l['memo'] = mdtex2html.convert(ll[-1]['memo'], extensions)
            l['details'] = mdtex2html.convert(ll[-1]['details'], extensions)
            out = l
    elif what.startswith('classLessons/'):
        cid = what[13:]
        if cid.isnumeric():
            ll = db.getClassLessons(cid)
            for l in ll:
                l['memo'] = mdtex2html.convert(l['memo'], extensions)
                l['details'] = mdtex2html.convert(l['details'], extensions)
            out = ll
    elif what.startswith('lessonAttendances/'):
        lid = what[18:]
        if lid.isnumeric():
            out = db.getLessonAttendances(lid)
    elif what.startswith('classAttendances/'):
        cid = what[17:]
        if cid.isnumeric():
            out = db.getClassAttendances(cid)
    elif what.startswith('studentAttendances/'):
        sid = what[19:]
        if sid.isnumeric():
            out = db.getStudentAttendances(sid)
    elif what=='timetable':
        out = db.getTimetable()
    else:
        return render_template('404.html', relroot='../'), 404
    return jsonify(out)

@app.route('/mdtex2html', methods=['POST'])
def post_mdtex2html():
    postvars = request.data
    try:
        return mdtex2html.convert(postvars.decode("utf-8"), extensions)
    except Exception as e:
        return 'ERROR: Could not convert the mdTeX to HTML:' + str(e)

@app.route('/setStudentImg/<int:sid>', methods=['POST'])
def setStudentImg(sid):
    db = dbio.GmDb(dbfile)
    print(str('hallo'), file=sys.stderr)
    f = request.files['image']
    # TODO: resize
    data = f.read()
    db.updateStudentImg(data, sid)
    content = 'student/%s' % sid
    return content

@app.route('/newDbEntry', methods=['POST'])
# TODO: check if RESTful:
def newDbEntry():
    db = dbio.GmDb(dbfile)
    if request.json['what'] == 'student':
        result = db.newStudent(request.json)
    elif request.json['what'] == 'class':
        result = db.newClass(request.json)
    elif request.json['what'] == 'lesson':
        result = db.newLesson(request.json)
    elif request.json['what'] == 'memo':
        result = db.newMemo(request.json)
    return str(result)

@app.route('/updateDbEntry', methods=['POST'])
@app.route('/updateDbEntry', methods=['PUT'])
# TODO: move all this to PUT-requests from frontend as well
def updateDbEntry():
    db = dbio.GmDb(dbfile)
    result = ''
    if request.json['what'] == 'student':
        result = db.updateStudent(request.json)
    elif request.json['what'] == 'class':
        result = db.updateClass(request.json)
    elif request.json['what'] == 'lesson':
        result = db.updateLesson(request.json)
    elif request.json['what'] == 'attendances':
        result = db.updateAttendances(request.json)
    elif request.json['what'] == 'memo':
        result = db.updateMemo(request.json)
    elif request.json['what'] == 'timetable':
        result = db.updateTimetable(request.json)
    if result == '':
        content = 'ERROR 400: Bad request, I didn\'t understand _what_ I shall update!'
    elif result == 0:
        content = 'ok'
    else:
        content = 'ERROR 500: SQL-Error: '+str(result)
    return content

@app.route('/updateSettings', methods=['PUT'])
def updateSettings():
    setnew = request.json
    if 'False' in setnew['extensions']:
        setnew['extensions'] = list(dict.fromkeys(setnew['extensions']))
        setnew['extensions'].remove('False')
    settings.set(setnew, conffile)
    global dbfile
    dbfile = settings.get('dbfile')
    global host
    host = settings.get('host')
    global debug
    debug = settings.get('debug')
    global extensions
    extensions = settings.get('extensions')
    content = 'ok'
    return content

@app.route('/deleteDbEntry', methods=['DELETE'])
# TODO: Requests to delete database-entries
def deleteDbEntry():
    db = dbio.GmDb(dbfile)
    result = ''
    if request.json['what'] == 'student':
        result = db.deleteStudent(request.json['sid'])
    elif request.json['what'] == 'class':
        result = db.deleteClass(request.json['cid'])
    elif request.json['what'] == 'lesson':
        result = db.deleteLesson(request.json['lid'])
    elif request.json['what'] == 'attendances':
        result = db.deleteAttendances(request.json['aid'])
    elif request.json['what'] == 'memo':
        result = db.deleteMemo(request.json['mid'])
    if result == '':
        content = 'ERROR 400: Bad request, I didn\'t understand _what_ I shall delete!'
    elif result == 0:
        content = 'ok'
    else:
        content = 'ERROR 500: SQL-Error: '+str(result)
    return content

@app.errorhandler(404)
def error_not_found(error):
    return render_template('404.html'), 404

# run it:

if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug)

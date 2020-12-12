#!/usr/bin/python3
#coding: utf-8
'''
Base file of GradeMan2
'''

import os
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header, parse_multipart, FieldStorage
from urllib import parse
import json
from jinja2 import Template
from multiprocessing import Process
from base64 import b64encode, b64decode, decodebytes
from io import BytesIO
from PIL import Image

from modules import dbio, mdTeX2html

# global settings:

dbfile = "grademan.sqlite3"
webServerPort = 8085

# WebServer stuff:

class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
    ''' HTTPRequestHandler class '''
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
    def do_HEAD(s):
        self._set_headers;
    
    def do_GET(self):
        ''' The GET-Handler returns a certain page or json-data-string '''
        # non-HTML requests:
        if self.path.startswith('/static/'):
            self.sendStatic()
            return
        elif self.path.startswith('/json/'):
            what = self.path[6:]
            if what=='students':
                s = db.getStudents()
                out = json.dumps(s)
            elif what=='classes':
                c = db.getClasses()
                out = json.dumps(c)
            elif what.startswith('classStudents/'):
                cid = what[14:]
                if cid.isnumeric():
                    s = db.getClassStudents(cid)
                    out = json.dumps(s)
            elif what.startswith('classLessons/'):
                cid = what[13:]
                if cid.isnumeric():
                    ll = db.getClassLessons(cid)
                    for l in ll:
                        l['memo'] = mdTeX2html.convert(l['memo'])
                        l['details'] = mdTeX2html.convert(l['details'])
                    out = json.dumps(ll)
            elif what.startswith('lessonAttendances/'):
                lid = what[18:]
                if lid.isnumeric():
                    aa = db.getLessonAttendances(lid)
                    out = json.dumps(aa)
            elif what.startswith('classAttendances/'):
                cid = what[17:]
                if cid.isnumeric():
                    aa = db.getClassAttendances(cid)
                    out = json.dumps(aa)
            elif what=='timetable':
                t = db.getTimetable()
                out = json.dumps(t)
            else:
                out = 'ERROR 404: Not found'
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(out, 'utf8'))
            return
        elif self.path.startswith('/getStudentImg/'):
            self.sendStudentImg()
            return
        
        self._set_headers()
        with open('templates/base.tpl') as f:
            basetemplate = Template(f.read())
        with open('templates/nav.tpl') as f:
            nav = Template(f.read())
        relroot = './'
        
        # switch for the path:
        if self.path == '/':
            with open('templates/index.tpl') as f:
                tmpl = Template(f.read())
            m = db.getMemos()
            mjson = json.dumps(m)
            t = db.getTimetable()
            tjson = json.dumps(t)
            c = db.getClasses()
            cjson = json.dumps(c)
            content = tmpl.render(mjson=mjson, tjson=tjson, cjson=cjson)
        elif self.path == '/reloadDb': # TODO: remove for stable
            db.reloadDb(dbfile)
            content = '<p>Datenbank erfolgreich neu geladen!</p><br />\n'
        elif self.path == '/test': # TODO: remove for stable
            content = '<p>Dein Pfad: %s</p><br />\n' % self.path
            content += getHtml.getTest()
        elif self.path.startswith('/student/'):
            # student page(s)
            relroot = '../'
            sid = self.path.strip('/student/')
            s = None
            if sid.isnumeric():
                s = db.getStudent(sid)
            if s == None:
                s = {'sid':'', 'givenname':'', 'familyname':'', 'gender':'', 'memo':''}
            if 'img' in s:
                if s['img'] is not None:
                    img = b64encode(s['img']).decode('utf-8')
                else:
                    img = ''
                del s['img']
            else: 
                img = ''
            memo = mdTeX2html.convert(s['memo'])
            sjson = json.dumps(s)
            classes = db.getClasses()
            sclasses = db.getStudentClasses(sid)
            with open('templates/student.tpl') as f:
                tmpl = Template(f.read())
            content = tmpl.render(s=s, memo=memo, img=img, sjson=sjson, classes=classes, sclasses=sclasses)
        elif self.path.startswith('/class/'):
            # class page(s)
            relroot = '../'
            cid = self.path.strip('/class/')
            c = None
            if cid.isnumeric():
                c = db.getClass(cid)
                lShort = db.getClassLessonsShort(cid)
                lShortJson = json.dumps(lShort)
            if c == None:
                c = {'cid':'', 'name':'', 'subject':'', 'graduate':'', 'memo':''}
                lShortJson = []
            memo = mdTeX2html.convert(c['memo'])
            cjson = json.dumps(c)
            with open('templates/class.tpl') as f:
                tmpl = Template(f.read())
            content = tmpl.render(relroot=relroot, c=c, memo=memo, cjson=cjson, lShortJson=lShortJson)
        elif self.path.startswith('/lesson/'):
            # lesson page(s)
            relroot = '../'
            lid = self.path.strip('/lesson/')
            l = None
            if lid.isnumeric():
                l = db.getLesson(lid)
            if l == None:
                l = {'lid':'', 'date':'', 'cid':'', 'topic':'', 'count':'', 'memo':'', 'details':''}
            ljson = json.dumps(l)
            c = db.getClasses()
            cjson = json.dumps(c)
            with open('templates/lesson.tpl') as f:
                tmpl = Template(f.read())
            content = tmpl.render(relroot=relroot, ljson=ljson, cjson=cjson)
        elif self.path == '/data':
            c = db.getClasses()
            cjson = json.dumps(c)
            with open('templates/data.tpl') as f:
                tmpl = Template(f.read())
            content = tmpl.render(relroot=relroot, cjson=cjson)
        elif self.path == '/mdTeXCheatsheet':
            with open('templates/mdTeXCheatsheet.tpl') as f:
                tmpl = Template(f.read())
            content = tmpl.render()
        elif (self.path.startswith('/setStudentImg/')
                and self.path.strip('/setStudentImg/').isnumeric()):
            relroot = '../'
            sid = self.path.strip('/setStudentImg/')
            with open('templates/setStudentImg.tpl') as f:
                tmpl = Template(f.read())
            content = tmpl.render(sid=sid)
        else:
            content = 'ERROR 404: The path was not found by GradeMan'
            content += '<p>Your path: %s</p><br />\n' % self.path
        
        # Write content as utf-8 data
        out = basetemplate.render(relroot=relroot, nav=nav.render(relroot=relroot), content=content)
        self.wfile.write(bytes(out, 'utf8'))
        return
    
    def sendStatic(self):
        '''send a static file from static-folder'''
        try:
            #Check the file extension required and set the right mime type
            sendReply = False
            if self.path.endswith('.js'):
                mimetype='application/javascript'
                sendReply = True
            elif self.path.endswith('.css'):
                mimetype='text/css'
                sendReply = True
            elif self.path.endswith('.svg'):
                mimetype='image/svg+xml'
                sendReply = True
            elif self.path.endswith('.woff2'):
                mimetype = 'application/font-woff2'
                sendReply = True
            if sendReply == True:
                #Open the static file requested and send it
                fipath = (str(os.getcwd())+self.path)
                f = open(fipath, 'rb')
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            else:
                self.send_error(501,'unsupported file type on path %s' % self.path)
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
    
    def sendStudentImg(self):
        '''send a student image as jpeg-file'''
        if self.path.strip('/getStudentImg/').isnumeric():
            sid = self.path.strip('/setStudentImg/')
            small = False
        elif self.path.strip('/setStudentImg/small/').isnumeric():
            sid = self.path.strip('/setStudentImg/small')
            small = True
        else:
            self.send_error(404, 'File not found')
            return
        s = db.getStudent(sid)
        if s==None or s['img'] == None:
            self.send_error(404, 'File not found')
            return
        self.send_response(200)
        self.send_header('Content-type','image/jpeg')
        self.end_headers()
        img = (s['img'])
        if small:
            stream = BytesIO(img)
            im = Image.open(stream)
            #im = Image.frombuffer('RGB', (350, 450), stream)
            im.thumbnail((105, 135))
            with BytesIO() as output:
                im.save(output, format='jpeg')
                img = output.getvalue()
        self.wfile.write(img)
    
    def parsePost(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'application/json':
            length = int(self.headers['content-length'])
            postvars = json.loads(self.rfile.read(length).decode('utf-8'))
        elif ctype == 'application/mdtex':
            length = int(self.headers['content-length'])
            postvars = self.rfile.read(length).decode('utf-8')
        else:
            postvars = {}
        return postvars
    
    def do_POST(self):
        ''' all operations on an exercise like editing is done via POST-Requests '''
        self._set_headers()
        relroot = ''
        
        # path-switch:
        if self.path == '/mdtex2html':
            postvars = self.parsePost()
            try:
                content = mdTeX2html.convert(postvars)
            except Exception as e:
                content = 'ERROR: Could not convert the mdTeX to HTML:' + str(e)
        elif self.path.startswith('/getHtml'): # TODO: move this to GET JSON and render on client-side
            postvars = self.parsePost()
            if postvars['what'] == 'attendances':
                attendances = db.getLessonAttendances(postvars['lid'])
                students = db.getClassStudents(postvars['cid'])
                content = getHtml.attendances(attendances, students)
        elif (self.path.startswith('/setStudentImg/') 
                and self.path.strip('/setStudentImg/').isnumeric()):
            sid = self.path.strip('/setStudentImg/')
            form = FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
            data = form['img'].file.read()
            #open("./img/%s.jpg" % sid, "wb").write(data)
            db.updateStudentImg(data, sid)
            #self.send_response(302)
            #self.send_header('Location', '/viewStudent/%s' % sid)
            #self.end_headers()
            # 302 redirect doesn't work because 200 OK answer is faster!
            # see https://docs.python.org/3/library/http.server.html
            # redirect on client side!
            content = 'student/%s' % sid
        elif self.path == '/newDbEntry':
            postvars = self.parsePost()
            result = ''
            if postvars['what'] == 'student':
                result = db.newStudent(postvars)
            elif postvars['what'] == 'class':
                result = db.newClass(postvars)
            elif postvars['what'] == 'lesson':
                result = db.newLesson(postvars)
            elif postvars['what'] == 'memo':
                result = db.newMemo(postvars)
            if result == '':
                content = 'ERROR 400: Bad request, I didn\'t understand _what_ I shall insert!'
            elif isinstance(result,int):
                content = str(result)
            else:
                content = result
        elif self.path == '/updateDbEntry': # TODO: move this to PUT-requests
            postvars = self.parsePost()
            result = ''
            if postvars['what'] == 'student':
                result = db.updateStudent(postvars)
            elif postvars['what'] == 'class':
                result = db.updateClass(postvars)
            elif postvars['what'] == 'lesson':
                result = db.updateLesson(postvars)
            elif postvars['what'] == 'memo':
                result = db.updateMemo(postvars)
            elif postvars['what'] == 'timetable':
                result = db.updateTimetable(postvars)
            if result == '':
                content = 'ERROR 400: Bad request, I didn\'t understand _what_ I shall update!'
            elif result == 0:
                content = 'ok'
            else:
                content = 'ERROR 500: SQL-Error: '+str(result)
        else:
            content = 'ERROR 404: URL not found for POST!'
        # Write content as utf-8 data
        self.wfile.write(bytes(content, "utf8"))
        return
    
    def do_PUT(self):
        ''' TODO: Requests to update database-entries '''
        postvars = self.parsePost()
        result = ''
        if postvars['what'] == 'student':
            result = db.updateStudent(postvars)
        #elif postvars['what'] == 'class':
        #    result = db.updateClass(postvars)
        elif postvars['what'] == 'lesson':
            result = db.updateLesson(postvars)
        elif postvars['what'] == 'attendances':
            result = db.updateAttendances(postvars)
        #elif postvars['what'] == 'memo':
        #    result = db.updateMemo(postvars)
        #elif postvars['what'] == 'timetable':
        #    result = db.updateTimetable(postvars)
        if result == '':
            content = 'ERROR 400: Bad request, I didn\'t understand _what_ I shall update!'
        elif result == 0:
            content = 'ok'
        else:
            content = 'ERROR 500: SQL-Error: '+str(result)
    
    def do_DELETE(self):
        ''' TODO: Requests to delete database-entries '''
        self._set_headers()
        # task-switch:
        postvars = self.parsePost()
        result = ''
        if postvars['what'] == 'student':
            result = db.deleteStudent(postvars['sid'])
        elif postvars['what'] == 'class':
            result = db.deleteClass(postvars['cid'])
        elif postvars['what'] == 'lesson':
            result = db.deleteLesson(postvars['lid'])
        elif postvars['what'] == 'attendances':
            result = db.deleteAttendances(postvars['aid'])
        elif postvars['what'] == 'memo':
            result = db.deleteMemo(postvars['mid'])
        if result == '':
            content = 'ERROR 400: Bad request, I didn\'t understand _what_ I shall delete!'
        elif result == 0:
            content = 'ok'
        else:
            content = 'ERROR 500: SQL-Error: '+str(result)

def runWebServer():
    ''' start the webserver '''
    print('starting server')
    server_address = ('127.0.0.1', webServerPort)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    print('server is running on port '+str(webServerPort))
    httpd.serve_forever()

# get it started:

db = dbio.GmDb(dbfile)

webServer = Process(target=runWebServer, args=())
webServer.start()

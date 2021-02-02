#!/usr/bin/python3
'''
Database-IO-file of TeXerBase - an Database Server for Exercises
'''

import sqlite3
import os
from modules import dbInit

class GmDb:
    ''' Database-Connection to the TeXerBase-Database '''
    def __init__(self, dbfile):
        if not os.path.exists(dbfile):
            connection = sqlite3.connect(dbfile)
            cursor = connection.cursor()
            # activate support for foreign keys in SQLite:
            sql_command = 'PRAGMA foreign_keys = ON;'
            cursor.execute(sql_command)
            connection.commit()
            connection.close()
        self._connection = sqlite3.connect(dbfile) # _x = potected, __ would be private
        dbInit.checkTables(self)
    
    def reloadDb(self, dbfile):
        '''reloads the database file, i.e. after external changes/sync'''
        self._connection.commit() # not necessary, just to be sure
        self._connection.close()
        self._connection = sqlite3.connect(dbfile)
    
    def newStudent(self, s):
        ''' inserts a new student and returns it's id, -1 for error '''
        cursor = self._connection.cursor()
        valuelist = (
                    s['givenname'],
                    s['familyname'],
                    s['gender'],
                    s['memo']
                )
        sqlTemplate = '''SELECT id FROM students WHERE 
                givenname=? and familyname=? and gender=? and memo=?'''
        cursor.execute(sqlTemplate, valuelist)
        result = cursor.fetchone()
        if result != None:
            return 'FAILED: Identical entry found with id %s, differ at least memo!' % str(result)
        sqlTemplate = '''INSERT INTO students 
                (givenname, familyname, gender, memo) 
                VALUES (?, ?, ?, ?)'''
        try:
            cursor.execute(sqlTemplate, valuelist)
        except sqlite3.OperationalError as err:
            args = list(err.args)
            return 'FAILED: SQL-Error: '+str(args)
        self._connection.commit()
        sqlTemplate = '''SELECT id FROM students WHERE 
                givenname=? and familyname=? and gender=? and memo=?'''
        cursor.execute(sqlTemplate, valuelist)
        result = cursor.fetchone()[0]
        self.setStudentClasses(result, s['cids'])
        return result
    
    def getStudent(self, sid):
        ''' get a student from it's id '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM students WHERE id=?'''
        cursor.execute(sqlTemplate, (sid, ))
        tup = cursor.fetchone()
        if tup is None:
            return None
        result = {
                    'sid'       : tup[0],
                    'givenname' : tup[1],
                    'familyname': tup[2],
                    'gender'    : tup[3],
                    'memo'      : tup[4],
                    'img'       : tup[5]
                }
        return result
    
    def updateStudent(self, s):
        ''' updates the db-entry for a student, returning 0 or error-string '''
        cursor = self._connection.cursor()
        sqlTemplate = '''UPDATE students SET givenname=?, familyname=?, gender=?, memo=? WHERE id=?'''
        valuelist = (
                    s['givenname'],
                    s['familyname'],
                    s['gender'],
                    s['memo'],
                    s['sid']
                )
        try:
            cursor.execute(sqlTemplate, valuelist)
        except sqlite3.OperationalError as err:
            args = list(err.args)
            return 'FAILED: SQL-Error: '+str(args)
        self._connection.commit()
        self.setStudentClasses(s['sid'], s['cids'])
        return 0
    
    def updateStudentImg(self, img, sid):
        ''' inserts or updates the image for a student, returning 0 or error-string '''
        cursor = self._connection.cursor()
        sqlTemplate = '''UPDATE students SET img=? WHERE id=?'''
        try:
            cursor.execute(sqlTemplate, (img, sid))
        except sqlite3.OperationalError as err:
            args = list(err.args)
            return 'FAILED: SQL-Error: '+str(args)
        self._connection.commit()
        return 0
    
    def getStudents(self):
        ''' get all students '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT id, givenname, familyname, gender FROM students ORDER BY familyname, givenname'''
        cursor.execute(sqlTemplate)
        tlist = cursor.fetchall()
        result = []
        for tup in tlist:
            s = {
                        'sid'       : tup[0],
                        'givenname' : tup[1],
                        'familyname': tup[2],
                        'gender'    : tup[3]
                    }
            result.append(s)
        return result
    
    def getStudentAttendances(self, sid):
        ''' get all addendances of a student '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT lid, cid, date, topic, count, 
                attendant, excused, homework, performance, participation, attendances.memo 
                FROM attendances LEFT JOIN lessons 
                ON attendances.lid=lessons.id 
                WHERE sid=?
                ORDER BY date DESC'''
        cursor.execute(sqlTemplate, (sid, ))
        atts = cursor.fetchall()
        if atts is None:
            return None
        attendances = []
        for att in atts:
            a = {
                        'lid'           : att[0],
                        'cid'           : att[1],
                        'date'          : att[2],
                        'topic'         : att[3],
                        'count'         : att[4],
                        'attendant'     : att[5],
                        'excused'       : att[6],
                        'homework'      : att[7],
                        'performance'   : att[8],
                        'participation' : att[9],
                        'memo'          : att[10]
                    }
            attendances.append(a)
        return attendances
    
    def newClass(self, c):
        ''' inserts a new class and returns it's id, -1 for error '''
        cursor = self._connection.cursor()
        valuelist = (
                    c['name'],
                    c['subject'],
                    c['graduate'],
                    c['memo']
                )
        valueli = (
                    c['name'],
                    c['subject']
                )
        sqlTemplate = '''SELECT id FROM classes WHERE 
                name=? and subject=?'''
        cursor.execute(sqlTemplate, valueli)
        result = cursor.fetchone()
        if result != None:
            return 'FAILED: Identical entry found with id %s, differ at least one: name or subject!' % str(result)
        sqlTemplate = '''INSERT INTO classes 
                (name, subject, graduate, memo) 
                VALUES (?, ?, ?, ?)'''
        try:
            cursor.execute(sqlTemplate, valuelist)
        except sqlite3.OperationalError as err:
            args = list(err.args)
            return 'FAILED: SQL-Error: '+str(args)
        self._connection.commit()
        sqlTemplate = '''SELECT id FROM classes WHERE 
                name=? and subject=?'''
        cursor.execute(sqlTemplate, valueli)
        result = cursor.fetchone()[0]
        return result
    
    def getClass(self, cid):
        ''' get a class from it's id '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM classes WHERE id=?'''
        cursor.execute(sqlTemplate, (cid, ))
        tup = cursor.fetchone()
        if tup is None:
            return None
        result = {
                    'cid'       : tup[0],
                    'name'      : tup[1],
                    'subject'   : tup[2],
                    'graduate'  : tup[3],
                    'memo'      : tup[4],
                }
        return result
    
    def getClasses(self):
        ''' get all classes '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM classes ORDER BY name, subject'''
        cursor.execute(sqlTemplate)
        tlist = cursor.fetchall()
        result = []
        for tup in tlist:
            s = {
                        'cid'       : tup[0],
                        'name'      : tup[1],
                        'subject'   : tup[2],
                        'graduate'  : tup[3],
                        'memo'      : tup[4],
                    }
            result.append(s)
        return result
    
    def updateClass(self, c):
        ''' updates the db-entry for a class, returning 0 or error-string '''
        cursor = self._connection.cursor()
        sqlTemplate = '''UPDATE classes SET name=?, subject=?, graduate=?, memo=? WHERE id=?'''
        valuelist = (
                    c['name'],
                    c['subject'],
                    c['graduate'],
                    c['memo'],
                    c['cid']
                )
        try:
            cursor.execute(sqlTemplate, valuelist)
        except sqlite3.OperationalError as err:
            args = list(err.args)
            return 'FAILED: SQL-Error: '+str(args)
        self._connection.commit()
        return 0
    
    def setStudentClasses(self, sid, cids):
        ''' set classes for a student '''
        cursor = self._connection.cursor()
        sqlTemplate = '''DELETE FROM studentclass WHERE sid=?'''
        cursor.execute(sqlTemplate, (sid, ))
        self._connection.commit()
        sqlTemplate = '''INSERT INTO studentclass (sid, cid)
                VALUES (?, ?)'''
        for cid in cids:
            if cid.isnumeric():
                cursor.execute(sqlTemplate, (sid, cid))
        self._connection.commit()
        return 0
    
    def getStudentClasses(self, sid):
        ''' get a list of the classes that a student is member of '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT cid FROM studentclass WHERE sid=?'''
        try:
            cursor.execute(sqlTemplate, (sid, ))
        except sqlite3.OperationalError as err:
            args = list(err.args)
            return 'FAILED: SQL-Error: '+str(args)
        cids = cursor.fetchall()
        sqlTemplate = '''SELECT * FROM classes WHERE id=?'''
        result = []
        for cid in cids:
            cursor.execute(sqlTemplate, (str(cid[0]), ))
            tup = cursor.fetchall()[0]
            c = {
                        'cid'       : tup[0],
                        'name'      : tup[1],
                        'subject'   : tup[2],
                        'graduate'  : tup[3],
                        'memo'      : tup[4],
                    }
            result.append(c)
        self._connection.commit()
        return result
    
    def getClassStudents(self, cid):
        ''' get a list of the students that are member of a class '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT sid, givenname, familyname, gender, memo 
                FROM students LEFT JOIN studentclass ON students.id = studentclass.sid 
                WHERE cid=? ORDER BY familyname, givenname'''
        students = cursor.execute(sqlTemplate, (cid, ))
        result = []
        for s in students:
            s = {
                        'sid'       : s[0],
                        'givenname' : s[1],
                        'familyname': s[2],
                        'gender'    : s[3],
                        'memo'      : s[4],
                    }
            result.append(s)
        self._connection.commit()
        return result
    
    def getClassLessonsShort(self, cid):
        ''' get the lessons of a class '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM lessons WHERE cid=? ORDER BY date'''
        cursor.execute(sqlTemplate, (cid, ))
        lessons = cursor.fetchall()
        if lessons is None:
            return None
        result = []
        for les in lessons:
            l = {
                        'lid'       : les[0],
                        'date'      : les[1],
                        'topic'     : les[3],
                        'count'     : les[4],
                    }
            result.append(l)
        return result
    
    def getClassLessons(self, cid):
        ''' get the lessons of a class '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM lessons WHERE cid=? ORDER BY date'''
        cursor.execute(sqlTemplate, (cid, ))
        lessons = cursor.fetchall()
        if lessons is None:
            return None
        result = []
        for les in lessons:
            l = {
                        'lid'       : les[0],
                        'date'      : les[1],
                        'topic'     : les[3],
                        'count'     : les[4],
                        'memo'      : les[5],
                        'details'   : les[6],
                    }
            result.append(l)
        return result
    
    def getClassAttendances(self, cid):
        ''' get all addendances of a class '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT id AS sid, givenname, familyname FROM students
                LEFT JOIN studentclass ON students.id=studentclass.sid WHERE cid=?
                ORDER BY familyname, givenname'''
        cursor.execute(sqlTemplate, (cid, ))
        stus = cursor.fetchall()
        if stus is None:
            return None
        students = []
        for stu in stus:
            s = {
                        'sid'       : stu[0],
                        'givenname' : stu[1],
                        'familyname': stu[2],
                    }
            students.append(s)
        lShort = self.getClassLessonsShort(cid)
        attendances = []
        for l in lShort:
            att = {'lid': l['lid'], }
            la = self.getLessonAttendances(l['lid']);
            for s in students:
                aFound = False
                sid = s['sid']
                for a in la:
                    if str(a['sid']) == str(sid):
                        att[str(sid)] = a
                        aFound = True
                        break
                if not aFound:
                    att[sid] = {}
            attendances.append(att)
        result = {'students':students, 'attendances':attendances}
        return result
    
    def newAttendances(self, lid):
        ''' inserts new attendances for a lesson '''
        cursor = self._connection.cursor()
        l = self.getLesson(lid)
        sqlTemplate = '''INSERT INTO attendances
                (lid, sid, memo) 
                VALUES (?, ?, '')'''
        ss = self.getClassStudents(l['cid'])
        for s in ss:
            cursor.execute(sqlTemplate, (l['lid'], s['sid']))
        self._connection.commit()
        return 0
    
    def getLessonAttendances(self, lid):
        ''' get attendances for a lesson '''
        cursor = self._connection.cursor()
        sqlTemplate = '''
                SELECT * FROM (SELECT * FROM attendances WHERE lid=?) 
                LEFT JOIN (SELECT id AS sid, givenname, familyname FROM students) 
                USING(sid) ORDER BY familyname'''
        cursor.execute(sqlTemplate, (lid, ))
        attendances = cursor.fetchall()
        if attendances is None:
            return None
        result = []
        for att in attendances:
            a = {
                        'lid'          : att[0],
                        'sid'          : att[1],
                        'attendant'    : att[2],
                        'excused'      : att[3],
                        'homework'     : att[4],
                        'performance'  : att[5],
                        'participation': att[6],
                        'memo'         : att[7],
                        'givenname'    : att[8],
                        'familyname'   : att[9],
                    }
            result.append(a)
        return result
    
    def updateAttendances(self, attendances):
        ''' updates the db-entry for a dict of attendances, returning 0 or error-string '''
        cursor = self._connection.cursor()
        sqlTemplate = '''UPDATE attendances 
                SET attendant=?, excused=?, homework=?, performance=?, participation=?, memo=?
                WHERE lid=? AND sid=?'''
        if type(attendances['sid']) is type(''):
            valuelist = (
                        attendances['attendant'],
                        attendances['excused'],
                        attendances['homework'],
                        attendances['performance'],
                        attendances['participation'],
                        attendances['memo'],
                        attendances['lid'],
                        attendances['sid']
                    )
            cursor.execute(sqlTemplate, valuelist)
            self._connection.commit()
        else:
            for i in range(0, len(attendances['sid'])):
                valuelist = (
                            attendances['attendant'][i],
                            attendances['excused'][i],
                            attendances['homework'][i],
                            attendances['performance'][i],
                            attendances['participation'][i],
                            attendances['memo'][i],
                            attendances['lid'][i],
                            attendances['sid'][i]
                        )
                cursor.execute(sqlTemplate, valuelist)
                self._connection.commit()
        return 0
    
    def newLesson(self, l):
        ''' inserts a new lesson and returns it's id, -1 for error '''
        cursor = self._connection.cursor()
        valuelist = (
                    l['date'],
                    l['cid'],
                    l['topic'],
                    l['count'],
                    l['memo'],
                    l['details']
                )
        sqlTemplate = '''INSERT INTO lessons 
                (date, cid, topic, count, memo, details) 
                VALUES (?, ?, ?, ?, ?, ?)'''
        cursor.execute(sqlTemplate, valuelist)
        self._connection.commit()
        sqlTemplate = '''SELECT id FROM lessons WHERE 
                date=? and cid=? and topic=? and count=? and memo=? and details=?'''
        cursor.execute(sqlTemplate, valuelist)
        result = cursor.fetchone()[0]
        self.newAttendances(result)
        # TODO: create attendances
        return result
    
    def getLesson(self, lid):
        ''' get a lesson from it's id '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM lessons WHERE id=?'''
        cursor.execute(sqlTemplate, (lid, ))
        tup = cursor.fetchone()
        if tup is None:
            return None
        result = {
                    'lid'       : tup[0],
                    'date'      : tup[1],
                    'cid'       : tup[2],
                    'topic'     : tup[3],
                    'count'     : tup[4],
                    'memo'      : tup[5],
                    'details'   : tup[6]
                }
        return result
    
    def updateLesson(self, l):
        ''' updates the db-entry for a lessoon, returning 0 or error-string '''
        cursor = self._connection.cursor()
        sqlTemplate = '''UPDATE lessons SET date=?, topic=?, count=?, memo=?, details=? WHERE id=?'''
        valuelist = (
                    l['date'],
                    l['topic'],
                    l['count'],
                    l['memo'],
                    l['details'],
                    l['lid']
                )
        try:
            cursor.execute(sqlTemplate, valuelist)
        except sqlite3.OperationalError as err:
            args = list(err.args)
            return 'FAILED: SQL-Error: '+str(args)
        self._connection.commit()
        return 0
    
    def newMemo(self, m):
        ''' inserts a new memo and returns it's id, -1 for error '''
        cursor = self._connection.cursor()
        valuelist = (
                    m['date'],
                    m['prio'],
                    m['memo']
                )
        sqlTemplate = '''INSERT INTO memos 
                (date, prio, memo) 
                VALUES (?, ?, ?)'''
        cursor.execute(sqlTemplate, valuelist)
        self._connection.commit()
        sqlTemplate = '''SELECT id FROM memos WHERE 
                date=? and prio=? and memo=?'''
        cursor.execute(sqlTemplate, valuelist)
        result = cursor.fetchone()[0]
        return result
    
    def getMemo(self, mid):
        ''' get a memo from it's id '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM memos WHERE id=?'''
        cursor.execute(sqlTemplate, (mid, ))
        tup = cursor.fetchone()
        if tup is None:
            return None
        result = {
                    'mid'       : tup[0],
                    'date'      : tup[1],
                    'prio'      : tup[2],
                    'memo'      : tup[3]
                }
        return result
    
    def getMemos(self):
        ''' returns all memos '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM memos ORDER BY prio, date'''
        cursor.execute(sqlTemplate)
        memos = cursor.fetchall()
        result = []
        if memos is None:
            return result
        for memo in memos:
            a = {
                        'mid'       : memo[0],
                        'date'      : memo[1],
                        'prio'      : memo[2],
                        'memo'      : memo[3]
                }
            result.append(a)
        return result
    
    def updateMemo(self, m):
        ''' updates the db-entry for a memo, returning 0 or error-string '''
        cursor = self._connection.cursor()
        sqlTemplate = '''UPDATE memos SET date=?, prio=?, memo=? WHERE id=?'''
        valuelist = (
                    m['date'],
                    m['prio'],
                    m['memo'],
                    m['mid']
                )
        try:
            cursor.execute(sqlTemplate, valuelist)
        except sqlite3.OperationalError as err:
            args = list(err.args)
            return 'FAILED: SQL-Error: '+str(args)
        self._connection.commit()
        return 0
    
    def deleteMemo(self, mid):
        ''' deletes a memo, returning 0 or error-string '''
        cursor = self._connection.cursor()
        sqlTemplate = '''DELETE FROM memos WHERE id=?'''
        valuelist = (mid, )
        try:
            cursor.execute(sqlTemplate, valuelist)
        except sqlite3.OperationalError as err:
            args = list(err.args)
            return 'FAILED: SQL-Error: '+str(args)
        self._connection.commit()
        return 0
    
    def getTimetable(self):
        ''' get the timetable '''
        cursor = self._connection.cursor()
        sqlTemplate = '''SELECT * FROM timetable '''
        cursor.execute(sqlTemplate)
        timetable = cursor.fetchall()
        if timetable is None:
            return None
        result = []
        for h in timetable:
            a = {
                        'no'    : h[0],
                        'time'  : h[1],
                        'mo'    : h[2],
                        'tu'    : h[3],
                        'we'    : h[4],
                        'th'    : h[5],
                        'fr'    : h[6],
                        'sa'    : h[7]
                    }
            result.append(a)
        return result
    
    def updateTimetable(self, timetable):
        ''' updates the timetable, returning 0 '''
        cursor = self._connection.cursor()
        sqlTemplate = '''DELETE FROM timetable'''
        cursor.execute(sqlTemplate)
        self._connection.commit()
        sqlTemplate = '''INSERT INTO timetable
                (no, time, mo, tu, we, th, fr, sa) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        if type(timetable['time']) is type(''):
            valuelist = (
                        1,
                        timetable['time'],
                        timetable['mo'],
                        timetable['tu'],
                        timetable['we'],
                        timetable['th'],
                        timetable['fr'],
                        timetable['sa']
                    )
            cursor.execute(sqlTemplate, valuelist)
            self._connection.commit()
            return 0
        for i in range(0, len(timetable['time'])):
            valuelist = (
                        i+1,
                        timetable['time'][i],
                        timetable['mo'][i],
                        timetable['tu'][i],
                        timetable['we'][i],
                        timetable['th'][i],
                        timetable['fr'][i],
                        timetable['sa'][i]
                    )
            cursor.execute(sqlTemplate, valuelist)
            self._connection.commit()
        return 0

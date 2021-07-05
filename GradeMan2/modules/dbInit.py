#!/usr/bin/python3
'''
Database-Init-file of TeXerBase - an Database Server for Exercises
'''

import sqlite3
import os, sys
import yaml

def checkTables(db):
    ''' makes sure default tables exist in the Database '''
    # students: givenname,familyname,gender,memo,img
    cursor = db._connection.cursor()
    sql_command = '''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER NOT NULL PRIMARY KEY,
            givenname VARCHAR(256) NOT NULL,
            familyname VARCHAR(256) NOT NULL,
            gender CHARACTER(20),
            memo TEXT,
            img BLOB
        );'''
    try:
        cursor.execute(sql_command)
    except sqlite3.OperationalError as err:
        args = list(err.args)
        args.append('Failed to create students table')
        err.args = tuple(args)
        raise
    # classes: name,subject,graduate,memo,seating
    cursor = db._connection.cursor()
    sql_command = '''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER NOT NULL PRIMARY KEY,
            name VARCHAR(256) NOT NULL,
            subject VARCHAR(256) NOT NULL,
            graduate BOOLEAN NOT NULL,
            memo TEXT,
            seating TEXT
        );'''
    try:
        cursor.execute(sql_command)
    except sqlite3.OperationalError as err:
        args = list(err.args)
        args.append('Failed to create classes table')
        err.args = tuple(args)
        raise
    # add colum for seating if not existing, TODO: remove this some day
    sql_command = '''
            ALTER TABLE classes ADD COLUMN seating TEXT;
        '''
    try:
        cursor.execute(sql_command)
    except sqlite3.OperationalError as err:
        print(str(err), file=sys.stderr) # obviously the column is existing already
    # studentclass: sid,cid
    cursor = db._connection.cursor()
    sql_command = '''
        CREATE TABLE IF NOT EXISTS studentclass (
            sid INTEGER NOT NULL,
            cid INTEGER NOT NULL,
            FOREIGN KEY (sid) REFERENCES students(id),
            FOREIGN KEY (cid) REFERENCES classes(id),
            PRIMARY KEY (sid, cid)
        );'''
    try:
        cursor.execute(sql_command)
    except sqlite3.OperationalError as err:
        args = list(err.args)
        args.append('Failed to create students table')
        err.args = tuple(args)
        raise
    # lessons: id,date,cid,topic,count,memo,details
    cursor = db._connection.cursor()
    sql_command = '''
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER NOT NULL PRIMARY KEY,
            date DATE NOT NULL,
            cid INTEGER NOT NULL,
            topic VARCHAR(255) NOT NULL,
            count CHARACTER(20) NOT NULL,
            memo TEXT,
            details TEXT,
            FOREIGN KEY (cid) REFERENCES classes(id)
        );'''
    try:
        cursor.execute(sql_command)
    except sqlite3.OperationalError as err:
        args = list(err.args)
        args.append('Failed to create students table')
        err.args = tuple(args)
        raise
    # attendance: lid,sid,attendant,excused,homework,performance,participation,memo
    cursor = db._connection.cursor()
    sql_command = '''
        CREATE TABLE IF NOT EXISTS attendances (
            lid INTEGER NOT NULL,
            sid INTEGER NOT NULL,
            attendant BOOLEAN,
            excused BOOLEAN,
            homework BOOLEAN,
            performance INTEGER,
            participation INTEGER,
            memo TEXT,
            FOREIGN KEY (lid) REFERENCES lessons(id),
            FOREIGN KEY (sid) REFERENCES students(id),
            PRIMARY KEY (lid, sid)
        );'''
    try:
        cursor.execute(sql_command)
    except sqlite3.OperationalError as err:
        args = list(err.args)
        args.append('Failed to create students table')
        err.args = tuple(args)
        raise
    # memos: id, date, prio, memo
    cursor = db._connection.cursor()
    sql_command = '''
        CREATE TABLE IF NOT EXISTS memos (
            id INTEGER NOT NULL PRIMARY KEY,
            date DATE NOT NULL,
            prio INTEGER,
            memo TEXT
        );'''
    try:
        cursor.execute(sql_command)
    except sqlite3.OperationalError as err:
        args = list(err.args)
        args.append('Failed to create memos table')
        err.args = tuple(args)
        raise
    # timetable: time,mo,tu,we,th,fr,sa
    cursor = db._connection.cursor()
    sql_command = '''
        CREATE TABLE IF NOT EXISTS timetable (
            no INTEGER NOT NULL PRIMARY KEY,
            time VARCHAR(255) NOT NULL,
            mo INTEGER,
            tu INTEGER,
            we INTEGER,
            th INTEGER,
            fr INTEGER,
            sa INTEGER,
            FOREIGN KEY (mo) REFERENCES classes(id),
            FOREIGN KEY (tu) REFERENCES classes(id),
            FOREIGN KEY (we) REFERENCES classes(id),
            FOREIGN KEY (th) REFERENCES classes(id),
            FOREIGN KEY (fr) REFERENCES classes(id),
            FOREIGN KEY (sa) REFERENCES classes(id)
        );'''
    try:
        cursor.execute(sql_command)
    except sqlite3.OperationalError as err:
        args = list(err.args)
        args.append('Failed to create timetable table')
        err.args = tuple(args)
        raise

#!/usr/bin/python3
'''
Database-IO-file of TeXerBase - an Database Server for Exercises
'''

import yaml, os, json
import hashlib, uuid

class settingsIo:
    def __init__(self, sfile):
        if not os.path.exists(sfile):
            s = {}
            s['dbfile'] = "grademan.sqlite3"
            #webServerPort = 8085
            s['host']='0.0.0.0'
            s['debug'] = True
            # extensions to be used by python-markdown:
            s['extensions']=['def_list', 'fenced_code', 'tables', 'admonition', 'nl2br', 'sane_lists', 'toc']
            with open(sfile, 'w') as file:
                yaml.dump(s, file)
        with open(sfile) as file:
            #self.s = yaml.full_load(file) #TODO: use this when available on all systems
            self.s = yaml.safe_load(file)
    
    def get(self, key):
        '''returns the value to a settings key'''
        if key=='dbfile':
            return self.s['dbfile']
        elif key=='host':
            return self.s['host']
        elif key=='debug':
            return self.s['debug']
        elif key=='extensions':
            return self.s['extensions']
        elif key=='dateHalfYear':
            return self.s['dateHalfYear']
        else:
            raise NameError('settings not found for '+str(key))
    
    def set(self, setnew, sfile):
        '''writes new settings to the settings-file'''
        # TODO: integrity-check
        if setnew['password']!= '':
            import hashlib, uuid
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(setnew['password'].encode('utf-8') + salt.encode('utf-8')).hexdigest()
            
            setnew['salt'] = salt
            setnew['password'] = hashed_password
        with open(sfile, 'w') as file:
            yaml.dump(setnew, file)
        with open(sfile) as file:
            #self.s = yaml.full_load(file) #TODO: use this when available on all systems
            self.s = yaml.safe_load(file)
    
    def getJson(self):
        '''returns settings as json-string'''
        return json.dumps(self.s)

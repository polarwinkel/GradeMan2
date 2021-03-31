#!/usr/bin/python3
'''
Database-IO-file of TeXerBase - an Database Server for Exercises
'''

import yaml, os, json

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
            self.s = yaml.full_load(file)
    
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
        else:
            raise NameError('settings not found for '+str(key))
    
    def getJson(self):
        '''returns settings as json-string'''
        return json.dumps(self.s)

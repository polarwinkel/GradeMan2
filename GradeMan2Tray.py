#!/usr/bin/python3
# -*- coding: utf-8 -*-
import wx.adv
import wx
import webbrowser
import subprocess
import os, sys
from waitress import serve
import multiprocessing as mp
import platform

sys.path.append(os.getcwd()+'/GradeMan2')
import app

version = '2.0.0'

TRAY_TOOLTIP = 'GradeMan2'
if platform.system()=='Linux':
    TRAY_ICON = 'static/favicon.svg'
else:
    TRAY_ICON = 'static/favicon.ico'

home = os.path.expanduser('~')
conffile = home+'/.GradeMan2conf.yaml'
port = 4202

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Start', self.on_start)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu
    
    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)
    
    def on_start(self, event):
        webbrowser.open('http://localhost:'+str(port))
    
    def on_left_down(self, event):
        print('This is GradeMan2 Taskbar server')
    
    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def runServer():
    serve(app.app, host='0.0.0.0', port=port)

def main():
    #p = os.popen('gunicorn3 app:app -w 1 -b localhost:'+str(port)+' -n GradeMan2')
    #p = subprocess.call(['gunicorn3', 'app:app', '-w 1', '-b localhost:'+str(port), '-n GradeMan2'])
    #p = subprocess.call(['waitress-serve', '--port='+str(port), 'app:app'])
    #serve(app.app, host='0.0.0.0', port=port)
    #p = subprocess.Popen(['python3', 'app.py'])
    server = mp.Process(target=runServer)
    server.start()
    tray = App(False)
    tray.MainLoop()
    server.terminate()

if __name__ == '__main__':
    mp.set_start_method('spawn') # Windows always spawns, never forks processes :-(
    os.chdir('GradeMan2')
    main()

#!/usr/bin/python3
# -*- coding: utf-8 -*-
import wx.adv
import wx
import webbrowser
import subprocess
import os
TRAY_TOOLTIP = 'GradeMan2'
TRAY_ICON = 'static/favicon.svg' 

os.chdir("GradeMan2")
port = 4202
home = os.path.expanduser('~')
conffile = home+'/.GradeMan2conf.yaml'

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

def main():
    server = App(False)
    #p = os.popen('gunicorn3 app:app -w 1 -b localhost:'+str(port)+' -n GradeMan2')
    #p = subprocess.call(['gunicorn3', 'app:app', '-w 1', '-b localhost:'+str(port), '-n GradeMan2'])
    p = subprocess.call(['waitress-serve', '--port='+str(port), 'app:app'])
    #p = subprocess.Popen(['python3', 'app.py'])
    server.MainLoop()

if __name__ == '__main__':
    main()

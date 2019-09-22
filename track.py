##import threading
##import timetracker
import tkinter as tk
import win32gui
import psutil, win32process
import os
import matplotlib.pyplot as plotter
from pathlib import Path
import json
import configparser as cp
import logging

class TrackTime:

    def __init__(self):
        config = cp.ConfigParser()
        config.read('conf.ini')
        DEF = config['DEFAULT']
        self.titles = DEF['titles'].split(',')
        self.ignore_processes = DEF['ignore'].split(',')
        
        self.root = tk.Tk('TimeTracker')
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.start_btn = tk.Button(self.frame, text="START",
                                   command=lambda:self.start_recording())
        self.start_btn.pack(side='left')
        self.stop_btn = tk.Button(self.frame, text='STOP',
                                  command=lambda:self.stop_recording())
        self.report_btn = tk.Button(self.frame, text='Report',
                                    command=lambda:self.create_report())
        self.report_btn.pack(side='right')
        self.root.mainloop()

    
    def active_window_process_name(self):
        fore_win_id = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(fore_win_id) #This produces a list of PIDs active window relates to
        try:
            app_name = psutil.Process(pid[-1]).name().split('.exe')[0].title()
            print(f'App name: {app_name}')
            if app_name in self.titles:
                return app_name
        except psutil._exceptions.NoSuchProcess:
            logging.warning(psutil._exceptions.NoSuchProcess)
        window_title = win32gui.GetWindowText(fore_win_id)
        logging.warning(f'Window title {window_title}')
        try:
            window_title = ' '.join(window_title.split()[0:2])
        except IndexError:
            pass
        return window_title

    def get_data_dict(self):
        self.DataPath = Path('Data')
##        if 'ProgramData' not in os.listdir():
        if not self.DataPath.exists() or (
        Path('data.json') not in self.DataPath.iterdir()): 
            self.DataPath.mkdir(exist_ok=True)
            return {}
##        if 'data.bak' not in os.listdir('ProgramData')
        
        with open('data.json') as file:
            return json.load(file)

    def start_recording(self):
        self.data_dict = self.get_data_dict()
        print('Recording')
        self.stop_btn.pack(side='left')
        self.start_btn['state']='disabled'
        self.stop_btn['state']='normal'
        self.recording=True
        self.record(None, 0)

    def stop_recording(self):
        self.recording=False
        self.start_btn['state']='normal'
        self.stop_btn['state']='disabled'
        self.save_data()

    def add(self, name, time):
        
        if name in self.data_dict:
            t = int(self.data_dict[name])
            t+=time
            self.data_dict[name]=t
        else:
            self.data_dict[name]=time

    def record(self, currentApp, totalTime):
        
        if self.recording:
            newApp = self.active_window_process_name()
            print(newApp)
            if newApp==currentApp:
                totalTime+=1
                print(f'In if: {totalTime}')
            else:
                self.add(currentApp, totalTime)
                currentApp=newApp
                logging.warning(f'Current app: {currentApp}')
                totalTime=0
                totalTime+=1
                print(f'In else: {totalTime}')

        self.root.after(1000, self.record, currentApp, totalTime)

    def save_data(self):
        data = json.dumps(self.data_dict)
        print(data)
        with open('data.json','w+') as file:
            file.write(data)

    def create_report(self):
        del self.data_dict[None]
        for process in self.ignore_processes:
            if process in self.data_dict.keys():
                del self.data_dict[process]
        labels = list(self.data_dict.keys())
        val = list(self.data_dict.values())
        print(labels)
        print(val)
        plotter.pie(val, labels=labels, autopct='%1.2f', startangle=90)
        plotter.legend()
        plotter.show()

    

try:
    tracker = TrackTime()
except Exception as e:
    print(e)
    

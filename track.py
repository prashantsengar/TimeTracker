import tkinter as tk
import win32gui
import psutil 
import win32process
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as fcta
import matplotlib.pyplot as plt
from pathlib import Path
import json
import configparser as cp
import logging
from datetime import date
import sqlite3
db=sqlite3.connect('mydb')
class TrackTime:
    

    def __init__(self):
        config = cp.ConfigParser()
        config.read('conf.ini')
        DEF = config['DEFAULT']
        self.titles = DEF['titles'].split(',')
        self.ignore_processes = DEF['ignore'].split(',')        
        self.root = tk.Tk()
        self.root.title('TimeTracker')
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
        self.report_btn2 = tk.Button(self.frame, text='Week Report',
                                    command=lambda:self.week_report())
        self.report_btn2.pack(side='right')
        self.report_btn1 = tk.Button(self.frame, text=' Month Report',
                                    command=lambda:self.month_report())
        self.report_btn1.pack(side='right')
        self.root.mainloop()

    
    def active_window_process_name(self):
        fore_win_id = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(fore_win_id) #This produces a list of PIDs active window relates to
        try:
            app_name = psutil.Process(pid[-1]).name().split('.exe')[0].title()
            logging.warning(f'App name: {app_name}')
            if app_name in self.titles:
                return app_name
        except psutil.NoSuchProcess:
            logging.warning(psutil.NoSuchProcess)
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
        logging.warning('Recording')
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
        self.save_datanew()

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
            logging.warning(newApp)
            if newApp==currentApp:
                totalTime+=1
                logging.warning(f'In if: {totalTime}')
            else:
                self.add(currentApp, totalTime)
                currentApp=newApp
                logging.warning(f'Current app: {currentApp}')
                totalTime=0
                totalTime+=1
                logging.warning(f'In else: {totalTime}')

            self.root.after(1000, self.record, currentApp, totalTime)

    def save_data(self):
        data = json.dumps(self.data_dict)
        logging.warning(data)
        with open('data.json','w+') as file:
            file.write(data)

    
    def create_report(self):
        print(self.data_dict)
        del self.data_dict[None]
        for process in self.ignore_processes:
            if process in self.data_dict.keys():
                del self.data_dict[process]
        labels = list(self.data_dict.keys())
        val = list(self.data_dict.values())
        logging.warning(labels)
        logging.warning(val)
        try:#To clear any previous figure (overwrite)
            self.widget.destroy()
            logging.warning('Cleared previous figure')            
        except Exception as e:#if no figure initially(self.widget isn't defined yet)
            logging.warning(e)
        self.figure = plt.Figure()
        subplot = self.figure.add_subplot()
        subplot.title.set_text("Report:")
        subplot.pie(val,labels=labels,autopct='%1.2f',startangle=90)
        piechart = fcta(self.figure, self.root) 
        self.widget=piechart.get_tk_widget()
        self.widget.pack(side='left',fill='both')
        
    def save_datanew(self):
        cursor=db.cursor()
        try:
            cursor.execute('''create table info(date date,name text,time int)''')# This table is already created
        except:
            pass
        cursor.execute('''select date from info''')
        print('The dictionary is',self.data_dict)
        alldates=cursor.fetchall()
        today_date=date.today()
        if today_date in alldates:
            cursor.execute('''select name from info where date=?''',(today_date))
            names=cursor.fetchall()
            #self.data_dict = self.get_data_dict()
            for process , time in self.data_dict.items():
                if process in names:
                    cursor.execute('''select time from info where date=? and name=?''',(today_date,process))
                    t=cursor.fetchone()
                    t+=time
                    cursor.execute('''UPDATE info SET time=? WHERE date=? and name=?''',(today_date,process))
                    db.commit()
        else:
            #self.data_dict = self.get_data_dict()
            for process , time in self.data_dict.items():
                 cursor.execute('''insert into info(date,name,time) values(?,?,?)''',(today_date,process,time))
                 db.commit()
        
    def month_report(self):
        cursor=db.cursor()
        today_month=date.today().strftime("%m")
        today_year=date.today().strftime("%Y")
        cursor.execute('''select name,time from info where strftime('%m',date)=? and strftime('%Y',date)=?''',(today_month,today_year))
        dataplot=cursor.fetchall()
        dataplot=dataplot[1:]
        labels=[]
        val=[]
        for i in dataplot:
            for j,k in dataplot:
              if j is not None:
                if j not in labels:
                    labels.append(j)
                    val.append(k)
                else:
                    i=labels.index(j)
                    val[i]+=k
        logging.warning(labels)
        logging.warning(val)
        try:#To clear any previous figure (overwrite)
            self.widget.destroy()
            logging.warning('Cleared previous figure')            
        except Exception as e:#if no figure initially(self.widget isn't defined yet)
            logging.warning(e)
        self.figure = plt.Figure()
        subplot = self.figure.add_subplot()
        subplot.title.set_text("Month Report:")
        subplot.pie(val,labels=labels,autopct='%1.2f',startangle=90)
        piechart = fcta(self.figure, self.root)
        self.widget=piechart.get_tk_widget()
        self.widget.pack(side='left',fill='both')
    def week_report(self):
        cursor=db.cursor()
        cursor.execute('''select name,time from info where date between date('now','weekday 1', '-21 days') and date('now')''')
        dataplot=cursor.fetchall()
        dataplot=dataplot[1:]
        labels=[]
        val=[]
        for i in dataplot:
            for j,k in dataplot:
              if j is not None:
                if j not in labels and k!=0:
                    labels.append(j)
                    val.append(k)
                else:
                    i=labels.index(j)
                    val[i]+=k
        logging.warning(labels)
        logging.warning(val)
        try:#To clear any previous figure (overwrite)
            self.widget.destroy()
            logging.warning('Cleared previous figure')            
        except Exception as e:#if no figure initially(self.widget isn't defined yet)
            logging.warning(e)
        self.figure = plt.Figure()
        subplot = self.figure.add_subplot()
        subplot.title.set_text("Week Report:")
        subplot.pie(val,labels=labels,autopct='%1.2f',startangle=90)
        piechart = fcta(self.figure, self.root)
        self.widget=piechart.get_tk_widget()
        self.widget.pack(side='left',fill='both')
try:
    tracker = TrackTime()
except Exception as e:
    logging.warning(e)

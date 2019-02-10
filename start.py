import threading
import timetracker
import tkinter as tk
import win32gui
import matplotlib.pyplot as plotter
root = tk.Tk()

_count=0
currentApp=''

    
def createReport():
    
    labels = list(timetracker.dic.keys())
    val = list(timetracker.dic.values())
    print(labels)
    print(val)
    plotter.pie(val, labels=labels, autopct='%1.2f', startangle=90)
    plotter.legend()
    plotter.show()
    
    

def startRecording():
    #global recording
    #currentApp=''
    global _count
    global currentApp


       
    #while True:
    if timetracker.recording:
        newApp = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        print(newApp)
        if newApp==currentApp:
            
            _count+=3
            print(f'In if: {_count}')
        else:
            timetracker.add(currentApp, _count)
            currentApp=newApp
            _count=0
            
            _count+=3
            print(f'In else: {_count}')

    root.after(1000, startRecording)

def startEv(btn):
    
    stop.pack(side='left')
    startRecording()
    #timetracker.startRecording()

frame = tk.Frame(root)
frame.pack()

start = tk.Button(frame, text="START", command=lambda:startEv(start))
start.pack(side='left')
stop = tk.Button(frame, text='STOP', command=lambda:timetracker.stop())
report = tk.Button(frame, text='Report', command=lambda:createReport())
report.pack(side='right')


root.mainloop()

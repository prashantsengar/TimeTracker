import timetracker
import tkinter as tk
root = tk.Tk()

def startEv(btn):
    newWin = tk.Tk()
    fr = tk.Frame(newWin)
    fr.pack()
    stop = tk.Button(fr, text='STOP', command=lambda:timetracker.save())
    stop.pack(side='left')
    timetracker.startRecording()

frame = tk.Frame(root)
frame.pack()

start = tk.Button(frame, text="START", command=lambda:startEv(start))
start.pack(side='left')

root.mainloop()

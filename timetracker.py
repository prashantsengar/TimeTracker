import win32gui
import json
import time
import atexit

dic= {}

def save():
    data = json.dumps(dic)
    file = open('data.json','w+')
    file.write(data)



def add(name, time):
    print(f"In add, time is : {time}")
    if name in dic:
        t = int(dic[name])
        t+=time
        dic[name]=t
    else:
        dic[name]=time

def startRecording():
    currentApp=''


    _count=0    
    while True:
        newApp = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        print(newApp)
        if newApp==currentApp:
            for i in range(3):
                time.sleep(1)
            _count+=3
            print(f'In if: {_count}')
        else:
            add(currentApp, _count)
            currentApp=newApp
            _count=0
            for i in range(3):
                time.sleep(1)
            _count+=3
            print(f'In else: {_count}')
            

if __name__=='__main__':
    
    atexit.register(save)
    try:
        print("Started recording")
        startRecording()
    except KeyboardInterrupt:
        save()
    finally:
        save()

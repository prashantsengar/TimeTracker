import win32gui
import json
import time
import atexit

dic= {}

recording=True

def stop():
    global recording
    recording=False
    save()

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


            

if __name__=='__main__':
    
    atexit.register(save)
    try:
        print("Started recording")
        startRecording()
    except KeyboardInterrupt:
        save()
    finally:
        save()

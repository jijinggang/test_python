#pip install -U pure-python-adb
import sys
from ppadb.client import Client as AdbClient
from ppadb.device import Device as AdbDevice



def connect() -> AdbDevice:
# Default is "127.0.0.1" and 5037
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    if(len(devices) != 1):
        print("No device or more than one device attached,num is ", len(devices))
        return
    device = client.device(devices[0].serial)
    if(device == None):
        print("No device attached")
    else:
        print("connect ",device.serial)
    return device

def install(file):
    device = connect()
    if device is None:
        return
    device.install(file)
    print("install ",file)    
def uninstall(bundleid):
    device = connect()
    if device is None:
        return
    print("uninstall ",bundleid)
    device.uninstall(bundleid)
def start(bundleid_activitiy):
    device = connect()
    if device is None:
        return
    print("start ",bundleid_activitiy)
    device.shell("am start -n " + bundleid_activitiy) 

def move(x,y):
    device = connect()
    if device is None:
        return
    print("press ",x,y)
    #device.input_tap(x,y)
     
    #device.input_swipe(300,300,800,800,100)
    device.input_swipe(800,800,300,300,100)
    #device.input_keyevent("a")
        
if __name__ == '__main__':
    match sys.argv[1:]:
        case ['install',file]:
            install(file)
        case ['uninstall', bundleid]:
            uninstall(bundleid)
        case ['start', bundleid]:
            start(bundleid)
        case ['move', x, y]:
            move(x,y)
        case _:
            print("Usage: python adb.py install|start|uninstall",sys.argv)
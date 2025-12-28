import ctypes
import threading
from time import sleep

wiimoteLib = None
isRunning = True # this should be faster than casting isTracking and will be false after tracking protocol terminates
isTracking = ctypes.c_byte(False) # only needed at startup, not too worried about casting with how rarely this is accessed in practice
accelData = None

def IsRunning():
    return isRunning

def IsCurrentlyTracking():
    return isTracking.value

def GetAccel():
    return accelData

def GetButtonID(name):
    match name.lower():
        case "two":
            return ctypes.c_uint16(0x0001)
        case "one":
            return ctypes.c_uint16(0x0002)
        case "dpadleft":
            return ctypes.c_uint16(256)
        case "b":
            return ctypes.c_uint16(0x0004)
        case _:
            raise Exception("Attempted to grab non-existent button ID")

class Event(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("eventInfo", ctypes.c_ubyte)
    ]

def BeginTrackingProtocol():
    wiimoteLib.AttemptTracking(ctypes.byref(isTracking)) # should release the global interpreter
    
    global isRunning
    isRunning = False

def InitLib():
    global wiimoteLib

    wiimoteLib = ctypes.CDLL("./Wiimote.dll")

    wiimoteLib.InitEventSystem()
    wiimoteLib.ReadBottomEventSafe.restype = Event

    global accelData
    accelData = (ctypes.c_float * 3).in_dll(wiimoteLib, "wiimoteAccel") # there is no need to keep track of the type after this
    
    return wiimoteLib

def AttemptTracking():
    trackingThread = threading.Thread(target=BeginTrackingProtocol)
    trackingThread.start()

    while trackingThread.is_alive() and not isTracking.value:
        sleep(0.5) # waiting for handshake
    

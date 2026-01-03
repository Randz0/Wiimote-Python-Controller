import ctypes
import threading
from time import sleep

wiimoteLib = None
isRunning = True # this should be faster than casting isTracking and will be false after tracking protocol terminates
isTracking = ctypes.c_byte(False) # only needed at startup, not too worried about casting with how rarely this is accessed in practice
motionOutputs = {}

def IsRunning():
    return isRunning

def IsCurrentlyTracking():
    return isTracking.value

def GetConnectedWiimotes():
    return ctypes.c_int.in_dll(wiimoteLib, "connected").value # type: ignore

def GetButtonID(name):
    match name.lower():
        case "two":
            return ctypes.c_uint16(0x0001)
        case "one":
            return ctypes.c_uint16(0x0002)
        case "dpadleft":
            return ctypes.c_uint16(0x0100)
        case "dpadup":
            return ctypes.c_uint16(0x0800)
        case "dpadright":
            return ctypes.c_uint16(0x0200)
        case "dpaddown":
            return ctypes.c_uint16(0x0800)
        case "plus":
            return ctypes.c_uint16(0x1000)
        case "b":
            return ctypes.c_uint16(0x0004)
        case _:
            raise Exception("Attempted to grab non-existent button ID")

class Event(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("eventInfo", ctypes.c_ubyte),
        ("controllerID", ctypes.c_ubyte)
    ]

class WiimoteOutput(ctypes.Structure):
    _fields_ = [
        ("acceleration", ctypes.c_float * 3),
        ("irPosNormalized", ctypes.c_float * 2)
    ]

# Do not directly call this. AttemptTracking() will do this on a seperate thread which will actually make it work
def BeginTrackingProtocol():
    wiimoteLib.AttemptTracking(ctypes.byref(isTracking)) # type: ignore # should release the global interpreter
    
    print("stop tracking")

    global isRunning
    isRunning = False

def InitLib():
    global wiimoteLib

    wiimoteLib = ctypes.CDLL("./Wiimote.dll")

    wiimoteLib.ReadBottomEventSafe.restype = Event
    
    return wiimoteLib

def AttemptTracking():
    trackingThread = threading.Thread(target=BeginTrackingProtocol)
    trackingThread.start()

    while trackingThread.is_alive() and not isTracking.value:
        sleep(0.5) # polling for a few seconds

    #initializing some variables before returning control back to the user

    connected = ctypes.c_int.in_dll(wiimoteLib, "connected") # type: ignore

    motionOutputsType = WiimoteOutput * connected.value
    motionOutputsRaw = motionOutputsType.in_dll(wiimoteLib, "motionOutputs") # type: ignore
    # grab the connected wiimote outputs

    for i in range(connected.value):
        motionOutputs[i] = motionOutputsRaw[i]
    

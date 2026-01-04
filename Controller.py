from math import atan2, pi
import vgamepad
import ctypes
from time import sleep

from WiimoteBackend import *

def WakeUpGamepad(gamepad: vgamepad.VDS4Gamepad):
    gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
    gamepad.update()

    sleep(0.05) # giving time for it to register

    gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
    gamepad.update()

    sleep(0.05) 

def InitGamepads():
    connected = GetConnectedWiimotes()

    for i in range(connected):
        gamepads[i] = vgamepad.VDS4Gamepad()
        WakeUpGamepad(gamepads[i])

def PressButton(buttID, gamepad: vgamepad.VDS4Gamepad):
    match buttID:
        case _: # this is filler code; replace with your own button mappings
            pass

def ReleaseButton(buttID, controllerID):
    match buttID:
        case _:
            pass

def HandleEvents():
    global bottomEvent

    while bottomEvent.type != 0:
        if bottomEvent.type == 1:
            PressButton(bottomEvent.eventInfo, gamepads[bottomEvent.controllerID])
        elif bottomEvent.type == 2:
            ReleaseButton(bottomEvent.eventInfo, gamepads[bottomEvent.controllerID])

        wiimoteLib.PopBottomEventSafe()
        bottomEvent = wiimoteLib.ReadBottomEventSafe()

def OnWiimoteStartTracking():
    global bottomEvent

    while IsRunning():
        bottomEvent = wiimoteLib.ReadBottomEventSafe()

        if bottomEvent.type != 0:
            HandleEvents()

        for i in range(len(gamepads)):
            gamepads[i].update()

        sleep(0.0166) # 60hz polling rate

gamepads = {}
wiimoteLib = InitLib()

AttemptTracking()

if IsCurrentlyTracking():
    InitGamepads()
    
    wiimoteLib.SetAccelTracking(ctypes.byref(ctypes.c_char(1)))
    OnWiimoteStartTracking()
else:
    print("Failed to track wiimote")
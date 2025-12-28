from math import atan2, pi
import vgamepad
import ctypes
from time import sleep

from WiimoteBackend import *

def WakeUpGamepad(gamepad: vgamepad.VDS4Gamepad):
    gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
    gamepad.update()

    sleep(0.1) # giving time for it to register

    gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
    gamepad.update()

    sleep(0.1) 

def PressButton(buttID):
    match buttID:
        case _: # this is filler code; replace with your own button mappings
            pass

def ReleaseButton(buttID):
    match buttID:
        case _:
            pass

def HandleEvents():
    global bottomEvent

    while bottomEvent.type != 0:
        if bottomEvent.type == 1:
            PressButton(bottomEvent.eventInfo)
        elif bottomEvent.type == 2:
            ReleaseButton(bottomEvent.eventInfo)

        wiimoteLib.PopBottomEventSafe()
        bottomEvent = wiimoteLib.ReadBottomEventSafe()

def OnWiimoteStartTracking():
    global bottomEvent

    while IsRunning():
        bottomEvent = wiimoteLib.ReadBottomEventSafe()

        if bottomEvent.type != 0:
            HandleEvents()
        
        gamepad.update()
        sleep(0.0166) # 60hz polling rate

gamepad = vgamepad.VDS4Gamepad()
wiimoteLib = InitLib()

AttemptTracking()

if IsCurrentlyTracking():
    WakeUpGamepad(gamepad)

    OnWiimoteStartTracking()
else:
    print("Failed to track wiimote")
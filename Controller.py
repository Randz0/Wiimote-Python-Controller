from math import atan2, pi
import vgamepad
import ctypes
from time import sleep

from WiimoteBackend import *

maxAngle = 40 * (pi / 180) # 40 deg in rad

def MapToNormalRot(angle):
    while angle < 0:
        angle += 2 * pi

    return pi - angle

def WakeUpGamepad(gamepad: vgamepad.VDS4Gamepad):
    gamepad.press_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
    gamepad.update()

    sleep(0.1) # giving time for it to register

    gamepad.release_button(button=vgamepad.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
    gamepad.update()

    sleep(0.1) 

def PressButton(buttID):
    match buttID:
        case 1: # 2
            gamepad.press_button(vgamepad.DS4_BUTTONS.DS4_BUTTON_TRIGGER_LEFT)
        case 0: # 1
            gamepad.press_button(vgamepad.DS4_BUTTONS.DS4_BUTTON_TRIGGER_RIGHT)
        case 2: # b
            gamepad.press_button(vgamepad.DS4_BUTTONS.DS4_BUTTON_CROSS)
        case 6: # left
            gamepad.press_button(vgamepad.DS4_BUTTONS.DS4_BUTTON_SQUARE)

def ReleaseButton(buttID):
    match buttID:
        case 1: # 2
            gamepad.release_button(vgamepad.DS4_BUTTONS.DS4_BUTTON_TRIGGER_LEFT)
        case 0: # 1
            gamepad.release_button(vgamepad.DS4_BUTTONS.DS4_BUTTON_TRIGGER_RIGHT)
        case 2: # b
            gamepad.release_button(vgamepad.DS4_BUTTONS.DS4_BUTTON_CROSS)
        case 6: # left
            gamepad.release_button(vgamepad.DS4_BUTTONS.DS4_BUTTON_SQUARE)

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
    
    angle = 0
    stickVal = 0

    while IsRunning():
        bottomEvent = wiimoteLib.ReadBottomEventSafe()

        if bottomEvent.type != 0:
            HandleEvents()

        angle = MapToNormalRot(atan2(accelData[1], accelData[0]))

        stickVal = max(min(-angle / maxAngle, 1), -1)
        gamepad.left_joystick_float(stickVal, 0)
        
        gamepad.update()
        sleep(0.0166) # 60hz polling rate

gamepad = vgamepad.VDS4Gamepad()
wiimoteLib = InitLib()

AttemptTracking()

if IsCurrentlyTracking():
    accelData = GetAccel()

    wiimoteLib.ListenButtonSafe(GetButtonID("two"))
    wiimoteLib.ListenButtonSafe(GetButtonID("one"))
    wiimoteLib.ListenButtonSafe(GetButtonID("b"))
    wiimoteLib.ListenButtonSafe(GetButtonID("dpadleft"))
    
    wiimoteLib.SetAccelTracking(ctypes.c_char(1))
    #wiimoteLib.SetIRTracking(ctypes.c_char(0)) # disable IR
    
    WakeUpGamepad(gamepad)

    OnWiimoteStartTracking()
else:
    print("Failed to track wiimote")
All of the visual studio dlls are here because the people behind wiiuse are very smart and made it so I had to compile with visual studios (as far as im lazy enough to do so).

these should be accessible via Environment paths but just for the sake of inclusivity i put them here as well




[Extra code that is unused]

noJerkBuffer = 5 # 5 frames not jerking
jerkBufffer = 3 # 3 frames of jerking

jerkThreshold = 10

framesNotJerking = 5 # stores how many not jerking
framesJerking = 3 # stores how many jerking

lastFrameAccel = [0,0,0]

def UpdateJerkCounter():
    jerkMag = (accelData[0] - lastFrameAccel[0]) ** 2 + (accelData[1] - lastFrameAccel[1]) ** 2 + (accelData[2] - lastFrameAccel[2]) ** 2 / 0.016

    global framesNotJerking
    global framesJerking

    if jerkMag < jerkThreshold:
        framesNotJerking += 1
        framesJerking = min(4, max(0, framesJerking * 0.9))
    else:
        framesNotJerking = 0
        framesJerking += 2

    lastFrameAccel[0] = accelData[0]
    lastFrameAccel[1] = accelData[1]
    lastFrameAccel[2] = accelData[2]

in main loop

UpdateJerkCounter()

        if framesNotJerking < noJerkBuffer and framesJerking > jerkBufffer:
            gamepad.press_button(vgamepad.DS4_BUTTONS.DS4_BUTTON_CROSS)
        elif framesJerking < jerkBufffer and framesNotJerking > noJerkBuffer:
            gamepad.release_button(vgamepad.DS4_BUTTONS.DS4_BUTTON_CROSS)    
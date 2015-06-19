from __future__ import division
import numpy as np
from psychopy import visual, core
import display
import math
import TobiiControllerP


def calibrate(numpts, outfile): # creates and returns a calibrated tobii controller
    errcode = 0  # error code to be set to 1 if calibration fails
    testWin = visual.Window(
        size=(640, 400), monitor="testMonitor", units="pix")

    # CONNECT TO EYE TRACKER
    tobii_cont = TobiiControllerP.TobiiController(testWin)

    tobii_cont.waitForFindEyeTracker()
    tobii_cont.activate(tobii_cont.eyetrackers.keys()[0])

    # set all possible calibration points
    pos = np.array([(0.1, 0.1),
                    (0.5, 0.1),
                    (0.9, 0.1),
                    (0.1, 0.5),
                    (0.5, 0.5),
                    (0.9, 0.5),
                    (0.1, 0.9),
                    (0.5, 0.9),
                    (0.9, 0.9)])

    # define which points to use based on numpts
    if numpts == 1 or numpts == 2 or numpts == 3:
        print "Warning! Calibrating with fewer than four points may result in poor calibration!"
    elif numpts == 4:
        idx = [0, 2, 6, 8]  # corners
    elif numpts == 5:
        idx = [0, 2, 4, 6, 8]  # corners + center
    elif numps == 6:
        idx = [0, 1, 2, 6, 7, 8]  # top and bottom rows
    else:
        idx = np.random.randint(0, 10, numpts)

    np.random.shuffle(idx)  # shuffles points to be in a random order
    pos = pos[idx]  # set pos to only contain the points needed

    display.countdown(testWin, 4)  # countdown from 4

    while True:
        ret = tobii_cont.doCalibration(pos)
        if ret == 'accept':
            break
        elif ret == 'abort':
            tobii_cont.destroy()
            return
    # ***Check format of this and figure out how to save into the outfile provided
    tobii_cont.eyetracker.GetCalibration()
    return tobii_cont

    # # ----old code replaced by TobiiControllerP code-----
    # # Start Calibration
    # totTime = 2  # total display time for point during calibration
    # calibdone = 0

    # # while not calibdone:
    # #     # START EYE TRACKER CALIBRATION

    #     core.wait(0.5)

    #     # loop over calibration points
    #     for i in range(numpts):
    #         position = pos[i]
    #         when0 = core.getTime()
    #         point(testWin, totTime, position)
    #         # ADD CALIBRATION POINT

    #     # blank screen
    #     display.fill_screen(testWin, (0, 0, 0))

    #     core.wait(1)  # give tobii time to catch up

    #     # TRY TO COMPUTE CALIBRATION
    #     # CHECK QUALITY OF THE CALIBRATION
    #     # ASK IF CALIBRATION WAS GOOD
    #     calibdone = 1
    # SAVE DATA


def point(win, totTime, position):
    circle = visual.Circle(
        win, radius=0, units='norm', pos=position, fillColor=[1, -1, -1], lineColor=None)
    cross = visual.TextStim(win, text='+',
                            font='Helvetica', alignHoriz='center', alignVert='center', units='norm',
                            pos=position, height=0.1, color=[255, 255, 255], colorSpace='rgb255',
                            wrapWidth=2)
    for i in range(100):
        circle.radius = 0.1 * math.sin(i * 2 * math.pi / 100)
        circle.draw()
        cross.draw()
        win.flip()


if __name__ == '__main__':
    calibrate(4, None)

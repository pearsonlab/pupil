from __future__ import division
import numpy as np
from psychopy import visual, core, gui
import display
import math
import cPickle as pickle
TESTSCREEN = 1
EXPERIMENTSCREEN = 0

def calibSettings():
    settingsDlg = gui.Dlg(title="Calibration")
    settingsDlg.addText('Set Parameters')
    settingsDlg.addField('Number of Calibration Points (4-9)', 5)
    settingsDlg.show()  # show dialog and wait for OK or Cancel
    if settingsDlg.OK:
        response = settingsDlg.data
        return response[0]
    else:
        return -1

def calibrate(controller, outfile): # creates and returns a calibrated tobii controller
    testWin = controller.testWin
    numpts = calibSettings()
    if numpts == -1:
        print "Calibration Cancelled"
        return
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

    while True:
        ret = controller.tobii_cont.doCalibration(pos)
        if ret == 'accept':
            break
        elif ret == 'abort':
            return
    # saves calibration into pickle file that can be loaded
    calib_object = controller.tobii_cont.eyetracker.GetCalibration()
    pickle.dump(calib_object, outfile)
    testWin.flip()
    # marks calibration as complete and opens up other actions
    controller.calib_complete = True
    controller.actions = controller.full_actions
    return

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
    tobii_cont = calibrate(4, None) # send in 'calibration.p' as outfile
    print "done"

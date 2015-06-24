import display
from psychopy import event
from psychopy import visual
import math
import time


def show_eyes(controller):
    running = True
    # start tracking
    controller.tobii_cont.startTracking()

    # set up figures to draw
    left_eye = visual.Circle(controller.experWin, radius=0.05, units='norm', colorSpace='rgb255')
    right_eye = visual.Circle(controller.experWin, radius=0.05, units='norm', colorSpace='rgb255')
    left_eye_test = visual.Circle(controller.testWin, radius=0.05, units='norm', colorSpace='rgb255')
    right_eye_test = visual.Circle(controller.testWin, radius=0.05, units='norm', colorSpace='rgb255')
    left_text = visual.TextStim(controller.experWin, height=0.1, pos=(-0.3,-0.4), units='norm')
    right_text = visual.TextStim(controller.experWin, height=0.1, pos=(0.3,-0.4), units='norm')
    press_text = visual.TextStim(controller.experWin, height=0.1, pos=(0,-0.3), text='Press any button to quit', units='norm')

    # run while key is not pressed
    while running:
        pressed = event.getKeys()
        if len(pressed) > 0:
            running = False  # stops running if a key is pressed

        # get pupil and validity information from Tobii
        curr_pupil = controller.tobii_cont.getCurrentPupilsandValidity()
        if curr_pupil == (None, None, None, None):
            continue
        left_pupil, left_validity, right_pupil, right_validity = curr_pupil

        # get gaze direction information from Tobii
        curr_gaze = controller.tobii_cont.getCurrentGazePosition()
        if curr_gaze == (None, None, None, None):
            continue
        left_x, left_y, right_x, right_y = curr_gaze

        # set colors based on validities
        if left_validity == 0:
            left_eye.color = [0, 255, 0]
            left_eye_test.color = [0, 255, 0]
        elif left_validity == 1:
            left_eye.color = [64, 192, 0]
            left_eye_test.color = [64, 192, 0]
        elif left_validity == 2:
            left_eye.color = [128, 128, 0]
            left_eye_test.color = [128, 128, 0]
        elif left_validity == 3:
            left_eye.color = [192, 64, 0]
            left_eye_test.color = [192, 64, 0]
        else:
            left_eye.color = [255, 0, 0]
            left_eye_test.color = [255, 0, 0]

        if right_validity == 0:
            right_eye.color = [0, 255, 0]
            right_eye_test.color = [0, 255, 0]
        elif right_validity == 1:
            right_eye.color = [64, 192, 0]
            right_eye_test.color = [64, 192, 0]
        elif right_validity == 2:
            right_eye.color = [128, 128, 0]
            right_eye_test.color = [128, 128, 0]
        elif right_validity == 3:
            right_eye.color = [192, 64, 0]
            right_eye_test.color = [192, 64, 0]
        else:
            right_eye.color = [255, 0, 0]
            right_eye_test.color = [255, 0, 0]

        # draw appropriate figures to visualize gaze on experimenter's screen
        if left_validity < 4:
            left_eye.pos = (left_x, left_y)
            left_eye_test.pos = (left_x, left_y)
            left_text.setText('Left Pupil Diameter: ' + str(left_pupil))
            left_eye.draw()
            left_eye_test.draw()
            left_text.draw()

        if right_validity < 4:
            right_eye.pos = (right_x, right_y)
            right_eye_test.pos = (right_x, right_y)
            right_text.setText('Right Pupil Diameter: ' + str(right_pupil))
            right_eye.draw()
            right_eye_test.draw()
            right_text.draw()

        # draw instruction
        press_text.draw()

        # update experimenter's and participant's screens
        controller.experWin.flip()
        controller.testWin.flip()
    # stop tracking
    controller.tobii_cont.stopTracking()

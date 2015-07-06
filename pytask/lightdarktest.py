'''
Code for light/dark test orginally coded in Matlab.
'''
from psychopy import visual, core
import numpy as np
import display

# mode = 0 (dark test) or 1 (light test), outfile is the file that data is
# saved to


def lightdarktest(controller, mode, outfile):
    # Create window to display test
    testWin = controller.testWin
    if mode == 0:  # dark test
        task = 'darktest'
        numtrials = 3  # number of light/dark cycles
        habit_mat = [1, 1, 1]  # set habituation to full brightness
        # set stimulus matrix to darkness
        stim_mat = np.negative(np.ones((numtrials, 3)))
        # back to full brightness for recovery
        rec_mat = np.ones((numtrials, 3))
        stim_time = 1  # duration of stimulus in seconds
        display.text(controller.experWin, 'Running Dark Test')
    elif mode == 1:  # light test
        task = 'lighttest'
        habit_mat = [-1, -1, -1]  # habituation is black
        stim_mat = [[-0.5, -0.5, -0.5],  # stimulus is increasing brightness each time
                    [0.00, 0.00, 0.00],
                    [0.50, 0.50, 0.50],
                    [1.00, 1.00, 1.00]]
        # set numtrials based on number of stimulus conditions
        numtrials = len(stim_mat)
        # recovery goes back to black
        rec_mat = np.negative(np.ones((numtrials, 3)))
        stim_time = 0.2  # length of stimulus time in seconds
        display.text(controller.experWin, 'Running Light Test')
    habit_dur = 10  # time for habituation
    # time for recovery between stimuli
    recover_dur = 8 * np.ones((1, numtrials))
    stim_dur = stim_time * np.ones((1, numtrials))  # duration of each stimulus
    display.countdown(controller)  # display countdown before task

    # habituation
    display.fill_screen(testWin, habit_mat)
    core.wait(habit_dur)

    # Start eye tracking
    if not controller.testing:
        controller.tobii_cont.setDataFile(outfile)
        controller.tobii_cont.startTracking()
        controller.tobii_cont.setEventsAndParams(['ontime', 'offtime', 'task'])
        controller.tobii_cont.setParam('task', task)

    for i in range(numtrials):
        core.wait(2.0)

        # display stimulus
        display.fill_screen(testWin, stim_mat[i])

        # record timestamp on tracker for start of stimulus
        if not controller.testing:
            controller.tobii_cont.recordEvent('ontime')

        # wait for stimulus
        core.wait(stim_dur[0][i])

        # display recovery
        display.fill_screen(testWin, rec_mat[i])

        # record timestamp on tracker for end of stimulus
        if not controller.testing:
            controller.tobii_cont.recordEvent('offtime')

        # wait for recovery
        core.wait(recover_dur[0][i])

    # End eye tracking
    if not controller.testing:
        controller.tobii_cont.stopTracking()
        controller.tobii_cont.closeDataFile()


if __name__ == '__main__':
    lightdarktest(0, None)

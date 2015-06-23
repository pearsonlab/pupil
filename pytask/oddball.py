import numpy as np
from psychopy import prefs
prefs.general['audioLib'] = ['pyo']
from psychopy import visual, core, sound, event, gui
import display
import os


def oddSettings(controller):
    vector_path = os.path.join(controller.settings_path, 'OddballVectors.csv')
    # checks if previous vector file exists
    if os.path.isfile(vector_path):
        generateDlg = gui.Dlg(title="Oddball")
        generateDlg.addField(
            'Load previous (0) or Generate (1) Oddball Vectors', 0)
        generateDlg.show()
        if generateDlg.OK:
            response = generateDlg.data[0]
            if response == 0:
                return np.genfromtxt(vector_path, delimiter=',')
        else:
            return [-999]

    settingsDlg = gui.Dlg(title="Oddball")
    settingsDlg.addText('Set Parameters')
    settingsDlg.addField('Number of Oddballs', 5)
    settingsDlg.addField('Minimum Between', 3)
    settingsDlg.addField('Maximum Between', 7)
    settingsDlg.show()  # show dialog and wait for OK or Cancel
    if settingsDlg.OK:
        response = settingsDlg.data
        return makeoddballs(
            vector_path, response[0], response[1], response[2], np.random.randint(1, 9999))
    else:
        return [-999]


def oddball(controller, outfile, flag, *args):
    trialvec = oddSettings(controller)
    if trialvec[0] == -999:
        return
    display.text(controller.experWin, 'Running Oddball')
    # set up window
    # Create window to display test
    testWin = controller.testWin
    # load sounds
    resource_path = '../task/'
    lowsnd = sound.Sound(resource_path + '500.wav')
    highsnd = sound.Sound(resource_path + '1000.wav')
    # parameters for task
    iti_mean = 3
    iti_range = 2
    # display instructions
    display.text_keypress(
        testWin, 'In this task, you will listen to some sounds. \n Press any key to continue')
    # play sound samples
    lowsnd.play()
    display.text_keypress(
        testWin, 'Some sounds are low... \n Press any key to continue')
    highsnd.play()
    display.text_keypress(
        testWin, '...and some are high. \n Press any key to continue')

    display.text_keypress(
        testWin, 'When you hear a sound, press the space bar.\n\nPress any key when ready.')
    display.countdown(testWin, 4)

    # START EYE TRACKING
    if not controller.testing:
        controller.tobii_cont.setDataFile(outfile)
        controller.tobii_cont.startTracking()

    core.wait(2.0)  # give small wait time before starting trial

    for isHigh in trialvec:
        if isHigh:
            if not controller.testing:
                # RECORD TIMESTAMP FOR SOUND PLAY
                controller.tobii_cont.recordEvent('Odd Sound')
            highsnd.play()  # play high sound if oddball
        else:
            if not controller.testing:
                # RECORD TIMESTAMP FOR SOUND PLAY
                controller.tobii_cont.recordEvent('Normal Sound')
            lowsnd.play()  # otherwise play low sound

        # wait for space bar
        keypress = event.waitKeys(keyList=['space', 'q'])
        if keypress[0] == 'q':
            break
        elif keypress[0] == 'space':
            if not controller.testing:
                # RECORD TIMESTAMP FOR KEY PRESS
                controller.tobii_cont.recordEvent('Key Press')

        iti = iti_mean + iti_range * (2 * np.random.random() - 1)

        core.wait(iti)

    # STOP EYE TRACKING AND SAVE DATA
    if not controller.testing:
        controller.tobii_cont.stopTracking()
        controller.tobii_cont.closeDataFile()


def makeoddballs(path, noddballs, minrun, maxrun, seed):
    # set the seed
    np.random.seed(seed)

    # run lengths (between min and max) surround each oddball
    lens = np.random.random_integers(minrun, maxrun, noddballs + 1)
    # calculate oddballs
    oddtrials = np.cumsum(lens)
    isodd = np.zeros((1, oddtrials[-1]))[0]
    isodd[oddtrials[:-1]] = 1
    np.savetxt(path, isodd, delimiter=",")
    return isodd

if __name__ == '__main__':
    # oddball(None,0,5,3,7)
    oddball(None, 1)

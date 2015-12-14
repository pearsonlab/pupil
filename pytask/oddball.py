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
            'Load existing (0) or Generate (1) Oddball Vectors', 0)
        generateDlg.show()
        if generateDlg.OK:
            response = generateDlg.data[0]
            if response == 0:
                return np.genfromtxt(vector_path, delimiter=',')
        else:
            return [-999]

    settingsDlg = gui.Dlg(title="Oddball")
    settingsDlg.addText('Set Parameters')
    settingsDlg.addField(
        'Number of Oddballs', controller.settings['Oddball: Count'])
    settingsDlg.addField(
        'Minimum Between', controller.settings['Oddball: Minimum Between'])
    settingsDlg.addField(
        'Maximum Between', controller.settings['Oddball: Maximum Between'])
    settingsDlg.show()  # show dialog and wait for OK or Cancel
    if settingsDlg.OK:
        response = settingsDlg.data
        return makeoddballs(
            vector_path, response[0], response[1], response[2], np.random.randint(1, 9999))
    else:
        return [-999]


def oddball(controller, outfile):
    trialvec = oddSettings(controller)
    if trialvec[0] == -999:
        return
    # set up window
    # Create window to display test
    testWin = controller.launchWindow()
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

    display.countdown(controller)

    # START EYE TRACKING
    if not controller.testing:
        controller.tobii_cont.setDataFile(outfile)
        controller.tobii_cont.startTracking()
        core.wait(0.5)  # make sure video starts before sync blip
        controller.tobii_cont.setEventsAndParams(
            ['task', 'soundtime', 'presstime', 'iti_mean', 'iti_range', 'trialvec', 'start_time'])
        controller.tobii_cont.setParam('task', 'oddball')
        controller.tobii_cont.setParam('iti_mean', iti_mean)
        controller.tobii_cont.setParam('iti_range', iti_range)
        controller.tobii_cont.setVector('trialvec', trialvec)
        controller.tobii_cont.setParam('start_time', core.getTime())

    display.sync_blip(controller.testWin)
    display.cross(controller.testWin)

    core.wait(2.0)  # give small wait time before starting trial

    for isHigh in trialvec:
        # RECORD TIMESTAMP FOR SOUND PLAY
        if not controller.testing:
            controller.tobii_cont.recordEvent('soundtime')
        if isHigh:
            highsnd.play()  # play high sound if oddball
        else:
            lowsnd.play()  # otherwise play low sound

        # wait for space bar
        keypress = event.waitKeys(keyList=['space', 'q'])
        if keypress[0] == 'q':
            break
        elif keypress[0] == 'space':
            if not controller.testing:
                # RECORD TIMESTAMP FOR KEY PRESS
                controller.tobii_cont.recordEvent('presstime')

        iti = iti_mean + iti_range * (2 * np.random.random() - 1)

        core.wait(iti)

    # STOP EYE TRACKING AND SAVE DATA
    if not controller.testing:
        controller.tobii_cont.stopTracking()
        display.text(testWin, 'Generating Figure...')
        image_file = os.path.join(
            controller.data_filepath, 'pupil_response.png')
        try:
            controller.tobii_cont.print_oddball_fig(image_file)
            display.image_keypress(testWin, image_file)
        except:
            display.text(testWin, 'Figure generation failed.')
        controller.tobii_cont.flushData()
    testWin.close()


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

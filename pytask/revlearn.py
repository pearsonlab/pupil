import numpy as np
from psychopy import prefs
prefs.general['audioLib'] = ['pyo']
from psychopy import visual, core, sound, event, gui
import display
import os


def revSettings(controller):
    vector_path = os.path.join(controller.settings_path, 'RevVectors.csv')
    # checks if previous vector file exists
    if os.path.isfile(vector_path):
        generateDlg = gui.Dlg(title="Reversal Learning")
        generateDlg.addField('Load previous (0) or Generate (1) Vectors', 0)
        generateDlg.show()
        if generateDlg.OK:
            response = generateDlg.data[0]
            if response == 0:
                return np.genfromtxt(vector_path, delimiter=',')
        else:
            return [-999]

    settingsDlg = gui.Dlg(title="Reversal Learning")
    settingsDlg.addText('Set Parameters')
    settingsDlg.addField(
        'Number of Switches', controller.settings['RevLearn: Number of Switches'])
    settingsDlg.addField(
        'Minimum Between', controller.settings['RevLearn: Minimum Between'])
    settingsDlg.addField(
        'Maximum Between', controller.settings['RevLearn: Maximum Between'])
    settingsDlg.show()  # show dialog and wait for OK or Cancel
    if settingsDlg.OK:
        response = settingsDlg.data
        return makeswitches(
            vector_path, response[0], response[1], response[2], np.random.randint(1, 9999))
    else:
        return [-999]


def revlearn(controller, outfile):
    trialvec = revSettings(controller)
    if trialvec[0] == -999:
        return
    # set up window
    # Create window to display test
    testWin = controller.launchWindow()

    # load sounds
    resource_path = '../task/'
    wrongsnd = sound.Sound(resource_path + 'buzz1.wav')
    rightsnd = sound.Sound(resource_path + 'dinga.wav')

    # parameters for task
    iti_mean = 3
    iti_range = 2

    # display instructions
    display.text_keypress(testWin,  ('Press the left or right key \n' +
                                     'when the cross appears onscreen.\n' +
                                     'You must learn by trial and error\n' +
                                     'which is correct. \n\n' +
                                     '(Press any key to continue)'))

    # sound samples
    rightsnd.play()
    display.text_keypress(
        testWin,  'You will hear this for correct responses. \n (Press any key to continue)')
    wrongsnd.play()
    display.text_keypress(
        testWin,  'And this for incorrect responses. \n (Press any key to continue)')
    display.text_keypress(
        testWin,  'Please make a choice as soon as the "+" appears\n(Press any key when ready)')

    # display countdown
    display.countdown(controller)

    # start eye tracking
    if not controller.testing:
        controller.tobii_cont.setDataFile(outfile)
        controller.tobii_cont.startTracking()
        controller.tobii_cont.setEventsAndParams(
            ['task', 'soundtime', 'presstime', 'cuetime', 'correct', 'choice', 'iti_mean', 'iti_range', 'trialvec'])
        controller.tobii_cont.setParam('task', 'revlearn')
        controller.tobii_cont.setParam('iti_mean', iti_mean)
        controller.tobii_cont.setParam('iti_range', iti_range)
        controller.tobii_cont.setVector('trialvec', trialvec)
    core.wait(2)

    for isTrue in trialvec:
        # display cross
        display.cross(testWin)
        if not controller.testing:
            controller.tobii_cont.recordEvent('cuetime')

        keypress = event.waitKeys(keyList=['left', 'right', 'q'])
        if not controller.testing:
            controller.tobii_cont.recordEvent('presstime')
            controller.tobii_cont.addParam('choice', keypress[0])
        if keypress[0] == 'q':
            break
        elif (keypress[0] == 'left' and not isTrue) or (keypress[0] == 'right' and isTrue):
            if not controller.testing:
                controller.tobii_cont.recordEvent('soundtime')
            rightsnd.play()
            correct = 1
        else:
            if not controller.testing:
                controller.tobii_cont.recordEvent('soundtime')
            wrongsnd.play()
            correct = 0
        if not controller.testing:
            controller.tobii_cont.addParam('correct', correct)
        # outcome period
        core.wait(1.0)
        # clear screen
        testWin.flip(clearBuffer=True)

        iti = iti_mean + iti_range * (2 * np.random.random() - 1)
        core.wait(iti)

    # stop eye tracking and save data
    if not controller.testing:
        controller.tobii_cont.stopTracking()
        controller.tobii_cont.flushData()
    testWin.close()


def makeswitches(path, nswitch, minrun, maxrun, seed):
    # set the seed
    np.random.seed(seed)

    # run lengths (between min and max) for each switch
    lens = np.random.random_integers(minrun, maxrun, nswitch + 1)
    # calculate switches
    switchtrials = np.cumsum(lens)
    isswitch = np.zeros((1, switchtrials[-1]))[0]
    isswitch[switchtrials[:-1]] = 1

    vals = np.zeros((1, nswitch + 1))[0]
    vals[1::2] = 1  # decides value at each switch

    # assign switch lengths to values
    whichval = np.cumsum(isswitch)
    trials = np.zeros((1, switchtrials[-1]))[0]
    for i in range(len(trials)):
        trials[i] = vals[whichval[i]]

    np.savetxt(path, trials, delimiter=",")
    return trials

if __name__ == '__main__':
    # revlearn(None,0,5,3,7)
    revlearn(None, 1)

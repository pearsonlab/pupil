import numpy as np
from psychopy import prefs
prefs.general['audioLib'] = ['pyo']
from psychopy import visual, core, sound, event
import display


def revlearn(outfile, flag, *args):
    # create new switch file
    if flag == 0:
        numswitches = args[0]
        minbetween = args[1]
        maxbetween = args[2]
        trialvec = makeswitches(
            numswitches, minbetween, maxbetween, np.random.randint(1, 9999))
    # loads from previously created switch file
    elif flag == 1:
        trialvec = np.genfromtxt('RevVectors.csv', delimiter=',')

    # set up window
    # Create window to display test
    testWin = visual.Window(
        size=(640, 400), monitor="testMonitor", units="pix")

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
    display.countdown(testWin, 4)

    # start eye tracking

    core.wait(2)

    for isTrue in trialvec:
        # display cross
        display.cross(testWin)

        keypress = event.waitKeys(keyList=['left', 'right', 'q'])
        if keypress[0] == 'q':
            break
        elif (keypress[0] == 'left' and not isTrue) or (keypress[0] == 'right' and isTrue):
            # record timestamp for key press
            rightsnd.play()
            correct = 1
        else:
            # record timestamp for key press
            wrongsnd.play()
            correct = 0
        # outcome period
        core.wait(1.0)
        # clear screen
        testWin.flip(clearBuffer=True)

        iti = iti_mean + iti_range * (2 * np.random.random() - 1)
        core.wait(iti)

        # save data for each trial (i.e. timestamps, choice, correctness, task
        # and parameters)

    # stop eye tracking

    # read eye data and save


def makeswitches(nswitch, minrun, maxrun, seed):
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

    np.savetxt('RevVectors.csv', trials, delimiter=",")
    return trials

if __name__ == '__main__':
    # revlearn(None,0,5,3,7)
    revlearn(None, 1)

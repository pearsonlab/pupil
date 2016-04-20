import numpy as np
import random
from psychopy import prefs
prefs.general['audioLib'] = ['pyo']
from psychopy import gui, sound, core, event
import display

def code_settings(controller):
    settingsDlg = gui.Dlg(title="Code")
    settingsDlg.addText('Set Parameters')
    settingsDlg.addField(
        'Response Time', controller.settings['Code: Response Time'])
    settingsDlg.addField(
        'Code Length', controller.settings['Code: Code Length'])
    settingsDlg.show()  # show dialog and wait for OK or Cancel
    if settingsDlg.OK:
        return settingsDlg.data
    else:
        return None

def code_game(controller, outfile):
    settings = code_settings(controller)
    if settings is not None:
        resp_time, code_length = settings
    else:
        return

    testWin = controller.launchWindow()
    display.text_keypress(testWin, "In this task, you will hear a chime.\n" +
                                   "Soon afterwards, you will be presented\n" +
                                   "with a code that you must reenter as\n" +
                                   "quickly as possible.")
    display.text_keypress(testWin, "If you do not respond in time, a loud,\n" +
                                   "unpleasant sound will play.")
    display.text_keypress(testWin, "Press any key to begin.")

    wrongsnd = sound.Sound('sounds/scary/276.wav')
    chime = sound.Sound('../task/dinga.wav', volume=0.4)

    display.countdown(controller)

    # START EYE TRACKING
    if not controller.testing:
        controller.tobii_cont.setDataFile(outfile)
        controller.tobii_cont.startTracking()
        controller.tobii_cont.setEventsAndParams(
            ['task', 'chimetime', 'codetime', 'endtime', 'resulttime',
             'resp_time', 'code_length', 'start_time'])
        controller.tobii_cont.setParam('task', 'code')
        controller.tobii_cont.setParam('resp_time', resp_time)
        controller.tobii_cont.setParam('code_length', code_length)
        controller.tobii_cont.setParam('start_time', core.getTime())

    wait_var = (np.random.rand() - 0.5) * 4
    core.wait(5 + wait_var)

    if not controller.testing:
        controller.tobii_cont.recordEvent('chimetime')
    chime.play()

    code = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range(code_length))
    core.wait(1.0)

    if not controller.testing:
        controller.tobii_cont.recordEvent('codetime')
    display.text(testWin, code)
    timer = core.CountdownTimer(resp_time)
    wrong = False
    for char in code:
        event.waitKeys(maxWait=timer.getTime(), keyList=char)
        if timer.getTime() <= 0:
            wrong = True
            break
    if timer.getTime > 0:
        core.wait(timer.getTime())

    if not controller.testing:
        controller.tobii_cont.recordEvent('endtime')
    display.text(testWin, "Time's up!")
    core.wait(2.0)
    if not controller.testing:
        controller.tobii_cont.recordEvent('resulttime')
    if wrong:
        wrongsnd.play()
        display.text(testWin, "Wrong")
    else:
        display.text(testWin, "Correct!")

    core.wait(6.0)
    if not controller.testing:
        controller.tobii_cont.stopTracking()
        display.text(testWin, 'Generating Figure...')
        image_file = outfile.name.split('.json')[0] + '_pupil_response.png'
        try:
            controller.tobii_cont.print_marked_fig(
                image_file, ['chimetime', 'codetime', 'endtime', 'resulttime'])
            display.image_keypress(testWin, image_file)
        except:
            display.text(testWin, 'Figure generation failed.')
        controller.tobii_cont.flushData()
    testWin.close()



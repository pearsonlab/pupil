import numpy as np
import random
from psychopy import prefs
prefs.general['audioLib'] = ['pyo']
from psychopy import gui, sound, core, event
import display


def alarm_settings(controller):
    settingsDlg = gui.Dlg(title="Alarm")
    settingsDlg.addText('Set Parameters')
    settingsDlg.addField(
        'Code Length', controller.settings['Alarm: Code Length'])
    settingsDlg.addField(
        'Number of Trials', controller.settings['Alarm: Number of Trials'])
    settingsDlg.show()  # show dialog and wait for OK or Cancel
    if settingsDlg.OK:
        return settingsDlg.data
    else:
        return None


def alarm_game(controller, outfile):
    settings = alarm_settings(controller)
    if settings is not None:
        code_length, num_trials = settings
    else:
        return

    testWin = controller.launchWindow()
    display.text_keypress(testWin, "In this task, you will hear a chime.\n" +
                                   "Soon afterwards, you will be presented\n" +
                                   "with a code that you must reenter as\n" +
                                   "quickly as possible in order to turn\n" +
                                   "off the alarm that begins to play.")
    display.text_keypress(testWin, "Press any key to begin.")

    chime = sound.Sound('sounds/alarm/chime.wav', volume=0.25)
    alarm = sound.Sound('sounds/alarm/fire_alarm.wav')

    display.countdown(controller)

    # START EYE TRACKING
    if not controller.testing:
        controller.tobii_cont.setDataFile(outfile)
        controller.tobii_cont.startTracking()
        controller.tobii_cont.setEventsAndParams(
            ['task', 'chimetime', 'alarmtime', 'finishtime',
             'code_length', 'start_time', 'num_trials'])
        controller.tobii_cont.setParam('task', 'alarm')
        controller.tobii_cont.setParam('code_length', code_length)
        controller.tobii_cont.setParam('num_trials', num_trials)
        controller.tobii_cont.setParam('start_time', core.getTime())

    for i in range(num_trials):
        display.cross(testWin)
        wait_var = np.random.rand() * 5
        core.wait(10 + wait_var)

        code = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz')
                       for i in range(code_length))

        if not controller.testing:
            controller.tobii_cont.recordEvent('chimetime')
        chime.play()
        core.wait(1.0)

        if not controller.testing:
            controller.tobii_cont.recordEvent('alarmtime')
        alarm.play()
        i = 0
        for char in code:
            display.text(testWin, i * ' ' + code[i:])
            event.waitKeys(keyList=char)
            i += 1

        if not controller.testing:
            controller.tobii_cont.recordEvent('finishtime')
        alarm.stop()
        display.text(testWin, "Good job!")
        core.wait(2.0)

    if not controller.testing:
        controller.tobii_cont.stopTracking()
        display.text(testWin, 'Generating Figure...')
        image_file = outfile.name.split('.json')[0] + '_whole_run.png'
        try:
            controller.tobii_cont.print_marked_fig(
                image_file, ['chimetime', 'alarmtime', 'finishtime'])
            display.image_keypress(testWin, image_file)
        except:
            display.text(testWin, 'Figure generation failed.')

        image_file = outfile.name.split('.json')[0] + '_summary.png'

        try:
            controller.tobii_cont.print_response(
                image_file, 'alarmtime', tpre=1.0, tpost=6.0)
            display.image_keypress(testWin, image_file)
        except:
            display.text(testWin, 'Figure generation failed.')

        controller.tobii_cont.flushData()
    testWin.close()

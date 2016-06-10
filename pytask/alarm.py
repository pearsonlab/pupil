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
        'Number of Normal Trials',
        controller.settings['Alarm: Number of Normal Trials'])
    settingsDlg.addField(
        'Number of Aversive Trials',
        controller.settings['Alarm: Number of Aversive Trials'])
    settingsDlg.show()  # show dialog and wait for OK or Cancel
    if settingsDlg.OK:
        return settingsDlg.data
    else:
        return None


def alarm_game(controller, outfile):
    settings = alarm_settings(controller)
    if settings is not None:
        num_normal, num_aversive = settings
    else:
        return

    testWin = controller.launchWindow()

    aversive_color = (227, 2, 24)
    neutral_color = (95, 183, 46)

    phone_ring = sound.Sound('sounds/alarm/phone_ring.wav', volume=0.10)
    alarm = sound.Sound('sounds/alarm/fire_alarm.wav')

    normal = ([0] * num_normal)
    aversive = ([1] * num_aversive)
    diff = num_normal - num_aversive
    if diff < 0:
        normal += (abs(diff) * [-1])
        random.shuffle(normal)
    elif diff > 0:
        aversive += (diff * [-1])
        random.shuffle(aversive)

    pairs = zip(normal, aversive)
    trialvec = []
    for pair in pairs:
        shuf_pair = list(pair)
        random.shuffle(shuf_pair)
        trialvec += shuf_pair
    if -1 in trialvec:
        trialvec.remove(-1)
    trialvec = np.array(trialvec)

    display.text_keypress(testWin, "In this task, you will see a colored\n" +
                                   "circle, followed by a sound.\n" +
                                   "When you hear a sound, press\n" +
                                   "any key to shut it off.")
    display.text_keypress(testWin, "Red circles are followed by a loud, harsh\n" +
                                   "sound.\n" +
                                   "Press any key to see a demo.")
    display.circle(testWin, aversive_color)
    core.wait(1.0)
    alarm.play()
    core.wait(1.0)
    alarm.stop()
    display.text_keypress(testWin, "Green circles are followed by a neutral\n" +
                                   "sound.\n" +
                                   "Press any key to see a demo.")
    display.circle(testWin, neutral_color)
    core.wait(1.0)
    phone_ring.play()
    core.wait(2.0)
    phone_ring.stop()
    display.text_keypress(testWin, "Press any key to begin the task.")

    display.countdown(controller)

    # START EYE TRACKING
    if not controller.testing:
        controller.tobii_cont.setDataFile(outfile)
        controller.tobii_cont.startTracking()
        controller.tobii_cont.setEventsAndParams(
            ['task', 'cuetime', 'soundtime', 'finishtime', 'trialvec'
             'start_time', 'num_normal', 'num_aversive'])
        controller.tobii_cont.setParam('task', 'alarm')
        controller.tobii_cont.setVector('trialvec', trialvec)
        controller.tobii_cont.setParam('num_normal', num_normal)
        controller.tobii_cont.setParam('num_aversive', num_aversive)
        controller.tobii_cont.setParam('start_time', core.getTime())

    for trial_type in trialvec:
        if trial_type == 0:
            color = neutral_color
            trial_sound = phone_ring
        elif trial_type == 1:
            color = aversive_color
            trial_sound = alarm
        else:
            raise Exception("Unknown value in trialvec")

        display.cross(testWin)
        wait_var = np.random.rand() * 5
        core.wait(10 + wait_var)

        if not controller.testing:
            controller.tobii_cont.recordEvent('cuetime')
        display.circle(testWin, color)
        core.wait(np.random.rand() * 3 + 1)

        if not controller.testing:
            controller.tobii_cont.recordEvent('soundtime')
        trial_sound.play()

        event.waitKeys()

        if not controller.testing:
            controller.tobii_cont.recordEvent('finishtime')
        trial_sound.stop()

        core.wait(1.0)

    if not controller.testing:
        controller.tobii_cont.stopTracking()
        display.text(testWin, 'Generating Figure...')
        image_file = outfile.name.split('.json')[0] + '_whole_run.png'
        try:
            controller.tobii_cont.print_marked_fig(
                image_file, ['cuetime', 'finishtime'])
            display.image_keypress(testWin, image_file)
        except:
            display.text(testWin, 'Figure generation failed.')

        image_file = outfile.name.split('.json')[0] + '_cuetime_comp.png'

        try:
            controller.tobii_cont.print_fig(
                image_file, 'cuetime', 'trialvec', tpre=1.0, tpost=8.0)
            display.image_keypress(testWin, image_file)
        except:
            display.text(testWin, 'Figure generation failed.')

        image_file = outfile.name.split('.json')[0] + '_finishtime_comp.png'

        try:
            controller.tobii_cont.print_fig(
                image_file, 'finishtime', 'trialvec', tpre=5.0, tpost=5.0)
            display.image_keypress(testWin, image_file)
        except:
            display.text(testWin, 'Figure generation failed.')

        controller.tobii_cont.flushData()
    testWin.close()

import numpy as np
import random
from psychopy import prefs
prefs.general['audioLib'] = ['pyo']
from psychopy import gui, sound, core
import display


def shock_settings(controller):
    settingsDlg = gui.Dlg(title="Shock")
    settingsDlg.addText('Set Parameters')
    settingsDlg.addField(
        'Number of Normal Trials',
        controller.settings['Shock: Number of Normal Trials'])
    settingsDlg.addField(
        'Number of Shock Trials',
        controller.settings['Shock: Number of Shock Trials'])
    settingsDlg.addField(
        'Shock Type', choices=['Sound', 'E-Stim'])
    settingsDlg.show()  # show dialog and wait for OK or Cancel
    if settingsDlg.OK:
        return settingsDlg.data
    else:
        return None


def shock_game(controller, outfile):
    settings = shock_settings(controller)
    if settings is not None:
        num_normal, num_shock, shock_type = settings
        soundstim = (shock_type == 'Sound')
    else:
        return

    window_color = (115, 114, 114)
    text_color = (203, 189, 26)
    shock_color = (227, 2, 24)
    neutral_color = (95, 183, 46)

    testWin = controller.launchWindow(window_color)

    if soundstim:
        neg_sound = sound.Sound('sounds/alarm/fire_alarm.wav', volume=0.05)
        stim_sound = sound.Sound('sounds/alarm/fire_alarm.wav')
    else:
        neg_sound = None
        trigger_val = 10 * np.ones(2200)
        stim_sound = sound.SoundPyo(value=trigger_val, secs=0.05, octave=8,
                                    volume=1.0, sampleRate=44100)

    normal = ([0] * num_normal)
    shock = ([1] * num_shock)
    diff = num_normal - num_shock
    if diff < 0:
        normal += (abs(diff) * [-1])
        random.shuffle(normal)
    elif diff > 0:
        shock += (diff * [-1])
        random.shuffle(shock)

    pairs = zip(normal, shock)
    trialvec = []
    for pair in pairs:
        shuf_pair = list(pair)
        random.shuffle(shuf_pair)
        trialvec += shuf_pair
    while -1 in trialvec:
        trialvec.remove(-1)
    trialvec = np.array(trialvec)

    display.text_keypress(testWin, "In this task, you will see two different\n" +
                                   "colored circles.\n", color=text_color)
    display.text_keypress(testWin, "Red circles will be followed by a shock\n" +
                                   "Press any key for a demo.",
                          color=text_color)
    display.circle(testWin, shock_color)
    core.wait(4.0)
    stim_sound.play()
    core.wait(1.0)
    stim_sound.stop()
    display.text_keypress(testWin, "Green circles will have no shock.\n" +
                                   "Press any key to see a demo.",
                          color=text_color)
    display.circle(testWin, neutral_color)
    if neg_sound is not None:
        core.wait(3.0)
        neg_sound.play()
        core.wait(2.0)
        neg_sound.stop()
    else:
        core.wait(5.0)
    display.text_keypress(testWin, "During the task, please make sure not \n" +
                                   "to look away from the screen.\n",
                          color=text_color)
    display.text_keypress(testWin, "Press any key to begin the task.",
                          color=text_color)

    display.countdown(controller, color=text_color)

    # START EYE TRACKING
    if not controller.testing:
        controller.tobii_cont.setDataFile(outfile)
        controller.tobii_cont.startTracking()
        controller.tobii_cont.setEventsAndParams(
            ['task', 'cuetime', 'shocktime', 'posttime', 'trialvec'
             'start_time', 'num_normal', 'num_shock'])
        controller.tobii_cont.setParam('task', 'alarm')
        controller.tobii_cont.setVector('trialvec', trialvec)
        controller.tobii_cont.setParam('num_normal', num_normal)
        controller.tobii_cont.setParam('num_shock', num_shock)
        controller.tobii_cont.setParam('start_time', core.getTime())

    for trial_type in trialvec:
        if trial_type == 0:
            color = neutral_color
            trial_sound = neg_sound
            sound_wait = 2.0
        elif trial_type == 1:
            color = shock_color
            trial_sound = stim_sound
            sound_wait = 2.0
        else:
            raise Exception("Unknown value in trialvec")

        display.cross(testWin, color=text_color)
        wait_var = np.random.rand() * 2
        core.wait(4 + wait_var)

        if not controller.testing:
            controller.tobii_cont.recordEvent('cuetime')
        display.circle(testWin, color)
        core.wait(4.0)

        if not controller.testing:
            controller.tobii_cont.recordEvent('shocktime')
        if trial_sound is not None:
            trial_sound.play()
            core.wait(sound_wait)
            trial_sound.stop()
        else:
            core.wait(1.0)

        core.wait(1.0)

        if not controller.testing:
            controller.tobii_cont.recordEvent('posttime')

    if not controller.testing:
        controller.tobii_cont.stopTracking()
        display.text(testWin, 'Generating Figure...')
        image_file = outfile.name.split('.json')[0] + '_whole_run.png'
        try:
            controller.tobii_cont.print_marked_fig(
                image_file, ['cuetime', 'shocktime'])
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

        image_file = outfile.name.split('.json')[0] + '_posttime_comp.png'

        try:
            controller.tobii_cont.print_fig(
                image_file, 'posttime', 'trialvec', tpre=5.0, tpost=5.0)
            display.image_keypress(testWin, image_file)
        except:
            display.text(testWin, 'Figure generation failed.')

        controller.tobii_cont.flushData()
    testWin.close()

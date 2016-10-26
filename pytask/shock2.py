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
        'Number of Shock Trials',
        controller.settings['Shock: Number of Shock Trials'])
    settingsDlg.addField(
        'Shock Type', choices=['E-Stim', 'Sound'])
    settingsDlg.show()  # show dialog and wait for OK or Cancel
    if settingsDlg.OK:
        return settingsDlg.data
    else:
        return None


def shock_game(controller, outfile):
    settings = shock_settings(controller)
    if settings is not None:
        num_shock, shock_type = settings
        soundstim = (shock_type == 'Sound')
    else:
        return

    window_color = (115, 114, 114)
    text_color = (203, 189, 26)

    testWin = controller.launchWindow(window_color)

    if soundstim:
        stim_sound = sound.Sound('sounds/alarm/fire_alarm.wav')
    else:
        trigger_val = 10 * np.ones(2200)
        stim_sound = sound.SoundPyo(value=trigger_val, secs=0.05, octave=8,
                                    volume=1.0, sampleRate=44100)

    display.text_keypress(testWin, "In this task, you will experience a\n" +
                                   "series of shocks with increasing\n" +
                                   "intensity.\n\n" +
                                   "Press any key for an example shock",
                          color=text_color)
    core.wait(4.0)
    stim_sound.play()
    core.wait(1.0)
    stim_sound.stop()

    display.text_keypress(testWin, "During the task, please make sure not \n" +
                                   "to look away from the screen.\n\n" +
                                   "Press any key to begin",
                          color=text_color)

    display.countdown(controller, color=text_color)

    # START EYE TRACKING
    if not controller.testing:
        controller.tobii_cont.setDataFile(outfile)
        controller.tobii_cont.startTracking()
        controller.tobii_cont.setEventsAndParams(
            ['task', 'shocktime', 'trialvec'
             'start_time', 'num_shock'])
        controller.tobii_cont.setParam('task', 'shock')
        controller.tobii_cont.setParam('num_shock', num_shock)
        controller.tobii_cont.setParam('start_time', core.getTime())
    core.wait(5.0)
    for i in range(num_shock):
        display.cross(testWin, color=text_color)

        core.wait(5.0)

        if not controller.testing:
            controller.tobii_cont.recordEvent('shocktime')
        stim_sound.play()
        core.wait(stim_sound.getDuration())
        stim_sound.stop()

    if not controller.testing:
        controller.tobii_cont.stopTracking()
        display.text(testWin, 'Generating Figure...')
        image_file = outfile.name.split('.json')[0] + '_whole_run.png'
        try:
            controller.tobii_cont.print_marked_fig(
                image_file, ['shocktime'])
            display.image_keypress(testWin, image_file)
        except:
            display.text(testWin, 'Figure generation failed.')

        image_file = outfile.name.split('.json')[0] + '_shocktime_comp.png'

        try:
            controller.tobii_cont.print_response(
                image_file, 'shocktime', tpre=5.0, tpost=1.0)
            display.image_keypress(testWin, image_file)
        except:
            display.text(testWin, 'Figure generation failed.')

        controller.tobii_cont.flushData()
    testWin.close()

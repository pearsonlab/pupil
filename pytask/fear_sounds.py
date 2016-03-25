import os
import display
from psychopy import core, sound
import random
from glob import glob


def play(controller, outfile):
    sound_order = glob('sounds/scary/*.wav') + glob('sounds/neutral/*.wav')
    random.shuffle(sound_order)
    is_scary = []
    for snd in sound_order:
        if 'scary' in snd:
            is_scary.append(1)
        else:
            is_scary.append(0)

    testWin = controller.launchWindow()

    display.text_keypress(testWin, 'In this task, you will hear some sound ' +
                                   'clips that are either scary or not' +
                                   '\n\nPress any key to continue.')

    if not controller.testing:
        controller.tobii_cont.setDataFile(outfile)
        controller.tobii_cont.startTracking()
        controller.tobii_cont.setEventsAndParams(
            ['task', 'stim_start', 'stim_end', 'sound_order', 'is_scary', 'start_time'])
        controller.tobii_cont.setParam('task', 'fear_sounds')
        controller.tobii_cont.setVector('sound_order', sound_order)
        controller.tobii_cont.setVector('is_scary', is_scary)
        controller.tobii_cont.setParam('start_time', core.getTime())

    core.wait(2.0)

    for sound_file in sound_order:
        snd = sound.SoundPyo(value=sound_file)
        if not controller.testing:
            controller.tobii_cont.recordEvent('stim_start')

        snd.play()
        core.wait(snd.getDuration())

        if not controller.testing:
            controller.tobii_cont.recordEvent('stim_end')

        core.wait(3.0)

    if not controller.testing:
        controller.tobii_cont.stopTracking()
        display.text(testWin, 'Generating Figure...')
        image_file = os.path.join(
            controller.data_filepath, controller.trial_name + '_whole_trial.png')
        try:
            controller.tobii_cont.print_whole_fig(
                image_file, 'stim_start', 'is_scary')
            display.image_keypress(testWin, image_file)
        except:
            display.text(testWin, 'Figure generation failed.')

        image_file = os.path.join(
            controller.data_filepath, controller.trial_name + '_pupil_response.png')
        try:
            controller.tobii_cont.print_fig(
                image_file, 'stim_start', 'is_scary', tpre=1.0, tpost=7.5)
            display.image_keypress(testWin, image_file)
        except:
            display.text(testWin, 'Figure generation failed.')

        controller.tobii_cont.flushData()

    testWin.close()

    return

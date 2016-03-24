import os
import display
from psychopy import event, core, visual
import random


def play(controller, outfile):
    clip_order = ['videos/control3.mp4', 'videos/horror3.mp4']
    clip_time = 180.0
    random.shuffle(clip_order)
    is_horror = []
    for clip in clip_order:
        if 'horror' in clip:
            is_horror.append(1)
        else:
            is_horror.append(0)

    testWin = controller.launchWindow()

    display.text_keypress(testWin, 'In this task, you will view some movie ' +
                                   'clips that are either scary or not' +
                                   '\n\nPress any key to continue.')

    if not controller.testing:
        controller.tobii_cont.setDataFile(outfile)
        controller.tobii_cont.startTracking()
        controller.tobii_cont.setEventsAndParams(
            ['task', 'stim_start', 'stim_end', 'clip_order', 'is_horror', 'start_time'])
        controller.tobii_cont.setParam('task', 'movie_clips')
        controller.tobii_cont.setVector('clip_order', clip_order)
        controller.tobii_cont.setVector('is_horror', is_horror)
        controller.tobii_cont.setParam('start_time', core.getTime())

    core.wait(2.0)

    size = (1920, 1080)

    for clip in clip_order:
        if 'horror' in clip:
            display.text_keypress(testWin, "Horror scene.\n\n" +
                                           "Press any key to continue.")
        else:
            display.text_keypress(testWin, "Non-horror scene.\n\n" +
                                           "Press any key to continue.")

        if not controller.testing:
            controller.tobii_cont.recordEvent('stim_start')

        timer = core.Clock()
        mov = visual.MovieStim2(testWin,
                                filename=clip,
                                units='pix',
                                size=size)
        if 'control3' in clip:
            mov.setVolume(40)
        shouldflip = mov.play()
        while mov.status != visual.FINISHED and timer.getTime() < clip_time:
            if shouldflip:
                testWin.flip()
            else:
                core.wait(0.001)
            shouldflip = mov.draw()
            if event.getKeys(keyList=['escape', 'q']):
                mov.stop()
                if not controller.testing:
                    controller.tobii_cont.stopTracking()
                testWin.close()
                core.quit()
        mov.stop()
        testWin.flip()
        testWin.flip()

        # wait for full clip time to run in case actual clip is shorter.
        core.wait(clip_time - timer.getTime())

        if not controller.testing:
            controller.tobii_cont.recordEvent('stim_end')

    if not controller.testing:
        controller.tobii_cont.stopTracking()
        display.text(testWin, 'Generating Figure...')
        image_file = os.path.join(
            controller.data_filepath, controller.trial_name + '_pupil_response.png')
        try:
            controller.tobii_cont.print_fig(
                image_file, 'stim_start', 'is_horror', tpre=0.0, tpost=clip_time)
            display.image_keypress(testWin, image_file)
        except:
            display.text(testWin, 'Figure generation failed.')

        controller.tobii_cont.flushData()

    testWin.close()

    return

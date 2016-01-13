import os
import glob
import random
import display
from psychopy import event, gui, core, visual
import numpy as np


def faceSettings(controller):
    order_path = os.path.join(controller.settings_path, 'FacemorphOrder.csv')

    if os.path.isfile(order_path):
        generateDlg = gui.Dlg(title='Faces')
        generateDlg.addField(
            "Load existing (0) or generate (1) display order", 0)
        generateDlg.show()
        if generateDlg.OK:
            resp = generateDlg.data[0]
            if resp == 0:
                with open(order_path) as f:
                    return f.read().split(',')
        else:
            return [-999]

    setDlg = gui.Dlg(title='Faces')
    setDlg.addText('Set Parameters')
    setDlg.addField(
        'Number of angry facemorphs (max: 10)', controller.settings['Faces: Angry'])
    setDlg.addField(
        'Number of fearful facemorphs (max: 10)', controller.settings['Faces: Fearful'])
    setDlg.addField(
        'Number of male identity facemorphs (max: 5)', controller.settings['Faces: Male Identity'])
    setDlg.addField(
        'Number of female identity facemorphs (max: 5)', controller.settings['Faces: Female Identity'])
    setDlg.show()
    if setDlg.OK:
        return make_order(order_path, *setDlg.data)
    else:
        return [-999]


def make_order(path, n_angry, n_fearful, n_m_identity, n_f_identity):
    poss_anger = glob.glob('faces/anger/*')
    poss_fear = glob.glob('faces/fear/*')
    poss_m_ident = glob.glob('faces/identity/male/*')
    poss_f_ident = glob.glob('faces/identity/female/*')

    angry = random.sample(poss_anger, min(n_angry, len(poss_anger)))
    fearful = random.sample(poss_fear, min(n_fearful, len(poss_fear)))
    m_ident = random.sample(poss_m_ident, min(n_m_identity, len(poss_m_ident)))
    f_ident = random.sample(poss_f_ident, min(n_f_identity, len(poss_f_ident)))

    all_stims = angry + fearful + m_ident + f_ident
    random.shuffle(all_stims)

    with open(path, 'w') as f:
        for stim in all_stims:
            f.write(stim)
            if stim != all_stims[-1]:
                f.write(',')

    return all_stims


def faces(controller, outfile):
    face_order = faceSettings(controller)
    if face_order[0] == -999:
        return
    is_fear = []
    for face in face_order:
        if 'fear' in face:
            is_fear.append(1)
        else:
            is_fear.append(0)

    testWin = controller.launchWindow()
    iti_mean = 3
    iti_range = 2

    display.text_keypress(testWin, 'In this task, you will view some videos ' +
                                   'of faces.\n\nPress any key to continue.')
    display.countdown(controller)

    if not controller.testing:
        controller.tobii_cont.setDataFile(outfile)
        controller.tobii_cont.startTracking()
        controller.tobii_cont.setEventsAndParams(
            ['task', 'stim_start', 'stim_end', 'iti_mean', 'iti_range', 'stims_used', 'is_fear' 'start_time'])
        controller.tobii_cont.setParam('task', 'faces')
        controller.tobii_cont.setParam('iti_mean', iti_mean)
        controller.tobii_cont.setParam('iti_range', iti_range)
        controller.tobii_cont.setVector('stims_used', face_order)
        controller.tobii_cont.setVector('is_fear', is_fear)
        controller.tobii_cont.setParam('start_time', core.getTime())

    display.cross(controller.testWin)
    core.wait(2.0)

    for face in face_order:
        mov = visual.MovieStim3(testWin,
                                filename=face,
                                units='pix', noAudio=True)

        if not controller.testing:
            controller.tobii_cont.recordEvent('stim_start')

        while mov.status != visual.FINISHED:
            mov.draw()
            testWin.flip()
            if event.getKeys(keyList=['escape', 'q']):
                testWin.close()
                core.quit()

        if not controller.testing:
            controller.tobii_cont.recordEvent('stim_end')

        display.cross(controller.testWin)
        iti = iti_mean + iti_range * (2 * np.random.random() - 1)

        core.wait(iti)

    if not controller.testing:
        controller.tobii_cont.stopTracking()
        display.text(testWin, 'Generating Figure...')
        image_file = os.path.join(
            controller.data_filepath, controller.trial_name + '_pupil_response.png')
        try:
            controller.tobii_cont.print_fig(
                image_file, 'stim_start', 'is_fear')
            display.image_keypress(testWin, image_file)
        except:
            display.text(testWin, 'Figure generation failed.')

        controller.tobii_cont.flushData()

    testWin.close()

    return

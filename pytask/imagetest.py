'''
Code for image display test.
'''
from psychopy import visual, core, gui
import numpy as np
import display
import os


def image_settings(controller):
    order_path = os.path.join(controller.settings_path, 'ImageOrder.csv')
    if os.path.isfile(order_path):
        generateDlg = gui.Dlg(title="Image Test")
        generateDlg.addField(
            'Load existing (0) or Generate (1) Image Order?', 0)
        generateDlg.show()
        if generateDlg.OK:
            response = generateDlg.data[0]
            if response == 0:
                images = np.genfromtxt(order_path, delimiter=',', dtype=str)
            else:
                images = make_order(os.path.join(os.getcwd(), 'images'),
                                    order_path, np.random.randint(1, 9999))
        else:
            return (-999, [])
    else:
        images = make_order(os.path.join(os.getcwd(), 'images'),
                            order_path, np.random.randint(1, 9999))

    settingsDlg = gui.Dlg(title="Image Test")
    settingsDlg.addText('Set Parameters')
    settingsDlg.addField(
        'Image Duration', controller.settings['Image Test: Display Duration'])
    settingsDlg.show()  # show dialog and wait for OK or Cancel
    if settingsDlg.OK:
        response = settingsDlg.data

        return (response[0], images)
    else:
        return(-999, [])


def make_order(image_path, order_path, seed):
    # set the seed
    np.random.seed(seed)

    # look for image folder and generate list of images, then shuffle the order
    images = os.listdir(image_path)
    np.random.shuffle(images)

    np.savetxt(order_path, images, delimiter=",", fmt="%s")
    return images


def imagetest(controller, outfile):
    stim_dur, images = image_settings(controller)
    if stim_dur == -999:
        return
    display.text(controller.experWin, 'Running Image Test')
    # set up test window
    testWin = controller.testWin
    # parameters for task
    iti_mean = 3
    iti_range = 2
    # set up image stim object
    stim = visual.ImageStim(testWin, image=os.path.join(os.getcwd(), 'images', images[0]),
                            units='norm', size=(1.0, 1.0))
    # display instructions
    display.text_keypress(
        testWin, 'In this task, you will view some images. \n Press any key when ready to begin.')

    display.countdown(controller)

    # START EYE TRACKING
    if not controller.testing:
        controller.tobii_cont.setDataFile(outfile)
        controller.tobii_cont.startTracking()
        controller.tobii_cont.setEventsAndParams(
            ['task', 'imagetime', 'iti_mean', 'iti_range', 'image_order'])
        controller.tobii_cont.setParam('task', 'image_test')
        controller.tobii_cont.setParam('iti_mean', iti_mean)
        controller.tobii_cont.setParam('iti_range', iti_range)
        controller.tobii_cont.setVector('image_orer', images)

    core.wait(2.0)  # give small wait time before starting trial

    for image in images:
        if not controller.testing:
            # RECORD TIMESTAMP FOR IMAGE DISPLAY
            controller.tobii_cont.recordEvent('imagetime')
        # display image
        stim.setImage(os.path.join(os.getcwd(), 'images', image))
        stim.draw()
        testWin.flip()

        # wait for predetermined stim_dur time
        core.wait(stim_dur)

        # clear screen
        testWin.flip()

        iti = iti_mean + iti_range * (2 * np.random.random() - 1)

        core.wait(iti)

    # STOP EYE TRACKING AND SAVE DATA
    if not controller.testing:
        controller.tobii_cont.stopTracking()
        controller.tobii_cont.closeDataFile()

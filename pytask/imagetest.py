'''
Code for image display test.
'''
from psychopy import visual, core, gui
import numpy as np
import display
import os


def image_settings(controller):
    order_path = os.path.join(controller.settings_path, 'ImageOrder.csv')
    settingsDlg = gui.Dlg(title="Image Test")
    settingsDlg.addText('Set Parameters')
    settingsDlg.addField(
        'Image Duration', controller.settings['Image Test: Display Duration'])
    if os.path.isfile(order_path):
        generateDlg = gui.Dlg(title="Image Test")
        generateDlg.addField(
            'Load existing (0) or Generate (1) Image Order?', 0)
        generateDlg.show()
        if generateDlg.OK:
            response = generateDlg.data[0]
            if response == 0:
                images = np.genfromtxt(order_path, delimiter=',', dtype=str)
                settingsDlg.show()  # show dialog and wait for OK or Cancel
                if settingsDlg.OK:
                    response = settingsDlg.data
                    return (response[0], images)
                else:
                    return(-999, [])
            else:  # generate new
                settingsDlg.addField(
                    'Num Fear Images', controller.settings['Image Test: Number of Fear Images'])
                settingsDlg.addField(
                    'Min Between', controller.settings['Image Test: Minimum Between'])
                settingsDlg.addField(
                    'Max Between', controller.settings['Image Test: Maximum Between'])
                settingsDlg.show()  # show dialog and wait for OK or Cancel
                if settingsDlg.OK:
                    response = settingsDlg.data
                    images = make_order(order_path, response[1], response[2], response[3], np.random.randint(1, 9999))
                    return (response[0], images)
                else:
                    return(-999, [])
        else:
            return (-999, [])
    else:
        settingsDlg.addField(
            'Num Fear Images', controller.settings['Image Test: Number of Fear Images'])
        settingsDlg.addField(
            'Min Between', controller.settings['Image Test: Minimum Between'])
        settingsDlg.addField(
            'Max Between', controller.settings['Image Test: Maximum Between'])
        settingsDlg.show()  # show dialog and wait for OK or Cancel
        if settingsDlg.OK:
            response = settingsDlg.data
            images = make_order(order_path, response[1], response[2],
                                response[3], np.random.randint(1, 9999))
            return (response[0], images)
        else:
            return(-999, [])


def make_order(order_path, nimages, minbtwn, maxbtwn, seed):
    # set the seed
    np.random.seed(seed)

    # look for image folder and generate list of each type of image
    fear_ims = os.listdir('images/fear')
    neutral_ims = os.listdir('images/neutral')
    if '.DS_Store' in fear_ims:
        fear_ims.remove('.DS_Store')
    if '.DS_Store' in neutral_ims:
        neutral_ims.remove('.DS_Store')
    np.random.shuffle(fear_ims)
    np.random.shuffle(neutral_ims)

    # run lengths (between min and max) surround each fear image
    lens = np.random.random_integers(minbtwn, maxbtwn, nimages + 1)
    feartrials = np.cumsum(lens)
    isfear = np.zeros((1, feartrials[-1]))[0]
    isfear[feartrials[:-1]] = 1

    # use 'isfear' vector to choose images for test
    images = list(isfear)
    for i in range(len(images)):
        if images[i] == 1:
            images[i] = os.path.join('fear', fear_ims.pop())
        else:
            images[i] = os.path.join('neutral', neutral_ims.pop())

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
            ['task', 'imagetime', 'iti_mean', 'iti_range', 'image_order', 'isfear'])
        controller.tobii_cont.setParam('task', 'image_test')
        controller.tobii_cont.setParam('iti_mean', iti_mean)
        controller.tobii_cont.setParam('iti_range', iti_range)
        controller.tobii_cont.setVector('image_order', images)

    core.wait(2.0)  # give small wait time before starting trial

    for image in images:
        if not controller.testing:
            # RECORD TIMESTAMP FOR IMAGE DISPLAY
            controller.tobii_cont.recordEvent('imagetime')
            # record whether it is a fearful image or not
            if 'fear' in image:
                controller.tobii_cont.addParam('isfear', 1)
            else:
                controller.tobii_cont.addParam('isfear', 0)

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

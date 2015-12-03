import display


# creates and returns a calibrated tobii controller
def calibrate(controller):
    testWin = controller.launchWindow()
    display.text_keypress(testWin, 'Press Enter to Calibrate')
    controller.tobii_cont.create_calibration()
    controller.tobii_cont.start_calibration()
    status = controller.tobii_cont.wait_for_status(
        '/api/calibrations/' + controller.tobii_cont.calibration_id + '/status', 'ca_state', ['failed', 'calibrated'])
    if status == 'calibrated':
        display.text_keypress(testWin, 'Calibration Successful!')
    elif status == 'failed':
        display.text_keypress(
            testWin, 'Calibration Failed. Please try again.')
        controller.testWin.close()
        return
    # marks calibration as complete and opens up other actions
    controller.calib_complete = True
    controller.actions = controller.full_actions
    controller.testWin.close()
    return

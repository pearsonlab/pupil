from psychopy import gui
import os
import sys
import json
import time
import datetime
TESTING = 0
if not TESTING:
    import TobiiControllerP
import lightdarktest
import oddball
import revlearn
import calibrate
import display
import draweyes
import pst


class TaskController:

    def __init__(self, working_path):
        self.testing = TESTING
        self.path = working_path
        self.settings_path = os.path.join(self.path, 'settings')
        self.settings_file = os.path.join(self.settings_path, 'settings.json')
        if os.path.isfile(self.settings_file):
            with open(self.settings_file) as settings:
                self.settings = json.load(settings)
        else:
            with open("default_settings.json") as settings:
                self.settings = json.load(settings)
        self.data_path = os.path.join(self.path, 'data')
        self.testWin, self.experWin = display.getWindows(self)
        self.actions = [ # actions that can be executed
            '0) Draw Eyes',
            '1) Calibrate',
            's) Settings',
            'r) Reset to Default Settings',
            'q) Quit']
        self.full_actions = [ # actions that can be executed after calibration
            '0) Draw Eyes',
            '1) Re-Calibrate',
            '2) Light Test',
            '3) Dark Test',
            '4) Oddball',
            '5) RevLearn',
            '6) PST',
            's) Settings',
            'r) Reset to Default Settings',
            'q) Quit']
        if self.testing:
            self.actions = self.full_actions
        self.subject = 0
        # CONNECT TO EYE TRACKER
        if not self.testing:
            self.tobii_cont = TobiiControllerP.TobiiController(self.testWin, self.experWin)
            self.tobii_cont.waitForFindEyeTracker()
            self.tobii_cont.activate(self.tobii_cont.eyetrackers.keys()[0])
            self.calib_complete = False
        else:
            self.calib_complete = True

    # Takes number as input and executes corresponding task.  Also manages data files.
    def execute(self, action):
        data_filename = datetime.datetime.fromtimestamp(
            time.time()).strftime('%H_%M_%Son%m-%d-%Y.tsv')
        data_filepath = os.path.join(
            self.data_path, str(self.subject))
        if action == 'q':
            self.testWin.close()
            self.experWin.close()
            if not self.testing:
                self.tobii_cont.destroy()
            return False
        elif action == '2' and self.calib_complete:
            data_filepath = os.path.join(
                data_filepath, 'lighttest')
            if not os.path.isdir(data_filepath):
                os.makedirs(data_filepath)
            with open(os.path.join(data_filepath, data_filename), 'w') as light_file:
                lightdarktest.lightdarktest(self, 1, light_file)
            return True
        elif action == '3' and self.calib_complete:
            data_filepath = os.path.join(
                data_filepath, 'darktest')
            if not os.path.isdir(data_filepath):
                os.makedirs(data_filepath)
            with open(os.path.join(data_filepath, data_filename), 'w') as dark_file:
                lightdarktest.lightdarktest(self, 0, dark_file)
            return True
        elif action == '1' and not self.testing:
            calib_filename = datetime.datetime.fromtimestamp(
                time.time()).strftime('%H_%M_%Son%m-%d-%Y-Calibration.p')
            if not os.path.isdir(data_filepath):
                os.makedirs(data_filepath)
            with open(os.path.join(data_filepath, calib_filename), 'w') as calib_file:
                calibrate.calibrate(self, calib_file)
            return True
        elif action == '4' and self.calib_complete:
            data_filepath = os.path.join(
                data_filepath, 'oddball')
            if not os.path.isdir(data_filepath):
                os.makedirs(data_filepath)
            with open(os.path.join(data_filepath, data_filename), 'w') as odd_file:
                oddball.oddball(self, odd_file)
            return True
        elif action == '5' and self.calib_complete:
            data_filepath = os.path.join(
                data_filepath, 'revlearn')
            if not os.path.isdir(data_filepath):
                os.makedirs(data_filepath)
            with open(os.path.join(data_filepath, data_filename), 'w') as revlearn_file:
                revlearn.revlearn(self, revlearn_file)
            return True
        elif action == '6' and self.calib_complete:
            data_filepath = os.path.join(
                data_filepath, 'PST')
            if not os.path.isdir(data_filepath):
                os.makedirs(data_filepath)
            with open(os.path.join(data_filepath, data_filename), 'w') as pst_file:
                pst.pst(self, pst_file)
            return True
        elif action == '0' and not self.testing:
            draweyes.show_eyes()
            return True
        elif action == 's':
            # open settings box
            setting_window = gui.DlgFromDict(self.settings)
            if setting_window.OK:
                with open(self.settings_file, 'w+') as settings:
                    json.dump(self.settings, settings)
            return True
        elif action == 'r':
            # reset to default settings
            with open("default_settings.json") as settings:
                self.settings = json.load(settings)
            with open(self.settings_file, 'w+') as settings:
                json.dump(self.settings, settings)
            return True
        else:
            print "Please enter a valid action"
            return True

    def run(self):
        # make directories to store settings and data if they don't exist
        if not os.path.isdir(self.settings_path):
            os.mkdir(self.settings_path)
        if not os.path.isdir(self.data_path):
            os.mkdir(self.data_path)



        display.text(self.testWin,"Welcome, Participant!")
        display.text(self.experWin,"Welcome, Experimenter!")

        # execute actions from menu
        while self.execute(self.select_action()):
            display.text(self.testWin,"Welcome, Participant!")
            display.text(self.experWin,"Welcome, Experimenter!")

    def select_action(self): # pulls up main menu that selects action
        # action_dict = {
        #     'Action: ': self.actions, 'Subject Number: ': self.subject}
        # action_window = gui.DlgFromDict(action_dict)
        # if action_window.OK:
        #     self.subject = action_dict['Subject Number: ']
        #     return action_dict['Action: ']
        # else:
        #     return 'Quit'

        # DlgFromDict not working properly.  It clashes with the PsychoPy
        # visual module

        if not self.calib_complete:
            actionDlg = gui.Dlg(title="Select Action")
            actionDlg.addText('Choose Action from:')
            for action in self.actions:
                actionDlg.addText(action)
            actionDlg.addField('Action:', '1')
            actionDlg.addField('Subject ID: ', self.subject)
            actionDlg.show()  # show dialog and wait for OK or Cancel
            if actionDlg.OK:
                response = actionDlg.data
                self.subject = response[1]
                return response[0]
            else:
                return 'q'
        else:
            actionDlg = gui.Dlg(title="Select Action")
            actionDlg.addText('Choose Action from:')
            for action in self.actions:
                actionDlg.addText(action)
            actionDlg.addField('Action:', '1')
            actionDlg.addText('Subject ID: ' + str(self.subject))
            actionDlg.show()  # show dialog and wait for OK or Cancel
            if actionDlg.OK:
                response = actionDlg.data
                return response[0]
            else:
                return 'q'

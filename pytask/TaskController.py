from psychopy import gui
import os
import json
import lightdarktest
import oddball
import revlearn
import faces
import calibrate
import display
import pst
import movie_clips
import fear_sounds
import code
import shock
TESTING = 0
if not TESTING:
    import TobiiController


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
        self.actions = [  # actions that can be executed
            '1) Calibrate',
            's) Settings',
            'r) Reset to Default Settings',
            'q) Quit']
        self.full_actions = [  # actions that can be executed after calibration
            '1) Re-Calibrate',
            '2) Dark Test',
            '3) Light Test',
            '4) PST',
            '5) RevLearn',
            '6) Oddball',
            '7) Faces',
            '8) Movie Clips',
            '9) Fear Sounds',
            '10) Code',
            '11) Shock',
            's) Settings',
            'r) Reset to Default Settings',
            'q) Quit']
        if self.testing:
            self.actions = self.full_actions
        self.subject = 'subject_name'
        # CONNECT TO EYE TRACKER
        if not self.testing:
            self.tobii_cont = TobiiController.TobiiController()
            self.calib_complete = False
        else:
            self.calib_complete = True

    def launchWindow(self, color=(115, 114, 114)):
        self.testWin = display.getWindows(self, color)
        return self.testWin

    # Takes number as input and executes corresponding task.  Also manages
    # data files.
    def execute(self, action):
        if action in ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11']:
            trialDlg = gui.Dlg(title="Trial Name")
            trialDlg.addField(
                'Enter Trial Name', 'run1')
            trialDlg.show()
            if trialDlg.OK:
                self.trial_name = trialDlg.data[0]
                data_filename = '_' + self.trial_name
            else:
                return True
            if not self.testing:
                self.tobii_cont.create_recording()
                data_filename += '_projID-' + self.tobii_cont.project_id + \
                    '_recID-' + self.tobii_cont.recording_id + '.json'
            else:
                data_filename += '_projID-test_recID-test.json'
        self.data_filepath = os.path.join(
            self.data_path, str(self.subject))
        if action == 'q':
            return False
        elif action == '3' and self.calib_complete:
            self.data_filepath = os.path.join(
                self.data_filepath, 'lighttest')
            if not os.path.isdir(self.data_filepath):
                os.makedirs(self.data_filepath)
            data_filename = 'lighttest' + data_filename
            with open(os.path.join(self.data_filepath, data_filename), 'w') as light_file:
                lightdarktest.lightdarktest(self, 1, light_file)
            return True
        elif action == '2' and self.calib_complete:
            self.data_filepath = os.path.join(
                self.data_filepath, 'darktest')
            if not os.path.isdir(self.data_filepath):
                os.makedirs(self.data_filepath)
            data_filename = 'darktest' + data_filename
            with open(os.path.join(self.data_filepath, data_filename), 'w') as dark_file:
                lightdarktest.lightdarktest(self, 0, dark_file)
            return True
        elif action == '1' and not self.testing:
            calibrate.calibrate(self)
            return True
        elif action == '6' and self.calib_complete:
            self.data_filepath = os.path.join(
                self.data_filepath, 'oddball')
            if not os.path.isdir(self.data_filepath):
                os.makedirs(self.data_filepath)
            data_filename = 'oddball' + data_filename
            with open(os.path.join(self.data_filepath, data_filename), 'w') as odd_file:
                oddball.oddball(self, odd_file)
            return True
        elif action == '7' and self.calib_complete:
            self.data_filepath = os.path.join(
                self.data_filepath, 'faces')
            if not os.path.isdir(self.data_filepath):
                os.makedirs(self.data_filepath)
            data_filename = 'faces' + data_filename
            with open(os.path.join(self.data_filepath, data_filename), 'w') as face_file:
                faces.faces(self, face_file)
            return True
        elif action == '8' and self.calib_complete:
            self.data_filepath = os.path.join(
                self.data_filepath, 'movie_clips')
            if not os.path.isdir(self.data_filepath):
                os.makedirs(self.data_filepath)
            data_filename = 'movie_clips' + data_filename
            with open(os.path.join(self.data_filepath, data_filename), 'w') as clip_file:
                movie_clips.play(self, clip_file)
            return True
        elif action == '9' and self.calib_complete:
            self.data_filepath = os.path.join(
                self.data_filepath, 'fear_sounds')
            if not os.path.isdir(self.data_filepath):
                os.makedirs(self.data_filepath)
            data_filename = 'fear_sounds' + data_filename
            with open(os.path.join(self.data_filepath, data_filename), 'w') as sound_file:
                fear_sounds.play(self, sound_file)
            return True
        elif action == '10' and self.calib_complete:
            self.data_filepath = os.path.join(
                self.data_filepath, 'code')
            if not os.path.isdir(self.data_filepath):
                os.makedirs(self.data_filepath)
            data_filename = 'code' + data_filename
            with open(os.path.join(self.data_filepath, data_filename), 'w') as code_file:
                code.code_game(self, code_file)
            return True
        elif action == '11' and self.calib_complete:
            self.data_filepath = os.path.join(
                self.data_filepath, 'shock')
            if not os.path.isdir(self.data_filepath):
                os.makedirs(self.data_filepath)
            data_filename = 'shock' + data_filename
            with open(os.path.join(self.data_filepath, data_filename), 'w') as shock_file:
                shock.shock_game(self, shock_file)
            return True
        elif action == '5' and self.calib_complete:
            self.data_filepath = os.path.join(
                self.data_filepath, 'revlearn')
            if not os.path.isdir(self.data_filepath):
                os.makedirs(self.data_filepath)
            data_filename = 'revlearn' + data_filename
            with open(os.path.join(self.data_filepath, data_filename), 'w') as revlearn_file:
                revlearn.revlearn(self, revlearn_file)
            return True
        elif action == '4' and self.calib_complete:
            self.data_filepath = os.path.join(
                self.data_filepath, 'PST')
            if not os.path.isdir(self.data_filepath):
                os.makedirs(self.data_filepath)
            data_filename = 'PST' + data_filename
            with open(os.path.join(self.data_filepath, data_filename), 'w') as pst_file:
                pst.pst(self, pst_file)
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

        # execute actions from menu
        while self.execute(self.select_action()):
            pass

    def select_action(self):  # pulls up main menu that selects action
        if not self.calib_complete:
            actionDlg = gui.Dlg(title="Select Action")
            actionDlg.addText('Choose Action from:')
            for action in self.actions:
                actionDlg.addText(action)
            actionDlg.addField('Action:', '1')
            actionDlg.addField('Subject Name: ', self.subject)
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
            actionDlg.addText('Subject Name: ' + str(self.subject))
            actionDlg.show()  # show dialog and wait for OK or Cancel
            if actionDlg.OK:
                response = actionDlg.data
                return response[0]
            else:
                return 'q'

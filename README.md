# Pupil

## Task and analysis code for pupillometry studies with Tobii and Psychtoolbox

### Relies on the [Tobii SDK](http://www.tobii.com/en/eye-tracking-research/global/products/software/tobii-analytics-software-development-kit/) and [Psychophysics Toolbox](http://psychtoolbox.org/HomePage)

### Task folder

`TrackPupil.m` is adapted from the Tobii SDK and allows users to interactively see the positions of their eyes onscreen as recorded by the tracker. This is good for situating participants in the chair.

`pupiltest.m` is a master programming for running the individual tasks. Given a user code, it sets up the necessary directory structure for saving files and runs selected tasks. Tasks include:

- Calibration: calls `calibrate.m`, which handles calibration with the Tobii and must be run prior to the rest of the tests. 
- Dark Test: calls `lightdarktest.m`.
- Pupillary Sleep Test: calls `pst.m`.
- Light Test: calls `lightdarktest.m`.
- Reversal Learning: calls `revlearn.m`.
- Oddball: calls `oddball.m`.
- Surprise: not yet implemented.

Other functions inside the folder are either resources for the tasks (wav files) or helper functions for the task code.

### Analysis folder

- `sample_analysis_scratch.m` is a matlab file that can be used to run selected analyses on selected data files. When run, prompts the user to select a file to analyze. Based on the file name, the program will choose the appropriate analysis:

- `analyze_*.m` are analysis files called by the above, each for a particular task.
- `utils/` contains helper functions needed to convert timestamps and clean and interpolate raw data.

### Pytask folder

Folder for the python ports of the tasks, including a GUI based system

#### Contents

- 'start.py' - Initializes the Task Controller after taking in the home directory

- 'TaskController.py' - Creates file system to store data and settings, runs tasks, and launches dialogue boxes.

- 'display.py' - Miscellaneous functions for displaying text, countdowns, etc.

The other files are simply ports of the MATLAB versions.  They are called from TaskController.

#### Python Setup and Notes

##### Setup

1. Download and install driver for USB Serial port reader from [here](http://downloads.trendnet.com/tu-s9_v2/utilities/driver_tu-s9_20151110.zip).
1. Create a folder in a convenient location that you will want to store your data and preferences.  The Task Controller will ask, upon starting, the location of this working directory.  In the future, the Task Controller will load your settings from here as long as you select the same folder.  Your data will also be stored here, organized by subject ID numbers that you will be prompted for and the type of task.

##### Usage

1. Connect your wifi to the Tobii Glasses (network name is the serial number on the recording unit. Password is 'TobiiGlasses')
1. Load the 'start.py' file from the pytask folder in PsychoPy and click run.

##### Notes

- The 'TESTING' variable at the top of 'TaskController.py' should be set to 0 for data collection purposes.  It is used for testing on non-Tobii connected computers.
- Data files are named based on the recording ID and Session ID that are assigned by the glasses. These will align with the filenames on the SD card.
- Settings can be changed on a per trial basis without affecting the global settings.  Simply run a trial and change the values in the dialogue box.  If you want to change the defaults that show up in these dialogue boxes, go into settings from the main menu and edit there.  The original settings can be reloaded by entering 'r' on the main menu.

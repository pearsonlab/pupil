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

1. Go into Monitor Center on PsychoPy and make sure there are two monitors present.  The names should be 'testMonitor' and 'tobiiMonitor'.  If these do not exist, go ahead and create them.

2. Download the tobii SDK and copy the 'python27' folder into your PsychoPy install directory.

On Windows, this is under 'ProgramFiles(x86)\PsychoPy2'. 

On MacOS, this is accessed by finding PsychoPy2 in your Applications folder, right-clicking, and clicking 'open package contents'. The directory you want to copy to is called 'Contents'.

Rename the 'python27' folder to 'tobii'.  This will allow the PsychoPy version of Python to import the tobii SDK functions.

3. If you are running for the first time, create a folder in a convenient location that you will want to store your data and preferences.  The Task Controller will ask, upon starting, the location of this working directory.  In the future, the Task Controller will load your settings from here as long as you select the same folder.  Your data will also be stored here, organized by subject ID numbers that you will be prompted for and the type of task.

4. To begin, load the 'start.py' file in PsychoPy and click run.

5. The 'TESTING' variable at the top of 'TaskController.py' should be set to 0 for data collection purposes.  It is used for testing on non-Tobii connected computers.

NOTES

Data files are named based on the timestamp from the time the test was started.

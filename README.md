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

`sample_analysis_scratch.m` is a matlab file that can be used to run selected analyses on selected data files. When run, prompts the user to select a file to analyze. Based on the file name, the program will choose the appropriate analysis:

- `analyze_*.m` are analysis files called by the above, each for a particular task.
- `utils/` contains helper functions needed to convert timestamps and clean and interpolate raw data.

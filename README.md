README FILE FOR PUPIL REPOSITORY

TASK FOLDER - 

tetio_CONNECT.m is a matlab file that communicates with 
tobii using the psychtoolbox commands and SDK
interface and sets up a connection between the computer
and the tobii screen.

PTBprelims.m is a script that opens the PsychToolBox window. 

DrawEyes.m is a function file that draws stimuli at various locations
on the tobii screen that have been preset by John Pearson and are used
to calibrate the tobii eye tracker

pupiltest.m is skeleton file that calls other files to run the
battery of tests desired by the user. Once Run it will prompt for
user inputs and should be straightforward for use. 

TrackPupil.m is a script that opens a "Track Status" window that allows the
participant to see if his or her eyes are being tracked. The pupils will show up 
as green circles if they are properly being tracked. This window will pop up before 
every task in pupiltest in order to confirm eyes are still being tracked.

get_next_fname.m is a function that names pupiltest files and calculates the version
from files in the current directory. 

check_status.m is a function that is called in multiple other script files. It is
a function that takes information from the SDK "tetio_getTrackers" command. This 
function lets us know if conditions for connectivity to the Tobii eyetracker are 
met or whether there is a problem with the connection. It also checks for the 
synchronization of the computer and Tobii clocks.

countdown.m is a short script that is called in before calibrate,
or any tests display to the screen as implied by the name it creates
a small countdown displayed on the tobii eyetracker to signal to us
and to the patient that a test or calibration is about to begin.

calibrate.m is a function run at the beginning, before testing to ensure
that the tobii is calibrated to the new patient being tested IT IS IMPORTANT TO
RUN THIS BEFORE EVERY NEW PATIENT. If calibration is not successful the tasks cannot be run.

swirl.m is a function that draws the pattern for the calibration. 

lightdarktest.m is a function for both light and dark tests. In dark test, the patient is
habituated to a bright white screen displayed on the tobii and pupil diameter is tracked as
we darken the screen to completely black for a brief time period before returning to the pure
white screen and rehabituating. In light test, we habituate the patient to darkness via a 
darkened room and a black screen and then at intervals we flash the screen with whites of  
increasing luminance and record the pupillary response.

convertlums.m is a function that corrects for the disparity between luminance we want and
luminance the computer gives us. Its output is the RGB value that actually corresponds
to the luminance we want. 

pst.m is the pupillary sleep test. It is a way to guage baseline pupil diameter and it's fluctuations.
It shows a dark screen and holds for a specified duration currently set to 30 seconds.

setup_audio.m is a short file that initializes the PsychPortAudio player and allows us
to use the PsychPortAudio and it's low latency high accuracy player for sounds during
testing. It is important to use the PsychPortAudio functions because their low latency
is important when utilizing perfectly timed sound stimuli to test against pupil response
timing becomes an important factor at these millisecond timescales and the built in matlab
player doesn't have the finess needed and provided by PsychPortAudio.

playsound.m is a function that plays sound through PsychPortAudio. 

shutdown_audio.m is a script that stops playback and closes the audio device.

setup_geometry.m is another short file that relates to through the talk2tobii commands and
sets up initial parameters about the Tobii screen size and resolution and it initializes a
set of axis that we use when placing stimuli on the tobii screen. In cases when certain 
images must be displayed at certain locations setup_geometry.m helps initialize and use the
determined parameters for screen drawing.

fixcross.m is a script that paints the fixation cross for the reversal learning task 
on-screen.

handle_input.m is a function that activates live keys that allow participant key responses
to be recorded. 

revlearn.m is a function that create a revearsal learning task for the patient. 
The participant is instructed to press either the right or left arrow key, one of which
results in a correct "ding" and the other in an incorrect "buzzer." Participants must
try to get as many correct as possible while learning when switches occur. A fixation cross
signals when the participant should push a key.

RevVectors.mat is a workspace contains three "standard" vectors with four, five, and six 
reversal vector options. The vector controls the reversal switches in revlearn.m.
This can be loaded in pupiltest.

buzz1.wav is the wav file for the incorrect noise in revlearn.
ding3.wav is the wav file for the correct noise in revlearn.

makeswitches.m is a function that that 

makeoddballs.m is a function that creates a pseudo-random distribution of oddballs 
in a trial vector for the oddball task.

oddball.m function runs the oddball task. 500hz tone beeps are interspersed randomly 
with 1000hz tone beeps and the participant's keyboard input is recorded at each tone.
(NOTE: do not repeatedly execute before running a participant!)

OddballVectors.mat is a workspace that contains three "standard" vectors with four,
five, and six oddball vector options. This can be loaded in pupiltest.

500.wav is the wav file for the low tone in oddball.
1000.wav is the wav file for the high tone in oddball. 

display_instructions.m formats instructional text so it displays correctly centered 
on-screen using PsychToolBox. 

processlt.m is the current version of the processing script for the lighttest and darktest
tests that we run. It isolates the different test trials and plots the pupilary response 
data gathered by the tobii as well as my current attempts at nonlinear fits to those data plots
this is a working file and not completely free of bugs, but is useful for very minimal analysis
and checking that data collection is taking place successfully.


tstatus.m is a function similar to check_status.m but instead it prints to the command window
the actual state of laptop to tobii connection. Run this file to check what exact state of connection
tobii is in. Whether it is connecting, connnected, calibrating, etc.


ANALYSIS FOLDER - 

cleanplot.m is a "skeleton file' function that plots graphs for the whatever data file name is in the input.
The second input controls which eye data is plotted. With the exception of pupillary sleep test 
(output is one graph), thetwo graphs generated will be (1) of the raw data and (2) of overlaid pupillary 
response to stimuli. 

dataorg.m is a "skeleton file" function that organizes data into separate matrix and struct. The matrix is a four 
column matrix "datamat" that contains all eye data in one file. The struct "outdat" contains data chopped
to certain seconds before and after the stimulus event. 

findevents.m is a function that finds the timestamp bins corresponding to either sound or onscreen stimuli.

makemat.m is a function that makes "datamat", a matrix with four columns of data corresponding to left eye,
right eye, timestamp, and average of left and right eye from the whole task.

makesecs.m is a function that converts the timestamps in datamat into seconds.

evtsplit.m is a function that makes the "outdat," a struct containing eye data chopped into pieces from 
a certain number of seconds before to after the stimulus. The struct contains left, right, and averaged 
data.

defbin.m is a function that is called in evtsplit to define number of bins to grab before and after the
stimulus event in the data. 

normdat.m is a function that adds normalized versions of left, right, and averaged right eye data to 
the outdat struct. Currently normalizes with the average of 200ms before the stimulus.

plotraw.m is a generic function that plots the raw data for the length of the task from datamat.

plotlightdark.m is a function that plots the stimuli times on the raw plot and creates a second plot 
with the overlaid pupillary response to stimuli data.

plotoddrev.m a function that plots the stimuli times on the raw plot and creates a second plot 
with the average pupillary response to stimuli data for odd vs. normal sounds or correct vs. incorrect
responses.



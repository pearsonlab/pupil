README FILE FOR PUPIL REPOSITORY

CONNECT.m is a matlab file that communicates with 
tobii using the psychtoolbox commands and talk2tobii
interface and sets up a connection between the computer
and the tobii screen

DISCONNECT.m is a matlab file that disconnects from the tobii
screen this file and the CONNECT.m file are often called in other
matlab scripts or functions and aren't used themselves as often
as they are included in the skeleton of other files.

DRAW_EYES.m is a file that calls the DrawEyes.m function it is used
in CALIBRATE.m to draw the spots on the screen used to calibrate the
tobii eye tracker to the patient being tested based on distance from
the screen and pupil tracking position

DrawEyes.m is a function file that draws stimuli at various locations
on the tobii screen that have been preset by John Pearson and are used
to calibrate the tobii eye tracker

Oddball_Dev is SDK-based script that plays 500hz tone beeps interspersed randomly 
with 1000hz tone beeps and records the participant's keyboard input at the 
oddball, 1000hz tone. (NOTE: do not repeatedly execute before running a participant!)

ParticipantTester.m skeleton file that calls other files to run the
battery of tests desired by the user. Once Run it will prompt for
user inputs and should be straightforward for use

calibrate.m is the file run at the beginning, before testing to ensure
that the tobii is calibrated to the new patient being tested IT IS IMPORTANT TO
RUN THIS BEFORE EVERY NEW PATIENT. Also, it may be helpful to rerun after every
trial of ParticipantTester.m just to account for any adjustments or movements in
body position of the patient over the course of the testing session.

check_status.m is a function that is called in multiple other script files. It is
a function that takes information from the talk2tobii('GET_STATUS') command and 
outputs it onto the matlab command window. This function lets us know if conditions for
connectivity to the Tobii eyetracker are met or whether there is a problem with the
connection.

countdown.m is a short script that is called in before calibrate,
or any tests display to the screen as implied by the name it creates
a small countdown displayed on the tobii eyetracker to signal to us
and to the patient that a test or calibration is about to begin.

processlt.m is the current version of the processing script for the lighttest and darktest
tests that we run. It isolates the different test trials and plots the pupilary response 
data gathered by the tobii as well as my current attempts at nonlinear fits to those data plots
this is a working file and not completely free of bugs, but is useful for very minimal analysis
and checking that data collection is taking place successfully.

pst.m is the pupillary sleep test. It is a way to guage baseline pupil diameter and it's fluctuations.
It shows a dark screen and holds for a specified duration currently set to 30 seconds.

revearsallearning.m and reversallearningfcn.m are a script and function file
that together attempt to create a revearsal learning task for the patient. 
The task is a simple keyboard response to a visual and auditory stimuli placed
on the tobii eye tracker screen and played on the speakers. The test records pupil
response to the stimuli as the test proceeds and will soon be able to save data on
patient responses in relation to stimulus desired, stimulus displayed, and stimulus
heard. This test is not yet fully functional but will be shortly.

revsightsound.m is reversallearning.m with a few minor changes.

setup_audio.m is a short file that initializes the PsychPortAudio player and allows us
to use the PsychPortAudio and it's low latency high accuracy player for sounds during
testing. It is important to use the PsychPortAudio functions because their low latency
is important when utilizing perfectly timed sound stimuli to test against pupil response
timing becomes an important factor at these millisecond timescales and the built in matlab
player doesn't have the finess needed and provided by PsychPortAudio.

setup_geometry.m is another short file that relates to through the talk2tobii commands and
sets up initial parameters about the Tobii screen size and resolution and it initializes a
set of axis that we use when placing stimuli on the tobii screen. In cases when certain 
images must be displayed at certain locations setup_geometry.m helps initialize and use the
determined parameters for screen drawing.

testerdarktest.m is a current and working version of darktest.m. In this test the patient is
habituated to a bright white screen displayed on the tobii and pupil diameter is tracked as
we darken the screen to completely black for a brief time period before returning to the pure
white screen and rehabituating. The pupil resonse is tracked and recorded and can be observed
using processlt.m although the fitting for this test is not yet complete.

testerlighttest.m is the opposite of darktest. It is a functional version of lighttest.m. In this
test we habituate the patient to darkness via a darkened room and a black screen and then at
intervals we flash the screen with white and record the pupillary response.

tetio_CONNECT.m is the SDK compatible version of CONNECT.m.

tetio_ParticipantTester.m is the SDK-based version of ParticipantTester.m. It calls tetio scripts
to execute the different tasks (calibrate, testerlighttest, testerdarktest, reversallearning, oddball,
pupillary sleep test). Prior to tetio_swirlCalibrate it calls TrackStatus, an SDK script that allows 
the participant to position his or her eyes in front of the eye tracker.

tetio_check_status.m is SDK compatible script that (1) checks whether the tracker and computer 
clocks are synched and (2) the connection with Tobii.

tetio_pst.m is the SDK-based version of pst.m, the pupillary sleep test.

tetio_reversallearning.m is the SDK-based version of reversallearning.m, which creates the trial vector
for tetio_reversallearningfcn.m.

tetio_reversallearningfcn.m is the SDK-based version of reversallearningfcn.m.

tetio_swirl.m is the SDK-based version of swirl.m.

tetio_swirlCalibrate.m is the SDK-based version of calibrate.m.

tetio_testerlighttest.m is the SDK-based version of testerlightest.m.

tstatus.m is a function similar to check_status.m but instead it prints to the command window
the actual state of laptop to tobii connection. Run this file to check what exact state of connection
tobii is in. Whether it is connecting, connnected, calibrating, etc.

work_tetio_testerdarktest.m is the latest version of the SDK-based testerdarktest.m file. It calibrates
and executes testerdarktest.m. 

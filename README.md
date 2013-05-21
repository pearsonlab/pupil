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

ParticipantTester.m skeleton file that calls other files to run the
battery of tests desired by the user. Once Run it will prompt for
user inputs and should be straightforward for use

calibrate.m is the file run at the beginning, before testing to ensure
that the tobii is calibrated to the new patient being tested

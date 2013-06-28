% Patient Tester
% Adapted from Ali's version by Anna and Anna
% 06/24/2013
%% Initialize Workspace
clear; clc

%% End where we begin
STARTDIR = pwd;
%% Create Global Variables
global Partnum numtrial Partfile

%% Patient & Test info
display('Must input all information that is asked')

Partnum = input('Input the participant''s designation number as a 3 digit number:   ', 's');
while isempty(Partnum)
    Partnum = input('What is the participant number? \n \n','s');
end

Date = input('Input today''s date as shown below \n \n dd_mm_yy:   ', 's');
while isempty(Date)
    Date = input('What is today''s date? \n \n','s');
end

trialnum = input('Have you run this participant today already? (Y/N):    ','s');
while isempty(trialnum)
    trialnum = input('Have you run this participant today already? (Y/N):    ','s');
end
if strcmp(trialnum, 'Y') || strcmp(trialnum, 'y')
    numtrial = input('Input a number. How many times have you run this patient today?:   ');
    numtrial = numtrial+1;
    numtrial = num2str(numtrial);
else
    numtrial = num2str(1);
end

%% CREATE A DIRECTORY TO STORE PARTICIPANT DATA
Partfile = strcat('Participant',Partnum,'_',Date,'_',numtrial);
cd /data/pupil

if exist(Partfile,'dir') == 0
    mkdir(Partfile)
elseif exist(Partfile,'dir') == 7
    whatdo = input('This participant trial has already been run today! \n \n Would you like to continue? Y/N:    ','s');
    while isempty(whatdo)
        whatdo = input('Would you like to Continue this participant trial? Y/N:     ');
    end
    if strcmp(whatdo, 'N') ==1 || strcmp(whatdo,'no') == 1 || strcmp(whatdo,'NO') == 1 || strcmp(whatdo,'n') == 1 || strcmp(whatdo,'No') ==1
        break
    elseif strcmp(whatdo, 'Y') ==1 || strcmp(whatdo,'y') ==1 || strcmp(whatdo,'Yes')==1 || strcmp(whatdo,'YES') ==1 || strcmp(whatdo,'yes') ==1
        display('Remember that replacing a directory deletes all files in the directory forever')        
        decide = input('Would you like to replace the directory (R),\n \n would you like to make a new directory (N) \n\n or would you like to add to the current directory (A) \n\n =>','s');
        while isempty(decide)
            decide = input('type in replace (R), new (N), or add (A)');
        end
        if strcmp(decide,'R') == 1 || strcmp(decide,'r') == 1
            rmdir(Partfile, 's');
        elseif strcmp(decide,'N') || strcmp(decide,'n') == 1
            Partfile = strcat(Partfile,'_01');
            mkdir(Partfile)
        elseif strcmp(decide,'A') == 1 || strcmp(decide,'a') == 1
            cd(Partfile)
        end
    end
end

cd(STARTDIR)
display('Created a directory in which all data will be saved')
display('Ready to Calibrate and run tests')
pause(2)
%% CALIBRATE TOBII FOR THIS PARTICIPANT
display('It is necessary to calibrate for a new patient every new session')
display('It is recommended (not necessary to recalibrate for each set of trials')
display('')
CALB = input('Do you need to calibrate for this patient? (Y/N):   ', 's');

if strcmp(CALB,'N') == 1 || strcmp(CALB,'n') == 1
    display('Okay Moving on')
elseif strcmp(CALB,'Y') ==1 || strcmp(CALB, 'y') ==1
    display('Press any key to Calibrate')
    pause
    %%% Connect ot Racker %%%%
    tetio_CONNECT;
    %%% Position eyes in front of tracker %%%
    addpath('/Applications/tobiiSDK/matlab/EyeTrackingSample/functions');
    addpath('/Applications/tobiiSDK/matlab//tetio');  
    addpath('/matlab/pupil');
    
    SetCalibParams;
    TrackStatus;
    %%% Calibrate %%%
    tetio_swirlCalibrate
end

%% RUN TESTS
%% LIGHT TEST
TrackStatus;
RUNLT = input('Would you like to run light test? (Y/N):    ', 's');

if strcmp(RUNLT,'N') == 1 || strcmp(RUNLT,'n') == 1
    display('Okay Moving on')
elseif strcmp(RUNLT,'Y') ==1 || strcmp(RUNLT, 'y') ==1
    pause(2)
    tetio_testerlighttest
    display('Check to see if the data has been saved')
    display('Then press any key to continue')
    pause
    cd(STARTDIR)
end

%% DARK TEST
tetio_CONNECT;
TrackStatus;
RUNDT = input('Would you like to run dark test? (Y/N):    ', 's');

if strcmp(RUNDT,'N') ==1 || strcmp(RUNDT, 'n') ==1
    display('Okay Moving on')
else
    pause(2)
    work_tetio_testerdarktest
    display('Check to see if the data has been saved')
    display('Then press any key to continue')
    pause
    cd(STARTDIR)
end

%% Reversal Learning
tetio_CONNECT
TrackStatus;
RUNRL = input('Would you like to run Reversal Learning? (Y/N):    ', 's');
if strcmp(RUNRL,'N') ==1 || strcmp(RUNRL, 'n') ==1
    display('Okay Moving on')
else
    pause(2)
    tetio_reversallearningfcn
    display('Check to see if the data has been saved')
    display('Then press any key to continue')
    pause(5)
    cd(STARTDIR)
end

%% DONE
display('FINISHED')


%% Wrap up participant
cd(STARTDIR)
%clc
%DISCONNECT
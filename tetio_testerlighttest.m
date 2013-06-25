%
% TesterdarkTest Modified with SDK Language
%

%task code to perform a test of the pupillary dark reflex
%cycle between blank and full white

clc 
clear all
close all



%%%%%%%% PTB preliminaries %%%%%%%%%%%%%
warning('off','MATLAB:dispatcher:InexactMatch');
Screen('Preference', 'SkipSyncTests',2); %disables all testing -- use only if ms timing is not at all an issue
Screen('Preference','VisualDebugLevel', 0);
Screen('Preference', 'SuppressAllWarnings', 1);
Screen('CloseAll')

%% Create Global Variables
global Partnum numtrial Partfile

datadoc = strcat(Partnum,'darktest_',numtrial); 
default_data = strcat(datadoc,'_data');
default_events = strcat(datadoc,'_events');
datafile = strcat('/data/pupil/',Partfile);

try
    try
        cd(datafile)
    catch
        mkdir(datafile)
        cd(datafile)
    end
    addpath('/matlab/pupil/code/TESTER')
end

%dlmwrite('default',zero(4),'\t') % MY ATTEMPT TO SOLVE THE SAVE FILE Problem

%%%%%%%% setup parameters %%%%%%%%%%%%%%
%what are the RGB triples to flash onscreen for the test?
%[0 0 0] = black; [255 255 255] = white


%%% Connect to Eye Tracker %%%
tetio_CONNECT;

addpath('/Applications/tobiiSDK/matlab/EyeTrackingSample');
addpath('/Applications/tobiiSDK/matlab/EyeTrackingSample/functions');
addpath('/Applications/tobiiSDK/matlab//tetio');  
addpath('/matlab/pupil');

%%% Position eyes in front of eye tracker %%%
%etCalibParams;
%TrackStatus;

%%% Calibrate %%%
%tetio_swirlCalibrate;

stim_col=255 *[ [0.25 0.25 0.25] ;
              [0.5 0.5 0.5];
              [0.75 0.75 0.75];
              [1 1 1] ] ;
stim_dur = [0.2 0.2 0.2 0.2]; %duration of flash (in s)
habituation_dur = 10; %habituation time (in s) before first flash
recover_dur = [8 8 8 8]; %recovery time post-flash (in s)

numtrials=size(stim_col,1);

% light_dur = 2; %duration of light stimulus (in s)
% dark_dur = 0.2; %duration of dark stimulus (in s)

which_screen=1;
[win, screenRect] = Screen('OpenWindow',which_screen,[0 0 0],[],32);
horz = screenRect(3);
vert = screenRect(4);

%%%%%%%% countdown to begin test %%%%%%%%%
for (i = 1:4);
    
    when = GetSecs + 1;
    
  % PRESENT STARTING Screen
    BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
    if i == 4
       txt = ''; 
    else
        txt = num2str(4-i);
    end
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, txt, floor(horz/2), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, win);
    flipTime = Screen('Flip', win, when);
end


% *************************************************************************
%
% Start tracking and plot the gaze data read from the tracker.
%
% *************************************************************************



leftEyeAll_light = [];
rightEyeAll_light = [];
timeStampAll_light = [];

for ind=1:numtrials
    
    tetio_startTracking;
    
    WaitSecs(2)
    %paint light stimulus onscreen
    Screen('FillRect',win,stim_col(ind,:),[]);
    Screen('Flip',win);
    
    %Record Time of Stim. Onset
    %StimOnSet(ind)=GetSecs;
    %not sure about the syncing of time so alternatively:
    StimOnSet(ind)=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
    
    %wait the duration of the stimulus
    WaitSecs(stim_dur(ind));
    
    
    %clear stimulus
    Screen('FillRect',win,[0 0 0]);
    Screen('Flip',win);
   
    %Record Time Stimulus goes off
    %StimOff(ind)=GetSecs;
    StimOff(ind)=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
    
    
    %wait recovery time
    WaitSecs(recover_dur(ind));
    
   [lefteye, righteye, timestamp, trigSignal] = tetio_readGazeData;
   
    numGazeData = size(lefteye, 2);
    leftEyeAll_light = vertcat(leftEyeAll_light, lefteye(:, 1:numGazeData));
    rightEyeAll_light = vertcat(rightEyeAll_light, righteye(:, 1:numGazeData));
    timeStampAll_light = vertcat(timeStampAll_light, timestamp(:,1));

    tetio_stopTracking;
    
end

%%% Close Tobii Connection %%%
tetio_disconnectTracker; 
tetio_cleanUp;

%DisplayData(leftEyeAll, rightEyeAll );

% % Save gaze data vectors to file here using e.g:



disp('Program finished.');
clear Screen;


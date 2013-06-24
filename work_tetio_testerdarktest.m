%
% TesterdarkTest Modified with SDK Language
%

%task code to perform a test of the pupillary dark reflex
%cycle between blank and full white

clc 
clear all
close all

addpath('/Applications/tobiiSDK/matlab/EyeTrackingSample/functions');
addpath('/Applications/tobiiSDK/matlab//tetio');  
addpath('/matlab/pupil');

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

numcycles = 5; %number of light/dark cycles
flash_dur = 1; %duration of the stimulus flash in secondsreturn

dark_stim = zeros(numcycles,3);

light_stim = 255*ones(1,3);

stim_dur = flash_dur * ones(numcycles,1); %duration of dark flash (in s)

% light_dur = 2; %duration of light stimulus (in s)
% dark_dur = 0.2; %duration of dark stimulus (in s)

habituation_dur = 10; %habituation time (in s) before first flash
recover_dur = 8*ones(numcycles,1); %(in s) after first flash

%%% Connect to Tobii %%%

tetio_CONNECT;

which_screen=1;
[win, screenRect] = Screen('OpenWindow',which_screen,[0 0 0],[],32);
horz = screenRect(3);
vert = screenRect(4);

%%%%%%%% countdown to begin test %%%%%%%%%
for (i = 1:4);
    
    when = GetSecs + 1;
    
  % PRESENT STARTING Screen
  

%open window, blank screen
    BlankScreen = Screen('OpenOffScreenwindow', win,[255 255 255]);
    if i == 4
       txt = ''; 
    else
        txt = num2str(4-i);
    end
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, txt, floor(horz/2), floor(vert/2), [0 0 0], [255 255 255], 1);
    Screen('CopyWindow', BlankScreen, win);
    flipTime = Screen('Flip', win, when);
end


% *************************************************************************
%
% Start tracking and plot the gaze data read from the tracker.
%
% *************************************************************************

%tetio_startTracking;

% leftEyeAll = [];
% rightEyeAll = [];
% timeStampAll = [];

for ind=1:numcycles
    
    tetio_startTracking;
    
    WaitSecs(2)
    %paint light stimulus onscreen
    Screen('FillRect',win,dark_stim(ind,:),[]);
    Screen('Flip',win);
    
    %Record Time of Stim. Onset
    StimOnSet(ind)=GetSecs;
    
    %wait the duration of the stimulus
    WaitSecs(stim_dur(ind));
    
    
    %clear stimulus
    Screen('FillRect',win,light_stim);
    Screen('Flip',win);
   
    %Record Time Stimulus goes off
    StimOff(ind)=GetSecs;
    
    %wait recovery time
    WaitSecs(recover_dur(ind));
    
    GazeDataPerTrial=tetio_readGazeData;
    
    tetio_stopTracking;
    
end
    
%[leftEyeAll, rightEyeAll, timeStampAll] = DataCollect(5, 0.4);

%tetio_stopTracking; 
tetio_disconnectTracker; 
tetio_cleanUp;

%DisplayData(leftEyeAll, rightEyeAll );

% % Save gaze data vectors to file here using e.g:



disp('Program finished.');
clear Screen;


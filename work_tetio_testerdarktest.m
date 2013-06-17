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




%%%%%%%% countdown to begin test %%%%%%%%%
for (i = 1:4);
    
    when = GetSecs + 1;
    
    % PRESENT STARTING Screen
    BlankScreen = Screen('OpenOffScreenwindow', window,[255 255 255]);
    if i == 4
       txt = ''; 
    else
        txt = num2str(4-i);
    end
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, txt, floor(horz/2), floor(vert/2), [0 0 0], [255 255 255], 1);
    Screen('CopyWindow', BlankScreen, window);
    flipTime = Screen('Flip', window, when);
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
    Screen('FillRect',window,dark_stim(ind,:),[]);
    Screen('Flip',window);
    
    
    %wait the duration of the stimulus
    WaitSecs(stim_dur(ind));
    
    %clear stimulus
    Screen('FillRect',window,light_stim);
    Screen('Flip',window);
   
    
    %wait recovery time
    WaitSecs(recover_dur(ind));
    
    tetio_stopTracking;
    
    z=tetio_readGazeData;
end
    
%[leftEyeAll, rightEyeAll, timeStampAll] = DataCollect(5, 0.4);

%tetio_stopTracking; 
tetio_disconnectTracker; 
tetio_cleanUp;

%DisplayData(leftEyeAll, rightEyeAll );

% % Save gaze data vectors to file here using e.g:
csvwrite('gazedataleft.csv', z);


disp('Program finished.');
clear Screen;


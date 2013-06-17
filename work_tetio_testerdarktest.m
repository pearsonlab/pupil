%
% TesterdarkTest Modified with SDK Language
%

clc 
clear all
close all

addpath('/Applications/tobiiSDK/matlab/EyeTrackingSample/functions');
addpath('/Applications/tobiiSDK/matlab//tetio');  
addpath('/matlab/pupil');

tetio_CONNECT;

tetio_CALIBRATE_EyeTrackingSample;

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



% Do we need to synchronize clocks? We need some way to record. 

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


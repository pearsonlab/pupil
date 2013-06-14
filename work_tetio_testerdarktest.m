%
% EyeTrackingSample
%

clc 
clear all
close all

addpath('/Applications/tobiiSDK/matlab/EyeTrackingSample/functions');
addpath('/Applications/tobiiSDK/matlab//tetio');  
addpath('/matlab/pupil');

% *************************************************************************
%
% Initialization and connection to the Tobii Eye-tracker
%
% *************************************************************************
 
disp('Initializing tetio...');
tetio_init();

% Set to tracker ID to the product ID of the tracker you want to connect to.
trackerId = 'TT060-301-14200895';

%   FUNCTION "SEARCH FOR TRACKERS" IF NOTSET
if (strcmp(trackerId, 'NOTSET'))
	warning('tetio_matlab:EyeTracking', 'Variable trackerId has not been set.'); 
	disp('Browsing for trackers...');

	trackerinfo = tetio_getTrackers();
	for i = 1:size(trackerinfo,2)
		disp(trackerinfo(i).ProductId);
	end

	tetio_cleanUp();
	error('Error: the variable trackerId has not been set. Edit the EyeTrackingSample.m script and replace "NOTSET" with your tracker id (should be in the list above) before running this script again.');
end

fprintf('Connecting to tracker "%s"...\n', trackerId);
tetio_connectTracker(trackerId)
	
currentFrameRate = tetio_getFrameRate;
fprintf('Frame rate: %d Hz.\n', currentFrameRate);





% *************************************************************************
%
% Calibration of a participant
%
% *************************************************************************

global Calib

screensize = get(0,'Screensize');
Calib.mondims1.x = screensize(1);
Calib.mondims1.y = screensize(2);
Calib.mondims1.width = screensize(3);
Calib.mondims1.height = screensize(4);

Calib.MainMonid = 1; 
Calib.TestMonid = 1;

Calib.points.x = [0.1 0.9 0.5 0.9 0.1];  % X coordinates in [0,1] coordinate system 
Calib.points.y = [0.1 0.1 0.5 0.9 0.9];  % Y coordinates in [0,1] coordinate system 
Calib.points.n = size(Calib.points.x, 2); % Number of calibration points
Calib.bkcolor = [0.85 0.85 0.85]; % background color used in calibration process
Calib.fgcolor = [0 0 1]; % (Foreground) color used in calibration process
Calib.fgcolor2 = [1 0 0]; % Color used in calibratino process when a second foreground color is used (Calibration dot)
Calib.BigMark = 25; % the big marker 
Calib.TrackStat = 25; % 
Calib.SmallMark = 7; % the small marker
Calib.delta = 200; % Moving speed from point a to point b
Calib.resize = 1; % To show a smaller window
Calib.NewLocation = get(gcf,'position');




disp('Starting TrackStatus');
% Display the track status window showing the participant's eyes (to position the participant).
tetio_TrackStatus; % Track status window will stay open until user key press.
disp('TrackStatus stopped');


%
% Display a stimulus 
%
% For the demo this simply reads and display an image.
% Any method for generation and display of stimuli availble to Matlab could
% be inserted here, for example using Psychtoolbox or Cogent. 
%
% *************************************************************************

numcycles = 2; %number of light/dark cycles
flash_dur = 1; %duration of the stimulus flash in secondsreturn

dark_stim = zeros(numcycles,3);

light_stim = 255*ones(1,3);

stim_dur = flash_dur * ones(numcycles,1); %duration of dark flash (in s)

% light_dur = 2; %duration of light stimulus (in s)
% dark_dur = 0.2; %duration of dark stimulus (in s)

habituation_dur = 10; %habituation time (in s) before first flash
recover_dur = 8*ones(numcycles,1); %(in s) after first flash

openwins=Screen('Windows');

if isempty(openwins)
    warning('off','MATLAB:dispatcher:InexactMatch');
    Screen('Preference', 'SkipSyncTests',2); %disables all testing -- use only if ms timing is not at all an issue
    Screen('Preference','VisualDebugLevel', 0);
    Screen('Preference', 'SuppressAllWarnings', 1);
    Screen('CloseAll')
    
    HideCursor; % turn off mouse cursor
    
    
    %which screen do we display to?
    which_screen=1;
    
    %open window, blank screen
    [window, screenRect] = Screen('OpenWindow',which_screen,[255, 255, 255],[],32);
    
else
    %blank the already open window
    window=openwins(1);
    Screen('FillRect',window,[255, 255, 255]); 
    Screen('Flip',window); 
end
horz = screenRect(3);
vert = screenRect(4);


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


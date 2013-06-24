function testerlighttest(varargin)
%task code to perform a test of the pupillary light reflex
%blank screen, flash screen, wait, repeat
%% Create Global Variables
global Partnum numtrial Partfile
%%
datadoc = strcat(Partnum,'_lighttest_',numtrial);
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
 
    
%%% Connect to Eye Tracker %%%
tetio_CONNECT;

%%% Position eyes in front of eye tracker %%%
SetCalibParams;
TrackStatus;

%%% Calibrate %%%
tetio_swirlCalibrate;
    
% dlmwrite('default',zero(4),'\t')
%%%%%%%% setup parameters %%%%%%%%%%%%%%
% what are the RGB triples to flash onscreen for the test?
% [0 0 0] = black; [255 255 255] = white
% NB: Bradshaw papers use a green LED, not white

stim_col=255 *[ [0.25 0.25 0.25] ;
              [0.5 0.5 0.5];
              [0.75 0.75 0.75];
              [1 1 1] ] ;
stim_dur = [0.2 0.2 0.2 0.2]; %duration of flash (in s)
habituation_dur = 10; %habituation time (in s) before first flash
recover_dur = [8 8 8 8]; %recovery time post-flash (in s)

numtrials=size(stim_col,1);

%%%%%%%% PTB preliminaries %%%%%%%%%%%%%

% Calibrate %
tetio_swirlCalibrate;

which_screen=1;
[window, screenRect] = Screen('OpenWindow',which_screen,[0 0 0],[],32);
horz = screenRect(3);
vert = screenRect(4);

%%%%%%%% countdown to start task %%%%%%%%
for (i = 1:4);
    
    when = GetSecs + 1;
    
    % PRESENT STARTING Screen
    BlankScreen = Screen('OpenOffScreenwindow', window,[0 0 0]);
    if i == 4
       txt = ''; 
    else
        txt = num2str(4-i);
    end
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, txt, floor(horz/2), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, window);
    flipTime = Screen('Flip', window, when);
end

%%%%%%%% start the task %%%%%%%%%%%%%%%%%

% Habituate to darkness
WaitSecs(habituation_dur);

for ind=1:numcycles
    
    tetio_startTracking;
    
    WaitSecs(0.5);
    timertrialstart(ind) = GetSecs %%% ???
    
    %paint stimulus onscreen
    Screen('FillRect',window,stim_col(ind,:),[]);
    Screen('Flip',window);
    
    %Record Time of Stim. Onset
    StimOnSet(ind)=GetSecs;
    
    %wait the duration of the stimulus
    WaitSecs(stim_dur(ind));
    
    %clear stimulus
    Screen('FillRect',window,[0 0 0]);
    Screen('Flip',window);
    
    %Record Time Stimulus goes off
    StimOff(ind)=GetSecs;
   
    %wait recovery time
    WaitSecs(recover_dur(ind));
    
    tetio_stopTracking;
    
    tetio_readGazeData;
end

% % Save gaze data vectors to file here using e.g:
%csvwrite('gazedataleft.csv', pupilgazedata);

%%% Close Tobii connection %%%
tetio_disconnectTracker; 
tetio_cleanUp;

disp('Program finished.');
clear Screen;

tstatus

Screen('CloseAll')

catch q
    ShowCursor
    sca
    keyboard
end

%% Chose where to end up

%cd(startdir) % Directory we started in
cd(datafile) % Directory in which we save light test data

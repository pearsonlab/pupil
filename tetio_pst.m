function pst(varargin)
%task code to perform the pupillary sleep test
%basically, blank screen and wait
addpath('/Applications/tobiiSDK/matlab/EyeTrackingSample');
addpath('/Applications/tobiiSDK/matlab/EyeTrackingSample/functions');
addpath('/Applications/tobiiSDK/matlab//tetio');  
addpath('/matlab/pupil');

tetio_CONNECT;

startdir = pwd;

try
    try
        cd('/data/pupil')
    catch
        mkdir('/data/pupil')
        cd('/data/pupil')
    end
    addpath('/matlab/pupil/code')

%%%%%%%% setup parameters %%%%%%%%%%%%%%
trial_dur= 10; %duration of test (in s)
habituation_dur = 10; %(in s)

cont = 1;
while (cont == 1)
    tt= input('enter "L" to run lightexposure pupil test or "D" to run dark pst\n','s');
    if ( strcmpi(tt,'L') || strcmpi(tt,'l') )
        cont = 0; trial_disp = [255, 255, 255]; screen_disp = [0,0,0];
    elseif ( strcmpi(tt,'D') || strcmpi(tt,'d') )
        cont = 0; trial_disp = [0, 0, 0]; screen_disp = [255,255,255];
    end
    
end

%%%%%%%% PTB preliminaries %%%%%%%%%%%%%
%check for open windows
openwins=Screen('Windows');

if isempty(openwins)
    warning('off','MATLAB:dispatcher:InexactMatch');
    Screen('Preference', 'SkipSyncTests',2); %disables all testing -- use only if ms timing is not at all an issue
    Screen('Preference','VisualDebugLevel', 0);
    Screen('Preference', 'SuppressAllWarnings', 1);
    Screen('CloseAll')
    %HideCursor; % turn off mouse cursor
    
    %which screen do we display to?
    which_screen=1;
    
    %open window, blank screen
    [window, screenRect] = Screen('OpenWindow',which_screen,screen_disp,[],32);
    
    else
    %blank the already open window
    window=openwins(1);
    Screen('FillRect',window,screen_disp); 
    Screen('Flip',window); 
end
%%%%%%%% communicate with Tobii %%%%%%%%%

% CHECK FOR TOBII CONNECTION

%%%%%%%% start the task %%%%%%%%%%%%%%%%%

% No countdown? 

numcycles=2

%wait to habituate to start screen
WaitSecs(habituation_dur);

for ind=1:numcycles
    
    tetio_startTracking;
    
    WaitSecs(2)
    %paint stimulus onscreen
    Screen('FillRect',window,trial_disp,[]);
    Screen('Flip',window);
    
    %Record Time of Stim. Onset
    StimOnSet_pst(ind)=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
    
    %wait the duration of the stimulus
    WaitSecs(trial_dur);
    
     %clear stimulus
    Screen('FillRect',window,screen_disp,[]);
    Screen('Flip',window);
   
    %Record Time Stimulus goes off
    %StimOff(ind)=GetSecs;
    StimOff_pst(ind)=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
    
    %wait recovery time
    WaitSecs(recover_dur(ind));
    
   [lefteye, righteye, timestamp, trigSignal] = tetio_readGazeData;
   
    numGazeData = size(lefteye, 2);
    leftEyeAll_pst = vertcat(leftEyeAll_pst, lefteye(:, 1:numGazeData));
    rightEyeAll_pst = vertcat(rightEyeAll_pst, righteye(:, 1:numGazeData));
    timeStampAll_pst = vertcat(timeStampAll_pst, timestamp(:,1));

    tetio_stopTracking;
    
end

Screen('CloseAll')

catch q
    ShowCursor
    sca
    %keyboard
end

%% Chose where to end up

cd(startdir) % Directory we started in
%cd('/data/pupil') % Directory in which we save light test data

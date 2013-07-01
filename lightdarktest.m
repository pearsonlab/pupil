function lightdarktest(mode,outfile)
% code to perform light and dark test
% mode = 0 (dark test) or 1 (light test)
% saves data to outfile

PTBprelims

switch mode
    case 0
        task = 'darktest';
        numtrials = 3; %number of light/dark cycles
        habit_mat = 255 * ones(1,3); %habituate to full bright
        stim_mat = zeros(numtrials,3); %dark during stimulus
        rec_mat = 255*ones(numtrials,3); %full bright during recovery
        stim_time = 1; %duration of the dark in seconds
    case 1
        task = 'lighttest';
        stim_mat = 255 * [ [0.25 0.25 0.25] ; %bright during stimulus
            [0.5 0.5 0.5];
            [0.75 0.75 0.75];
            [1 1 1] ] ;
        numtrials=size(stim_mat,1);
        rec_mat = zeros(numtrials,3); %dark during recovery
        habit_mat = zeros(1,3); %habituate to full bright
        stim_time = 0.2;
end

habituation_dur = 10; %habituation time (in s) before first flash
recover_dur = 8*ones(1,numtrials); %recovery time post-flash (in s)
stim_dur = stim_time*ones(1,numtrials);  %duration of each stimulus (in s)

%display onscreen countdown
countdown

% *************************************************************************
%
% Start tracking and plot the gaze data read from the tracker.
%
% *************************************************************************

% leftEyeAll_light = [];
% rightEyeAll_light = [];
% timeStampAll_light = [];

%put on habituation stimulus
Screen('FillRect',win,habit_mat,[]);
Screen('Flip',win);
WaitSecs(habituation_dur);

for ind=1:numtrials
    
    tetio_startTracking;
    
    WaitSecs(2)
    
    %paint light stimulus onscreen
    Screen('FillRect',win,stim_mat(ind,:),[]);
    Screen('Flip',win);
    
    %Record Time of Stim. Onset
    %StimOnSet(ind)=GetSecs;
    %not sure about the syncing of time so alternatively:
    data(ind).ontime=tetio_localToRemoteTime(tetio_localTimeNow());
    
    %wait the duration of the stimulus
    WaitSecs(stim_dur(ind));
    
    %clear stimulus
    Screen('FillRect',win,rec_mat(ind,:));
    Screen('Flip',win);
   
    %Record Time Stimulus goes off
    %StimOff(ind)=GetSecs;
    data(ind).offtime=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
    
    %wait recovery time
    WaitSecs(recover_dur(ind));
    
    %read eye data
    data(ind).gazedata = tetio_readGazeData;
    
%     [lefteye, righteye, timestamp, trigSignal] = tetio_readGazeData;
%    
%     numGazeData = size(lefteye, 2);
%     leftEyeAll_light = vertcat(leftEyeAll_light, lefteye(:, 1:numGazeData));
%     rightEyeAll_light = vertcat(rightEyeAll_light, righteye(:, 1:numGazeData));
%     timeStampAll_light = vertcat(timeStampAll_light, timestamp(:,1));

    tetio_stopTracking;
    
    %%%% save data each trial %%%%%%
    save(outfile,'data','task')
    
end



%tetio_cleanUp; %%%% are we sure we need to do this?

% return the screen to dark
Screen('FillRect',win,[0 0 0],[]);
Screen('Flip',win);

disp('Program finished.');


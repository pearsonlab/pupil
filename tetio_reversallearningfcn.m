function reversallearningfcn(outfile)
% code to perform reversal learning test
% saves data to outfile

%% Set up data files
global Partnum numtrial Partfile trialvec

%% Unify Key Names
%KbCheck('UnifyKeyNames') 
KbName('UnifyKeyNames') %keynames will match those on Mac OS-X operating sys
stopkey=KbName('escape');
Rkey=KbName('rightarrow');
Lkey=KbName('leftarrow');

%%%%%%%% PTB preliminaries %%%%%%%%%%%%%
PTBprelims

% datadoc = strcat(Partnum,'revlearn',numtrial);
% default_data = strcat(datadoc,'_data');
% default_events = strcat(datadoc,'_events');
% datafile = strcat('/data/pupil/',Partfile);
% 
%     try
%         cd(datafile)
%     catch
%         mkdir(datafile)
%         cd(datafile)
%     end
%     addpath('/matlab/pupil/code/TESTER')
%     

%check for open windows
openwins=Screen('Windows');

%which screen do we display to?
which_screen=1;

%open window, blank screen
    [window, screenRect] = Screen('OpenWindow',which_screen,[0, 0, 0],[],32);
else
    %blank the already open window
    window=openwins(1);
    Screen('FillRect',window,[255, 255, 255]); 
    Screen('Flip',window);
    which_screen = 1;
    [window, screenRect] = Screen('OpenWindow',which_screen,[0, 0, 0],[],32);
end
horz = screenRect(3);
vert = screenRect(4);
    
% InitializeMatlabOpenGL([],[],1);
%ListenChar(2); %keeps keyboard input from going to Matlab window


%%%%%%%%%%%%%% Sound Parameters %%%%%%%%%%%%%
setup_audio
[popsnd,popF]=wavread('pop.wav');
[cashsnd,cashF]=wavread('cash.wav');

%create task vectors
revsightsound

% Trial vec is a row vector of 1's and 0's. Flag trial # in trialvec at which it switches between%
trialchange = find(diff(trialvec)~=0)+1;


%%%%%%%% countdown to start task %%%%%%%%
countdown

%%%%%%%% Start the Task %%%%%%%%%%%%%%%%%%%%%

%%%Recording prelims.

leftEyeAll_rl = [];
rightEyeAll_rl = [];
timeStampAll_rl = [];

WaitSecs(0.5);

pressvec = zeros(1, length(trialvec));
for ind = 1:length(trialvec)
    
    tetio_startTracking;
    timertrialstart(ind) = uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
    
    % paint on screen stimulus
    Screen('FillOval',window,[0 100 30], [horz*.25, vert*.15, horz*.75, vert*.75]) %balloon
    Screen('Flip', window);
    
    
    % Wait for response
    press = 0;
    while press == 0
        [secs, KeyCode] = KbWait([], 3);
    if (find(KeyCode)==79)%they chose right
        presstime(ind)=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
        pressvec(ind) = 0;
        press = 1;
    elseif (find(KeyCode)==80) %they chose left
        presstime(ind)=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
	    pressvec(ind) = 1;
        press =2;
    elseif find(KeyCode)==41 %they chose esc to bail out
        presstime(ind)=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
	    pressvec(ind) = 2;
        press = 3;
	    %Screen('Closeall')
	    return
    end
    end
    
    
    if pressvec(ind) == trialvec(ind);
        PsychPortAudio('DeleteBuffer');
        PsychPortAudio('FillBuffer',pahandle,cashsnd');
        PsychPortAudio('SetLoop',pahandle);
        PsychPortAudio('Start',pahandle);
        soundtime(ind)=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
    %tell that cashsound happened
        sndplay(ind) = 1 % Record 'cash'
    elseif pressvec(ind) ~= trialvec(ind)
        PsychPortAudio('DeleteBuffer')
        PsychPortAudio('FillBuffer',pahandle,popsnd');
        PsychPortAudio('SetLoop',pahandle);
        PsychPortAudio('Start',pahandle);
        soundtime(ind)=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
      % tell that pop happened
        sndplay(ind) = 2 % Record 'pop'
    end
    Screen('FillRect',window, [0 0 0]);
    Screen('Flip',window);
    WaitSecs(0.5);
    tetio_stopTracking;
    %%recording
    [lefteye, righteye, timestamp, trigSignal] = tetio_readGazeData;
   
    numGazeData = size(lefteye, 2);
    leftEyeAll_rl = vertcat(leftEyeAll_rl, lefteye(:, 1:numGazeData));
    rightEyeAll_rl = vertcat(rightEyeAll_rl, righteye(:, 1:numGazeData));
    timeStampAll_rl = vertcat(timeStampAll_rl, timestamp(:,1));

   %%%% save data each trial %%%%%%
    data(ind).lefteye = lefteye;
    data(ind).righteye = righteye;
    data(ind).timestamp = timestamp;
    data(ind).trig = trigSignal;
    save(outfile,'data','task')
     
end

reversalmat = [soundtime' presstime'];

%%% Save Data to File %%%


%end

catch q
     ShowCursor
     sca
     keyboard
 end
 
% return the screen to dark
Screen('FillRect',win,[0 0 0],[]);
Screen('Flip',win);

disp('Program finished.');
end

% %% Chose where to end up
% 
% %cd(startdir) % Directory we started in
% cd(datafile) % Directory in which we save light test data

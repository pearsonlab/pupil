function reversallearningfcn(outfile)
% code to perform reversal learning test
% saves data to outfile

%% Set up data files
global Partnum numtrial Partfile trialvec

%% Unify Key Names
 task = 'reversallearning'
KbName('UnifyKeyNames'); %keynames will match those on Mac OS-X operating sys


stopkey=KbName('escape');
Rkey=KbName('RightArrow');
Lkey=KbName('LeftArrow');

%%%%%%%% PTB preliminaries %%%%%%%%%%%%%
PTBprelims
try
%%%%%%%%%%%%%% Sound Parameters %%%%%%%%%%%%%
setup_audio
[popsnd,popF]=wavread('pop.wav');
[cashsnd,cashF]=wavread('cash.wav');

%create task vectors
revsightsound

% Trial vec is a row vector of 1's and 0's. Flag trial # in trialvec at which it switches between%
trialchange = find(diff(trialvec)~=0)+1;


%display onscreen countdown
countdown

%%%%%%%% Start the Task %%%%%%%%%%%%%%%%%%%%%


WaitSecs(0.5);
presstime=[];%%empty matrix
soundtime=[];

pressvec = zeros(1, length(trialvec));
for ind = 1:length(trialvec)
    
    tetio_startTracking;
    
    WaitSecs(2);
    
    timertrialstart(ind) = uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
    
    % paint on screen stimulus
    Screen('FillOval',win,[0 100 30], [horz*.25, vert*.15, horz*.75, vert*.75]) %balloon
    Screen('Flip', win);
    
    
    % Wait for response
    press = 0;
    while press == 0
        [secs, KeyCode] = KbWait(-1);
    if (find(KeyCode)==39)%they chose right
        data(ind).presstime=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
        pressvec(ind) = 0;
        press = 1;
    elseif (find(KeyCode)==37) %they chose left
        data(ind).presstime=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
	    pressvec(ind) = 1;
        press =2;
    elseif find(KeyCode)==41 %they chose esc to bail out
        data(ind).presstime=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
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
        data(ind).soundtime=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
    %tell that cashsound happened
        sndplay(ind) = 1 % Record 'cash'
    elseif pressvec(ind) ~= trialvec(ind)
        PsychPortAudio('DeleteBuffer')
        PsychPortAudio('FillBuffer',pahandle,popsnd');
        PsychPortAudio('SetLoop',pahandle);
        PsychPortAudio('Start',pahandle);
        data(ind).soundtime=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
      % tell that pop happened
        sndplay(ind) = 2 % Record 'pop'
    end
    
    %blank screen between each key press
    Screen('FillRect',win, [0 0 0]);
    Screen('Flip',win);
    WaitSecs(0.5);
    
    tetio_stopTracking;
    
    %read eye data
    [lefteye, righteye, timestamp, trigSignal] = tetio_readGazeData;
   
%     numGazeData = size(lefteye, 2);
%     leftEyeAll_rl = vertcat(leftEyeAll_rl, lefteye(:, 1:numGazeData));
%     rightEyeAll_rl = vertcat(rightEyeAll_rl, righteye(:, 1:numGazeData));
%     timeStampAll_rl = vertcat(timeStampAll_rl, timestamp(:,1));

   %%%% save data each trial %%%%%%
    data(ind).lefteye = lefteye;
    data(ind).righteye = righteye;
    data(ind).timestamp = timestamp;
    data(ind).trig = trigSignal;
    data(ind).presstime = presstime;
    data(ind).soundtime = soundtime;
    save(outfile,'data','task')
     
end

% reversalmat = [soundtime' presstime'];

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

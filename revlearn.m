function revlearn(outfile,flag,varargin)
% code to perform reversal learning test
% saves data to outfile
% flag = 0 for generating a new set of switches; if so, varargin has two
% arguments, the number of contingency switches and the minimum and maximum 
% numbers of trials between switches
% flag = 1 loads data from a file (name given in varargin)

% default values if flag not specified
if ~exist('flag','var')
    flag = 0;
    nswitch = 4;
    minrun = 3;
    maxrun = 6;
    seed = 12345;
    
else
    % set up switches when flag is specified
    switch flag
        case 0
            nswitch = varargin{1};
            minrun = varargin{2};
            maxrun = varargin{3};
            if length(varargin) > 3
                seed = varargin{4};
            else
                seed = GetSecs;
            end
            trialvec = makeswitches(nswitch,minrun,maxrun,seed);
        case 1
            dat = load(varargin{1});
            trialvec = dat.trialvec;
    end
    
end

% Unify Key Names
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

% display instructions
instructions = {['For this task, press the left or right key \n' ...
    'when the cross appears onscreen.\n' ...
    'You must learn by trial and error which is correct. \n\n' ...
    '(Press any key to continue)']};
display_instructions(win, instructions);

% Sound samples
txt = {'You will hear this for correct responses.'};
playsound(pahandle, cashsnd)
display_instructions(win,txt);
txt = {'And this for incorrect responses.'};
playsound(pahandle, popsnd);
display_instructions(win,txt);

%display onscreen countdown
countdown

%%%%%%%% Start the Task %%%%%%%%%%%%%%%%%%%%%

WaitSecs(0.5);
presstime=[];%%empty matrix
soundtime=[];

pressvec = zeros(1, length(trialvec));
for ind = 1:length(trialvec)
    
    tetio_startTracking;
    
    WaitSecs(.5);
    
    timertrialstart(ind) = uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
    
    % paint on screen stimulus
   txt1='+';
     Screen('TextSize', BlankScreen, 100);
    [nx, ny, bbox] = DrawFormattedText(win, txt1, 'center', 'center', [255 255 255]);
  Screen('FrameRect', win, 0, bbox)
    Screen('Flip',win);
    
    
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

   %%%% save data each trial %%%%%%
    data(ind).lefteye = lefteye;
    data(ind).righteye = righteye;
    data(ind).timestamp = timestamp;
    data(ind).trig = trigSignal;
    data(ind).presstime = presstime;
    data(ind).soundtime = soundtime;
    task = 'revlearn';
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

function revlearn(outfile,flag,varargin)
% code to perform reversal learning test
% saves data to outfile
% flag = 0 for generating a new set of switches; if so, varargin has two
% arguments, the number of contingency switches and the minimum and maximum 
% numbers of trials between switches
% flag = 1 loads data from a file (name given in varargin)

task = 'revlearn';

% default values if flag not specified
if ~exist('flag','var')
    nswitch = 4;
    minrun = 3;
    maxrun = 6;
    seed = 12345;
    trialvec = makeswitches(nswitch,minrun,maxrun,seed);
else
    % set up switches when flag is specified
    switch flag
        case 0
            nswitch=input('How many switches would you like?', 's');
            minrun=input('Minimum run?', 's');
            maxrun=input('Maximum run?', 's');
            seed = GetSecs;
            trialvec = makeswitches(nswitch,minrun,maxrun,seed);
        case 1
            dat = load(varargin{1});
            trialvec = dat.(varargin{2});
    end
    
end

% Unify Key Names
KbName('UnifyKeyNames'); %keynames will match those on Mac OS-X operating sys
Rkey=KbName('RightArrow');
Lkey=KbName('LeftArrow');
livekeys = [Lkey, Rkey];

%%%%%%%% PTB preliminaries %%%%%%%%%%%%%
PTBprelims

%%%%%%%%%%%%%% Sound Parameters %%%%%%%%%%%%%
setup_audio
[wrongsnd,buzzF]=wavread('buzz1.wav');
[rightsnd,dingF]=wavread('ding3.wav');

%%%%%%%%%%%%%% Task Parameters %%%%%%%%%%%%%
iti_mean = 3;
iti_range = 2;
pars.iti_mean = iti_mean;
pars.iti_range = iti_range;

%%%%%%%%%%%%%% Display Instructions %%%%%%%%%%%%%
instructions = {['Press the left or right key \n' ...
    'when the cross appears onscreen.\n' ...
    'You must learn by trial and error\n' ...
    'which is correct. \n\n' ...
    '(Press any key to continue)']};
display_instructions(win, instructions);

% Sound samples
txt = {'You will hear this for correct responses. \n (Press any key to continue)'};
playsound(pahandle, rightsnd);
display_instructions(win,txt);
txt = {'And this for incorrect responses. \n (Press any key to continue)'};
playsound(pahandle, wrongsnd);
display_instructions(win,txt);
txt = {'Please make a choice as soon as the "+" appears'; 'Press any key when ready.'};
display_instructions(win,txt);

%display onscreen countdown
countdown
ListenChar(2);

%%%%%%%% Start the Task %%%%%%%%%%%%%%%%%%%%%
tetio_startTracking;

WaitSecs(2); %give subjects a delay before first trial

for ind = 1:length(trialvec)
    %cue onset
    fixcross
    
    cuetime = tetio_localToRemoteTime(tetio_localTimeNow());
    
    % Wait for response
    [choice, ~] = handle_input(livekeys);
    presstime=tetio_localToRemoteTime(tetio_localTimeNow());
    
    % correct or incorrect?
    if (choice==Lkey && trialvec(ind) == 0) || (choice==Rkey && trialvec(ind) == 1)
        soundtime=tetio_localToRemoteTime(tetio_localTimeNow());
        playsound(pahandle,rightsnd);
        correct = 1;
    else
        soundtime=tetio_localToRemoteTime(tetio_localTimeNow());
        playsound(pahandle,wrongsnd);
        correct = 0;
    end
    
    WaitSecs(1); %outcome period
    
    % blank screen 
    Screen('FillRect',win, [0 0 0]);
    Screen('Flip',win);
    
    iti = iti_mean + iti_range*(2*rand-1);
    
    WaitSecs(iti);
    
    %%%% save data each trial %%%%%%
    data(ind).choice = choice;
    data(ind).correct = correct;
    data(ind).cuetime = cuetime;
    data(ind).presstime = presstime;
    data(ind).soundtime = soundtime;
    save(outfile,'data','task','pars')
     
end
tetio_stopTracking;

%read eye data
[lefteye, righteye, timestamp, trigSignal] = tetio_readGazeData;
eyedata.lefteye = lefteye;
eyedata.righteye = righteye;
eyedata.timestamp = timestamp;
eyedata.trig = trigSignal;

save(outfile,'data','eyedata','task','pars','trialvec')

shutdown_audio;
ListenChar(0);

% return the screen to dark
Screen('FillRect',win,[0 0 0],[]);
Screen('Flip',win);

disp('Program finished.');
end

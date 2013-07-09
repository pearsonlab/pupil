function oddball(outfile,flag,varargin)
% code to perform reversal learning test
% saves data to outfile
% flag = 0 for generating a new set of switches; if so, varargin has two
% arguments, the number of contingency switches and the minimum and maximum 
% numbers of trials between switches
% flag = 1 loads data from a file (name given in varargin)

task = 'oddball';

% default values if flag not specified
if ~exist('flag','var')
    nodd = 4;
    minrun = 3;
    maxrun = 6;
    seed = 12345;
    trialvec = makeoddballs(nodd,minrun,maxrun,seed);
else
    % set up switches when flag is specified
    switch flag
        case 0
            nodd=input('How many oddballs would you like?', 's');
            minrun=input('Minimum run?', 's');
            maxrun=input('Maximum run?', 's');
                seed = GetSecs;
            end
            trialvec = makeoddballs(nodd,minrun,maxrun,seed);
        case 1
            vectfile=input('Would you like four,five, or six oddballs?(you must type out the word right now)', 's');
            dat = load(varargin{1});
            trialvec = dat.(vectfile);
    end
    
end

% Unify Key Names
KbName('UnifyKeyNames'); %keynames will match those on Mac OS-X operating sys
Rkey=KbName('RightArrow');
Lkey=KbName('LeftArrow');
spacebar = KbName('space');
livekeys = [spacebar];

%%%%%%%% PTB preliminaries %%%%%%%%%%%%%
PTBprelims

%%%%%%%%%%%%%% Sound Parameters %%%%%%%%%%%%%
setup_audio
[lowsnd,lowF]=wavread('500.wav');
[highsnd,highF]=wavread('1000a.wav');

%%%%%%%%%%%%%% Task Parameters %%%%%%%%%%%%%
iti_mean = 3;
iti_range = 2;
pars.iti_mean = iti_mean;
pars.iti_range = iti_range;

%%%%%%%%%%%%%% Display Instructions %%%%%%%%%%%%%
instructions = {'In this task, you will listen to some sounds. \n Press any key to continue'};
display_instructions(win, instructions);

% Sound samples
txt = {'Some sounds are low...'};
playsound(pahandle, lowsnd);
display_instructions(win,txt);

txt = {'...and some are high.'};
playsound(pahandle, highsnd);
display_instructions(win,txt);

txt = {['When you hear a sound, press the space bar.\n\n' ...
    'Press any key when ready.']};
display_instructions(win,txt);

%display onscreen countdown
countdown    
    
%%%%%%%% Start the Task %%%%%%%%%%%%%%%%%%%%%
tetio_startTracking;

WaitSecs(2); %give subjects a delay before first trial
fixcross;
for ind=1:length(trialvec);
    
    %cue onset
    soundtime = tetio_localToRemoteTime(tetio_localTimeNow());
    if trialvec(ind)
        playsound(pahandle, highsnd);
    else
        playsound(pahandle, lowsnd);
    end
    
    % Wait for response
    handle_input(livekeys);
    presstime = tetio_localToRemoteTime(tetio_localTimeNow());
    
    iti = iti_mean + iti_range*(2*rand-1);
    
    WaitSecs(iti);
    
    %%%% save data each trial %%%%%%
    data(ind).soundtime = soundtime;
    data(ind).presstime = presstime;
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

% return the screen to dark
Screen('FillRect',win,[0 0 0],[]);
Screen('Flip',win);

disp('Program finished.');




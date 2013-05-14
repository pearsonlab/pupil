function reversallearningfcn(varargin)

DEBUG = 1;

%% Set up data files
global Partnum numtrial Partfile trialvec
%% Unify Key Names
%KbCheck('UnifyKeyNames') 
KbName('UnifyKeyNames') %keynames will match those on Mac OS-X operating sys
stopkey=KbName('escape');
Rkey=KbName('rightarrow');
Lkey=KbName('leftarrow');

while ~DEBUG
datadoc = strcat(Partnum,'revlearn',numtrial);
default_data = strcat(datadoc,'_data');
default_events = strcat(datadoc,'_events');
datafile = strcat('/data/pupil/',Partfile);
end
try
    if ~DEBUG
    try
        cd(datafile)
    catch
        mkdir(datafile)
        cd(datafile)
    end
    addpath('/matlab/pupil/code/TESTER')
    
%%PTB Settings (it tends to complain on PCs)
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
ListenChar(2); %keeps keyboard input from going to Matlab window
    end
%%%%%%%%%%%%%% Sound Parameters %%%%%%%%%%%%%
setup_audio
[popsnd,popF]=wavread('pop.wav');
[cashsnd,cashF]=wavread('cash.wav');
% cash = audioplayer(cashsnd, cashF);
% pops = audioplayer(popsnd, popF);

% %setup geometry
% setup_geometry

%create task vectors
reversallearning

%%%%%%%% communicate with Tobii %%%%%%%%%

%% CHECK FOR TOBII CONNECTION
if ~DEBUG
    need_to_connect=0;
    cond_res = check_status(2, 10, 1, 1); % check slot 2 (connected), wait 10 seconds max, in 1 sec intervals.
    tmp = find(cond_res==0, 1);
    if( ~isempty(tmp) )
        display('tobii not connected');
        need_to_connect=1;
    end
    if need_to_connect
        CONNECT %script to connect to tobii
    end

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
%%%%%%%% Start the Task %%%%%%%%%%%%%%%%%%%%%
talk2tobii('START_AUTO_SYNC')
talk2tobii('START_TRACKING'); %start recording eye data
WaitSecs(0.5);
[status,history]=talk2tobii('GET_STATUS');
if ~status(7)
    disp('Tracker can''t start')
    return
end

%start writing data to memory
%talk2tobii('RECORD');
%WaitSecs(0.5);

%record trial start
talk2tobii('EVENT','task start',0)
c = talk2tobii()
end
pressvec = zeros(1, length(trialvec));
for ind = 1:length(trialvec)
    if ~DEBUG
    talk2tobii('EVENT', 'trial_start', ind)
    timertrialstart(ind) = GetSecs;
    % paint on screen stimulus
    Screen('FillOval',window,[0 0 255], [horz*.25, vert*.25, horz*.75, vert*.75]) %balloon
    Screen('Flip', window)
    % tell tobii
    talk2tobii('EVENT', 'visual stim', ind)
    end
    % Wait for response
    press = 0;
    while press == 0
        [secs, KeyCode] = KbWait([], 3);
    if (find(KeyCode)==79)  %they chose right
        pressvec(ind) = 0;
        press = 1;
    elseif (find(KeyCode)==80) %they chose left
	    pressvec(ind) = 1;
        press =2;
    elseif find(KeyCode)==41 %they chose esc to bail out
	    pressvec(ind) = 2;
        press = 3;
	    %Screen('Closeall')
	    return
    end
    end
    %talk2tobii('EVENT', 'key press', ind)
    if pressvec(ind) == trialvec(ind)
        PsychPortAudio('DeleteBuffer')
        PsychPortAudio('FillBuffer',pahandle,cashsnd');
        PsychPortAudio('SetLoop',pahandle);
        PsychPortAudio('Start',pahandle);
        talk2tobii('EVENT', 'cashsound', ind)
        sndplay(ind) = 'cash'
    elseif pressvec(ind) ~= trialvec(ind)
        PsychPortAudio('DeleteBuffer')
        PsychPortAudio('FillBuffer',pahandle,popsnd');
        PsychPortAudio('SetLoop',pahandle);
        PsychPortAudio('Start',pahandle);
        talk2tobii('EVENT', 'popsound', ind)
        sndplay(ind) = 'pop'
    end
    if ~DEBUG
    WaitSecs(1)
    talk2tobii('EVENT', 'trial over', ind)
    c = talk2tobii()
    %savedata
    
    if ind == 1
        appstr = 'TRUNK';
    else
        appstr = 'APPEND';
    end
    talk2tobii('SAVE_DATA', default_data, default_events, appstr);
    talk2tobii('CLEAR_DATA') % flush buffer  
    end
end
save('default_data.mat', [pressvec, trialvec, sndplay])
talk2tobii('CLEAR_DATA') % flush buffer
WaitSecs(0.5);
%close tobii connection
talk2tobii('STOP_RECORD');
WaitSecs(0.5);
talk2tobii('STOP_TRACKING');
WaitSecs(0.5);
talk2tobii('STOP_AUTO_SYNC')
WaitSecs(0.5);
%talk2tobii('DISCONNECT');
%WaitSecs(0.5);
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

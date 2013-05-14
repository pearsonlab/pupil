function pst(varargin)
%task code to perform the pupillary sleep test
%basically, blank screen and wait
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
trial_dur= 30; %duration of test (in s)
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

%%%%%%%% start the task %%%%%%%%%%%%%%%%%
talk2tobii('START_TRACKING'); %start recording eye data
WaitSecs(0.5);
[status,history]=talk2tobii('GET_STATUS');
if ~status(7)
    disp('Tracker can''t start')
    return
end

%wait to habituate to start screen
WaitSecs(habituation_dur);

%start writing data to memory
talk2tobii('RECORD');
WaitSecs(0.5);

%record trial start
talk2tobii('EVENT','trial start')

%paint stimulus onscreen
Screen('FillRect',window,trial_disp,[]);
Screen('Flip',window);
%tell Tobii
talk2tobii('EVENT','stim on')

%wait the duration of the stimulus
WaitSecs(trial_dur);

 
%clear stimulus
Screen('FillRect',window,screen_disp,[]);
Screen('Flip',window);

%tell tobii
talk2tobii('EVENT','stim off')

%wait recovery time
WaitSecs(recover_dur(ind));

%tell tobii trial over
talk2tobii('EVENT','trial over')

%save data
if (ind==1)
    appstr='TRUNK';
else
    appstr='APPEND';
end

%talk2tobii('SAVE_DATA','default_data','default_events',appstr); %NEED TO HAVE A WAY TO SPECIFY FILENAME
talk2tobii('CLEAR_DATA') %flush buffer

%close tobii connection
talk2tobii('STOP_RECORD');
WaitSecs(0.5);
talk2tobii('STOP_TRACKING');
WaitSecs(0.5);
tstatus

Screen('CloseAll')

catch q
    ShowCursor
    sca
    %keyboard
end

%% Chose where to end up

cd(startdir) % Directory we started in
%cd('/data/pupil') % Directory in which we save light test data

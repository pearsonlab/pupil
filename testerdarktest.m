function testerdarktest(varargin)
%task code to perform a test of the pupillary dark reflex
%cycle between blank and full whitelslsls
%% Create Global Variables
global Partnum numtrial Partfile

datadoc = strcat(Partnum,'darktest_',numtrial);
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
    addpath('/matlab/pupil/code/TESTER')

%dlmwrite('default',zero(4),'\t') % MY ATTEMP TO SOLVE THE SAVE FILE Problem

%%%%%%%% setup parameters %%%%%%%%%%%%%%
%what are the RGB triples to flash onscreen for the test?
%[0 0 0] = black; [255 255 255] = white

numcycles = 5; %number of light/dark cycles
flash_dur = 1; %duration of the stimulus flash in secondsreturn

dark_stim = zeros(numcycles,3);

light_stim = 255*ones(1,3);

stim_dur = flash_dur * ones(numcycles,1); %duration of dark flash (in s)

% light_dur = 2; %duration of light stimulus (in s)
% dark_dur = 0.2; %duration of dark stimulus (in s)

habituation_dur = 10; %habituation time (in s) before first flash
recover_dur = 8*ones(numcycles,1); %(in s) after first flash


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
    [window, screenRect] = Screen('OpenWindow',which_screen,[255, 255, 255],[],32);
    
else
    %blank the already open window
    window=openwins(1);
    Screen('FillRect',window,[255, 255, 255]); 
    Screen('Flip',window); 
end
horz = screenRect(3);
vert = screenRect(4);

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

%%%%%%%% countdown to begin test %%%%%%%%%
for (i = 1:4);
    
    when = GetSecs + 1;
    
    % PRESENT STARTING Screen
    BlankScreen = Screen('OpenOffScreenwindow', window,[255 255 255]);
    if i == 4
       txt = ''; 
    else
        txt = num2str(4-i);
    end
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, txt, floor(horz/2), floor(vert/2), [0 0 0], [255 255 255], 1);
    Screen('CopyWindow', BlankScreen, window);
    flipTime = Screen('Flip', window, when);
end

%%%%%%%% start the task %%%%%%%%%%%%%%%%%
talk2tobii('START_TRACKING'); %start recording eye data
WaitSecs(0.5);
[status,history]=talk2tobii('GET_STATUS');
if ~status(7)
    disp('Tracker can''t start')
    return
end


%wait to habituate to light
WaitSecs(habituation_dur);

%start writing data to memory
talk2tobii('RECORD');
WaitSecs(0.5);

%record trial start
talk2tobii('EVENT','task start',0)

for ind=1:numcycles
    %tell tobii trial starting
    talk2tobii('EVENT','trial start',ind)
    
    %paint light stimulus onscreen
    Screen('FillRect',window,dark_stim(ind,:),[]);
    Screen('Flip',window);
    %tell Tobii
    talk2tobii('EVENT','stim on',ind)
    
    %wait the duration of the stimulus
    WaitSecs(stim_dur(ind));
    
    %clear stimulus
    Screen('FillRect',window,light_stim);
    Screen('Flip',window);
    %tell tobii
    talk2tobii('EVENT','stim off',ind)
    
    %wait recovery time
    WaitSecs(recover_dur(ind));
    
    %tell tobii trial over
    talk2tobii('EVENT','trial over',ind)
    
    %save data
    if (ind==1)
        appstr='TRUNK';
    else
        appstr='APPEND';
    end
    talk2tobii('SAVE_DATA',default_data,default_events,appstr); %NEED TO HAVE A WAY TO SPECIFY FILENAME
    talk2tobii('CLEAR_DATA') %flush buffer
end

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

%cd(startdir) % Directory we started in
cd(datafile) % Directory in which we save light test data
   
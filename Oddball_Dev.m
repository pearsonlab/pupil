%% Oddball Task %%
% Plays tones in a constant stream, participant must detect presence of odd
% tone 

%%%IF YOU ARE DOING THIS TASK SEVERAL TIMES OVER, you can get the problem
%%%of an ever reducing number of trials, clear all if that problem comes
%%%up. 
%% Unify Key Names
%KbCheck('UnifyKeyNames') 
%KbName('UnifyKeyNames') %keynames will match those on Mac OS-X operating sys
stopkey=KbName('escape');
spacebar = KbName('space');

%%%%%%%% PTB preliminaries %%%%%%%%%%%%%
warning('off','MATLAB:dispatcher:InexactMatch');
Screen('Preference', 'SkipSyncTests',2); %disables all testing -- use only if ms timing is not at all an issue
Screen('Preference','VisualDebugLevel', 0);
Screen('Preference', 'SuppressAllWarnings', 1);
Screen('CloseAll')


%% Create Global Variables
global Partnum numtrial Partfile
datadoc = strcat(Partnum,'revlearn',numtrial);
default_data = strcat(datadoc,'_data');
default_events = strcat(datadoc,'_events');
datafile = strcat('/data/pupil/',Partfile);

    try
        cd(datafile)
    catch
        mkdir(datafile)
        cd(datafile)
    end
    addpath('/matlab/pupil/code/TESTER')
   

%%%% Sound Parameters %%%%

addpath('/Users/participant/desktop')
    
[lowsnd,lowF]=wavread('500hz.wav');
[highsnd,highF]=wavread('1000hz.wav');

InitializePsychSound()
pahandle=PsychPortAudio('Open',[],[],0,[],1);

ntrials = 10;
numhigh = ntrials/5;

cond_check=1;
ListenChar(2);
%for now a connection, take this out when Participant tester is complete
tetio_CONNECT;

while cond_check==1;
   %%%% Randomization %%%%
oddtrialvec = zeros(length(ntrials),1);
oddtrialvec(randperm(ntrials,numhigh),1)=1;
% Run Length Code %

checkgood=[([oddtrialvec(diff(oddtrialvec) ~= 0)' oddtrialvec(end)]') (diff([0 find(diff(oddtrialvec) ~= 0)' length(oddtrialvec)])')];

%%checks to see if the vector is nice
b=checkgood(:,1)==0 & checkgood(:,2)< 2; 
c=checkgood(:,1)==1 & checkgood(:,2) == 2 ;
if sum(b) || sum(c) > 0
    cond_check=1;
else
    cond_check=0;
end
      
end

oddtrialvec

%%% Start the Task %%%
which_screen=1;
[win, screenRect] = Screen('OpenWindow',which_screen,[0 0 0],[],32);
horz = screenRect(3);
vert = screenRect(4);

%%%%%%%%introduce sounds
BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
   text='This is an introduction.'
    
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, text, (floor(horz/2)-100), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, win);
    flipTime = Screen('Flip', win);
    pause(1.8)
      
  BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
   text='You will hear two sounds.'
    
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, text, (floor(horz/2)-100), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, win);
    flipTime = Screen('Flip', win);
    pause(1.8)
      
    
     BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
   text='One of the sounds is the oddball';
    
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, text, (floor(horz/2)-100), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, win);
    flipTime = Screen('Flip', win);
    pause(1.8)
    
    
    BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
   text='When the task begins press any key on the keyboard when you hear the oddball';
    
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, text, (floor(horz/2)-370), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, win);
    flipTime = Screen('Flip', win);
    pause(1.8)
    
    BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
      for (ze = 1:4);
    if mod(ze,2)==1;
    text2='this is the oddball sound'
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, text2, (floor(horz/2)-100), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, win);
    Screen('Flip', win, when);
    PsychPortAudio('DeleteBuffer')
    PsychPortAudio('FillBuffer', pahandle, highsnd');
    PsychPortAudio('SetLoop',pahandle);
    PsychPortAudio('Start',pahandle,1);
    pause(2)
    BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
    else
    PsychPortAudio('DeleteBuffer')
    PsychPortAudio('FillBuffer', pahandle, lowsnd');
    PsychPortAudio('SetLoop',pahandle);
    PsychPortAudio('Start',pahandle,1); 
    text2='this is the regular sound'
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, text2, (floor(horz/2)-100), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, win);
    Screen('Flip', win, when);
    pause(2)
    BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
    end
      end

BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
   text='The task will begin shortly';
    
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, text, (floor(horz/2)-200), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, win);
    flipTime = Screen('Flip', win);
    pause(3);
      
%%%%%%%% countdown to begin test %%%%%%%%%
for (i = 1:4);
    
    when = GetSecs + 1;
    
  % PRESENT STARTING Screen
    BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
    if i == 4
       txt = ''; 
    else
        txt = num2str(4-i);
    end
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, txt, floor(horz/2), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, win);
    flipTime = Screen('Flip', win, when);
end

txt1='+'
Screen('TextSize', BlankScreen, 50);
   Screen('DrawText', BlankScreen, txt1, floor(horz/2), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, win);
    flipTime = Screen('Flip', win, when);
   
    


leftEyeAll_odd = [];
rightEyeAll_odd = [];
timeStampAll_odd = [];
%%% Start the Task %%%

    
    
for i=1:length(oddtrialvec);
    tetio_startTracking;
    startSecs = tetio_localToRemoteTime(tetio_localTimeNow());
    tic;
    if oddtrialvec(i)==1;
    PsychPortAudio('DeleteBuffer')
    PsychPortAudio('FillBuffer', pahandle, highsnd');
    PsychPortAudio('SetLoop',pahandle);
    PsychPortAudio('Start',pahandle,1);
    sndtype_odd(i)=1;
    else
    PsychPortAudio('DeleteBuffer')
    PsychPortAudio('FillBuffer', pahandle, lowsnd');
    PsychPortAudio('SetLoop',pahandle);
    PsychPortAudio('Start',pahandle,1); 
    sndtype_odd(i)=2;
    end
    
    t = GetSecs;
    while GetSecs - t < 1.4;
        [keydown, secs]=KbCheck;
        if keydown ==1
            keyhit(i)=[tetio_localToRemoteTime(int64(secs))];
        end
    end
    toc;
    
   [lefteye, righteye, timestamp, trigSignal] = tetio_readGazeData;
   
    numGazeData = size(lefteye, 2);
    leftEyeAll_odd= vertcat(leftEyeAll_odd, lefteye(:, 1:numGazeData));
    rightEyeAll_odd = vertcat(rightEyeAll_odd, righteye(:, 1:numGazeData));
    timeStampAll_odd = vertcat(timeStampAll_odd, timestamp(:,1));

    tetio_stopTracking;
       
    
end

%here is where I make something to make sure that thye are not missing any
%oddballs/pressing the key randomly, etc...

ListenChar(0);
% Stop playback:
PsychPortAudio('Stop', pahandle);

% Close the audio device:
PsychPortAudio('Close', pahandle);

disp('Program finished.');
clear Screen;

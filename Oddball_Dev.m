%% Oddball Task %%
% Plays tones in a constant stream, participant must detect presence of odd
% tone 

%%%IF YOU ARE DOING THIS TASK SEVERAL TIMES OVER, you can get the problem
%%%of an ever reducing number of trials, clear all if that problem comes
%%%up. 


function Oddball_Dev(outfile)
%% Unify Key Names
%KbCheck('UnifyKeyNames') 
%KbName('UnifyKeyNames') %keynames will match those on Mac OS-X operating sys
stopkey=KbName('escape');
spacebar = KbName('space');

%%%%%%%% PTB preliminaries %%%%%%%%%%%%%
PTBprelims


%%%% Sound Parameters %%%%

addpath('/Users/participant/desktop')%%change the stuff to the folder we want, remove from desktop
    
[lowsnd,lowF]=wavread('500.wav');
[highsnd,highF]=wavread('1000.wav');

InitializePsychSound()
pahandle=PsychPortAudio('Open',[],[],0,[],2);

ntrials = 10;
numhigh = ntrials/5;

cond_check=1;
ListenChar(2);
%for now a connection, take this out when Participant tester is complete
%tetio_CONNECT;

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
wehn=GetSecs +1;
%%%%%%%%introduce sounds
BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
   text='This is an introduction.'
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, text, (floor(horz/2)-100), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, win);
    flipTime = Screen('Flip', win);
    pause(1.8)

    BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
   text='When the task begins press any key on the keyboard when you hear a sound';
    
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, text, (floor(horz/2)-400), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, win);
    flipTime = Screen('Flip', win);
    pause(1.8)
    

BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
   text='The task will begin shortly';
    
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, text, (floor(horz/2)-200), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, win);
    flipTime = Screen('Flip', win);
    pause(3);
      


%display onscreen countdown
countdown


txt1='+'
Screen('TextSize', BlankScreen, 50);
   Screen('DrawText', BlankScreen, txt1, floor(horz/2), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, win);
    flipTime = Screen('Flip', win, when);

%%% Start the Task %%%

    
    
for i=1:length(oddtrialvec);
    tetio_startTracking;
    startSecs = tetio_localToRemoteTime(tetio_localTimeNow());
    tic;
    if oddtrialvec(i)==1;
    PsychPortAudio('DeleteBuffer')
    PsychPortAudio('FillBuffer', pahandle, highsnd');
    PsychPortAudio('SetLoop',pahandle);
    PsychPortAudio('Start',pahandle,2);
    sndtyp_odd(i)=1;
    else
    PsychPortAudio('DeleteBuffer')
    PsychPortAudio('FillBuffer', pahandle, lowsnd');
    PsychPortAudio('SetLoop',pahandle);
    PsychPortAudio('Start',pahandle,2); 
    sndtyp_odd(i)=2;
    end
    
    t = GetSecs;
    while GetSecs - t < 1.4;
        [keydown, secs]=KbCheck;
        if keydown ==1
            keyhit(i)=[tetio_localToRemoteTime(int64(secs))];
        end
    end
 
    
    tetio_stopTracking;
  
    [lefteye, righteye, timestamp, trigSignal] = tetio_readGazeData;
 
       
    %%%% save data each trial %%%%%%
%     data(i).lefteye = lefteye;
%     data(i).righteye = righteye;
%     data(i).timestamp = timestamp;
%     data(i).trig = trigSignal;
%     save(outfile,'data','task')
end

%here is where I make something to make sure that thye are not missing any
%oddballs/pressing the key randomly, etc...using sndtype_odd and keyhit to
%compare that there are no key presses during sndtype_odd==2

ListenChar(0);
% Stop playback:
PsychPortAudio('Stop', pahandle);

% Close the audio device:
PsychPortAudio('Close', pahandle);
% return the screen to dark
Screen('FillRect',win,[0 0 0],[]);
Screen('Flip',win);

disp('Program finished.');




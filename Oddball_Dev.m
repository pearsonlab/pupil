%% Oddball Task %%
% Plays tones in a constant stream, participant must detect presence of odd
% tone 
%% Unify Key Names
%KbCheck('UnifyKeyNames') 
%KbName('UnifyKeyNames') %keynames will match those on Mac OS-X operating sys
stopkey=KbName('escape');
spacebar = KbName('space');

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
    
[lowsnd,lowF]=wavread('500.wav');
[highsnd,highF]=wavread('1000.wav');

InitializePsychSound()
pahandle=PsychPortAudio('Open',[],[],0,[],1);

ntrials = 30;
numhigh = ntrials/5;

cond_check=1;

while cond_check==1;
   %%%% Randomization %%%%
oddtrialvec = zeros(length(ntrials),1);
oddtrialvec(randperm(ntrials,numhigh),1)=1;
% Run Length Code %

checkgood=[([oddtrialvec(diff(oddtrialvec) ~= 0)' oddtrialvec(end)]') (diff([0 find(diff(oddtrialvec) ~= 0)' length(oddtrialvec)])')];

%%checks to see if the vector is nice
b=checkgood(:,1)==0 & checkgood(:,2)< 2  
c=checkgood(:,1)==1 & checkgood(:,2) == 2 
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


%%% Start the Task %%%
for i= 1:length(oddtrialvec);
    
    [ch, when]=GetChar;
    
if oddtrialvect==1;
    PsychPortAudio('DeleteBuffer')
    PsychPortAudio('FillBuffer', pahandle, highsnd');
    PsychPortAudio('SetLoop',pahandle);
    PsychPortAudio('Start',pahandle,4);
    sndtype(ind)=1;
    keypress(i)=ch;
    WaitSecs(1)

else
    PsychPortAudio('DeleteBuffer')
    PsychPortAudio('FillBuffer', pahandle, lowsnd');
    PsychPortAudio('SetLoop',pahandle);
    PsychPortAudio('Start',pahandle,4); 
    sndtype(ind)=2;
    keypress(i)=ch;
    WaitSecs(1)
end
end

    

% Initialization Processes %







% Stop playback:
PsychPortAudio('Stop', pahandle);

% Close the audio device:
PsychPortAudio('Close', pahandle);
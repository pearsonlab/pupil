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

k=[oddtrialvec(diff(oddtrialvec) ~= 0)' oddtrialvec(end)]'; 

num=diff([0 find(diff(oddtrialvec) ~= 0)' length(oddtrialvec)])';
checkgood=[k num];

%%checks to see if the vector is nice
cont=1; 
while (cont==1)
for z=1:length(checkgood);
    if checkgood(z,1)==0 & checkgood(z,2)<2  || checkgood(z,1)==1 & checkgood(z,2) == 2 
        cond_check=1; cont=0; 
    else 
        cond_check=0;
    end
end
end
end
disp(oddtrialvec)

%%% Start the Task %%%
%%% Randomize when high tones happen %%%
for i= 1:length(oddtrialvec);
    
    [ch, when]=GetChar;
    
if oddtrialvect==1;
    PsychPortAudio('DeleteBuffer')
    PsychPortAudio('FillBuffer', pahandle, highsnd');
    PsychPortAudio('SetLoop',pahandle);
    PsychPortAudio('Start',pahandle,4);
    type(ind)=1;
    keypress(i)=ch;
    WaitSecs(1)

else
    PsychPortAudio('DeleteBuffer')
    PsychPortAudio('FillBuffer', pahandle, lowsnd');
    PsychPortAudio('SetLoop',pahandle);
    PsychPortAudio('Start',pahandle,4); 
    type(ind)=2;
    keypress(i)=ch;
    WaitSecs(1)
end
end

    

% Initialization Processes %







% Stop playback:
PsychPortAudio('Stop', pahandle);

% Close the audio device:
PsychPortAudio('Close', pahandle);
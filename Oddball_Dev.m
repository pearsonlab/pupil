%% Oddball Task %%
% Plays tones in a constant stream, participant must detect presence of odd
% tone 
%% Unify Key Names
%KbCheck('UnifyKeyNames') 
%KbName('UnifyKeyNames') %keynames will match those on Mac OS-X operating sys
stopkey=KbName('escape');
Rkey=KbName('rightarrow');
Lkey=KbName('leftarrow');

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
    
[lowsnd,lowF]=wavread('50.wav');
[highsnd,highF]=wavread('100.wav');

setup_audio;
InitializePsychSound;
pahandle = PsychPortAudio('Open', [], [], 0, freq);

%%% Randomize when high tones happen %%%

k = 

% Initialization Processes %


%%% Start the Task %%%
PsychPortAudio('DeleteBuffer')
PsychPortAudio('FillBuffer', pahandle, lowsnd');
PsychPortAudio('SetLoop',pahandle);
PsychPortAudio('Start',pahandle);

PsychPortAudio('DeleteBuffer')
PsychPortAudio('FillBuffer', pahandle, highsnd');
PsychPortAudio('SetLoop',pahandle);
PsychPortAudio('Start',pahandle);

% Stop playback:
PsychPortAudio('Stop', pahandle);

% Close the audio device:
PsychPortAudio('Close', pahandle);
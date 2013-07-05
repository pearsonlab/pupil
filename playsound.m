function playsound(handle,snd)
% play snd through handle using PsychPortAudio
% snd is a timepts x channels file
PsychPortAudio('DeleteBuffer')
PsychPortAudio('FillBuffer', handle, snd');
PsychPortAudio('SetLoop',handle);
PsychPortAudio('Start',handle,1);
%setup_audio.m
%initialize and ready playback using PTB's PsychAudio driver

InitializePsychSound()
pahandle=PsychPortAudio('Open',[],[],0); %the 0 is for reqlatency class
%need this to be 0 (def=1) so that it plays nicely and isn't aggressive
%about latency (since we don't need precise sound timing); setting this to
%1 causes weirdness in playback; this allows sound to be laggy on occasion,
%but results in no distortion
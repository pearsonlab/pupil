function pst(duration,outfile)
%duration is in seconds


% set up windows, etc.
PTBprelims

% count down to task
countdown

% paint blank screen
Screen('FillRect',win,[0 0 0],[]);
Screen('Flip',win);

tetio_startTracking;

WaitSecs(duration)

tetio_stopTracking;

% read and save data
[lefteye, righteye, timestamp, trigSignal] = tetio_readGazeData;
data.lefteye = lefteye;
data.righteye = righteye;
data.timestamp = timestamp;
data.trig = trigSignal;
save(outfile,'duration','data');

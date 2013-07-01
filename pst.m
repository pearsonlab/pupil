function pst(duration,outfile)

% set up windows, etc.
PTBprelims

% count down to task
countdown

% paint blank screen
Screen('FillRect',window,[0 0 0],[]);
Screen('Flip',window);

tetio_startTracking;

WaitSecs(duration)

data.gazedata = tetio_readGazeData;

tetio_stopTracking;
    

%tetio_cleanUp; %%%% not sure we need this: jmp

save(outfile,'duration','data');

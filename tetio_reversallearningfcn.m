function reversallearningfcn(outfile)
% code to perform reversal learning test
% saves data to outfile

%% Set up data files
global Partnum numtrial Partfile trialvec

%% Unify Key Names
 task = 'reversallearning'
KbName('UnifyKeyNames'); %keynames will match those on Mac OS-X operating sys


stopkey=KbName('escape');
Rkey=KbName('RightArrow');
Lkey=KbName('LeftArrow');

%%%%%%%% PTB preliminaries %%%%%%%%%%%%%
PTBprelims
try
%%%%%%%%%%%%%% Sound Parameters %%%%%%%%%%%%%
setup_audio
[popsnd,popF]=wavread('pop.wav');
[cashsnd,cashF]=wavread('cash.wav');

%create task vectors
revsightsound

% Trial vec is a row vector of 1's and 0's. Flag trial # in trialvec at which it switches between%
trialchange = find(diff(trialvec)~=0)+1;

% On-screen instructions
BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
   text='This the Reversal Learning Task. \n press any key to continue with the text'
    Screen('TextSize', BlankScreen, 20);
    [nx, ny, bbox] = DrawFormattedText(win, text, 'center', 'center', [255 255 255],'textbounds');
  Screen('FrameRect', win, 0, bbox)
    Screen('Flip',win);
    pause;

    BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
   text='Either the right or left arrow is correct. \n You will learn by trial and error.';
   Screen('TextSize', BlankScreen, 20);
   Screen('Textbounds',win)
    [nx, ny, bbox] = DrawFormattedText(win, text, 'center', 'center', [255 255 255],'textbounds');
  Screen('FrameRect', win, 0, bbox)
    Screen('Flip',win);
    pause;
    
 % Sound samples   
  for zed=mod(1:2,2)
    if zed==1
    pahandle=PsychPortAudio('Open',[],[],0,[],2);
    PsychPortAudio('DeleteBuffer')
    PsychPortAudio('FillBuffer', pahandle, cashsnd');
    PsychPortAudio('SetLoop',pahandle);
    PsychPortAudio('Start',pahandle,1);
     BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
   text='This is the result of pushing the correct arrow';
   Screen('TextSize', BlankScreen, 20);
    [nx, ny, bbox] = DrawFormattedText(win, text, 'center', 'center', [255 255 255]);
  Screen('FrameRect', win, 0, bbox)
    Screen('Flip',win);
    pause(2.5);
    
    else
         pahandle=PsychPortAudio('Open',[],[],0,[],2);
    PsychPortAudio('DeleteBuffer')
    PsychPortAudio('FillBuffer', pahandle, popsnd');
    PsychPortAudio('SetLoop',pahandle);
    PsychPortAudio('Start',pahandle,1);
     BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
   text='This is the result of pushing the incorrect arrow';
   Screen('TextSize', BlankScreen, 20);
    [nx, ny, bbox] = DrawFormattedText(win, text, 'center', 'center', [255 255 255]);
  Screen('FrameRect', win, 0, bbox)
    Screen('Flip',win);
    pause(2.5);
    end
  end

    BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
   text='You gain points by pushing the correct arrow in each round. \n Listen to the sounds to determine whether your arrow choice is correct.';
   Screen('TextSize', BlankScreen, 20);
    [nx, ny, bbox] = DrawFormattedText(win, text, 'center', 'center', [255 255 255]);
  Screen('FrameRect', win, 0, bbox)
    Screen('Flip',win);
    pause;  
  
%display onscreen countdown
countdown

%%%%%%%% Start the Task %%%%%%%%%%%%%%%%%%%%%


WaitSecs(0.5);
presstime=[];%%empty matrix
soundtime=[];

pressvec = zeros(1, length(trialvec));
for ind = 1:length(trialvec)
    
    tetio_startTracking;
    
    WaitSecs(.5);
    
    timertrialstart(ind) = uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
    
    % paint on screen stimulus
   txt1='+';
     Screen('TextSize', BlankScreen, 100);
    [nx, ny, bbox] = DrawFormattedText(win, txt1, 'center', 'center', [255 255 255]);
  Screen('FrameRect', win, 0, bbox)
    Screen('Flip',win);
    
    
    % Wait for response
    press = 0;
    while press == 0  
        [secs, KeyCode] = KbWait(-1);
    if (find(KeyCode)==39)%they chose right
        data(ind).presstime=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
        pressvec(ind) = 0;
        press = 1;
    elseif (find(KeyCode)==37) %they chose left
        data(ind).presstime=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
	    pressvec(ind) = 1;
        press =2;
    elseif find(KeyCode)==41 %they chose esc to bail out
        data(ind).presstime=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
	    pressvec(ind) = 2;
        press = 3;
	    %Screen('Closeall')
	    return
    end
    end
    
    
    if pressvec(ind) == trialvec(ind);
        PsychPortAudio('DeleteBuffer');
        PsychPortAudio('FillBuffer',pahandle,cashsnd');
        PsychPortAudio('SetLoop',pahandle);
        PsychPortAudio('Start',pahandle);
        data(ind).soundtime=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
    %tell that cashsound happened
        sndplay(ind) = 1 % Record 'cash'
    elseif pressvec(ind) ~= trialvec(ind)
        PsychPortAudio('DeleteBuffer')
        PsychPortAudio('FillBuffer',pahandle,popsnd');
        PsychPortAudio('SetLoop',pahandle);
        PsychPortAudio('Start',pahandle);
        data(ind).soundtime=uint64(tetio_localToRemoteTime(tetio_localTimeNow()));
      % tell that pop happened
        sndplay(ind) = 2 % Record 'pop'
    end
    
    %blank screen between each key press
    Screen('FillRect',win, [0 0 0]);
    Screen('Flip',win);
    WaitSecs(0.5);
    
    tetio_stopTracking;
    
    %read eye data
    [lefteye, righteye, timestamp, trigSignal] = tetio_readGazeData;

   %%%% save data each trial %%%%%%
    data(ind).lefteye = lefteye;
    data(ind).righteye = righteye;
    data(ind).timestamp = timestamp;
    data(ind).trig = trigSignal;
    data(ind).presstime = presstime;
    data(ind).soundtime = soundtime;
    save(outfile,'data','task')
     
end

% reversalmat = [soundtime' presstime'];

%%% Save Data to File %%%


%end

catch q
     ShowCursor
     sca
     keyboard
 end
 
% return the screen to dark
Screen('FillRect',win,[0 0 0],[]);
Screen('Flip',win);

disp('Program finished.');
end

% %% Chose where to end up
% 
% %cd(startdir) % Directory we started in
% cd(datafile) % Directory in which we save light test data

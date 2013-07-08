%paint fixation cross onscreen
PTBprelims;
txt1='+';
Screen('TextSize', BlankScreen, 100);
DrawFormattedText(win, txt1, 'center', 'center', [200 200 200]);
Screen('Flip',win);
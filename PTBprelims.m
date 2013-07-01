% PTBprelims.m
% helper script to go find open psychtoolbox windows and either get
% dimensions or initialize

which_screen = 1;

% if PTB isn't already running, open a window
windowPtrs = Screen('Windows');
if isempty(windowPtrs)
    %which screen do we display to?
    [win, screenRect] = Screen('OpenWindow',which_screen,[0 0 0],[],32);
else
    win = windowPtrs(which_screen);
    screenRect = Screen('Rect',win);
end
horz=screenRect(3);
vert=screenRect(4);
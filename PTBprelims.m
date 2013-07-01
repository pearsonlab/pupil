% PTBprelims.m
% helper script to go find open psychtoolbox windows and either get
% dimensions or initialize

%%%%%%%% PTB preliminaries %%%%%%%%%%%%%
warning('off','MATLAB:dispatcher:InexactMatch');
Screen('Preference', 'SkipSyncTests',2); %disables all testing -- use only if ms timing is not at all an issue
Screen('Preference','VisualDebugLevel', 0);
Screen('Preference', 'SuppressAllWarnings', 1);

% if PTB isn't already running, open a window
windowPtrs = Screen('Windows');
if isempty(windowPtrs)
    %which screen do we display to?
    which_screen=1;
    [win, screenRect] = Screen('OpenWindow',which_screen,[0 0 0],[],32);
else
    win = windowPtrs(1);
    screenRect = Screen('Rect',win);
end
horz=screenRect(3);
vert=screenRect(4);
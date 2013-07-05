function display_instructions(win, text)
% display onscreen instructions on window win using PTB
% text is a cell array of instructions, each of which is displayed on a
% single screen
% on each screen, the subject must press a key to continue

BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
Screen('TextSize', BlankScreen, 20);

for ind = 1:length(text)
    [~, ~, bbox] = DrawFormattedText(win, text, 'center', 'center', [255 255 255],'textbounds');
%    Screen('FrameRect', win, 0, bbox)
    Screen('Flip',win);
    pause;
end

% return the screen to dark
Screen('FillRect',win,[0 0 0],[]);
Screen('Flip',win);

function display_instructions(win, text, nowait)
% display onscreen instructions on window win using PTB
% text is a cell array of instructions, each of which is displayed on a
% single screen
% on each screen, the subject must press a key to continue unless nopause=1

if ~exist('nowait','var')
    nowait = 0;
end

if ~iscell(text)
    text = {text};
end

BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
Screen('TextSize', BlankScreen, 20);

for ind = 1:length(text)
    DrawFormattedText(win, text{ind}, 'center', 'center', [70 70 70],'textbounds');
    Screen('Flip',win);
    if ~nowait
        pause;
    end
end

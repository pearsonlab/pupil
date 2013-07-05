function [resp, T] = handle_input(livekeys)
%livekeys are keyboard codes (as returned by KbName) for which PTB should
%return input

while 1
    [T, respvec] = KbStrokeWait();
    resp = find(respvec);
    if ismember(resp, livekeys)
        return
    end
end
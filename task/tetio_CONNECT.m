%% CONNECT TO TOBII TRACKER

% *************************************************************************
%
% Initialization and connection to the Tobii Eye-tracker
%
% *************************************************************************

try %see if we're already connected
    currentFrameRate = tetio_getFrameRate;
catch
    % Set to tracker ID to the product ID of the tracker you want to connect to.
    trackerId = 'TT060-301-14200895';
    
    fprintf('Connecting to tracker "%s"...\n', trackerId);
    tetio_connectTracker(trackerId);
    
    currentFrameRate = tetio_getFrameRate;
    fprintf('Frame rate: %d Hz.\n', currentFrameRate);
end

%% sync. the clocks

WaitSecs(1); %to make sure everything is okay before checking clock sync

%%look for synchronization

sync = tetio_clockSyncState;

if sync == 0
    warning('tetio_clocksyncfalse' , 'Clocks are not synchronized');
    disp('Clocks are not synchronized');
end




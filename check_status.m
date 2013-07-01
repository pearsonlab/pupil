%% check for valid connection to Tobii
% Check clock synchronization
% Check connection status

tetio_init();

tracker_status = tetio_getTrackers;
good = {'ok'};

goodstatus = strcmp(tracker_status.Status,good);
        
if goodstatus ~= 1
    disp('Connection not valid')
    error('check_status has failed - tracker is not connected')
else
    sync_state = tetio_clockSyncState();
    if sync_state ~= 1
        disp('Sync not valid')
        error('check_status has failed - clocks are not synched')
    end
end

    

    
       
        
   
    

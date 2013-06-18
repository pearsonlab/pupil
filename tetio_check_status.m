%% check for valid connection to Tobii
% Check clock synchronization
% Check connection status

sync_state = tetio_clockSyncState();

tracker_status = tetio_getTrackers;
good = {'ok'};

goodstatus= strcmp(tracker_status(6),good);
        
if sync_state ~= 1 || goodstatus ~= 1
    disp('Connection not valid')
    error('check_status has failed - either time is not synched or tracker is not connected')
    
    
    
       
        
   
    

% CONNECT TO TOBII

%the following is a kludge needed because, even though it's in the path,
%matlab has trouble loading a certain dylib file if we don't call the mex
%from that directory
startdir=pwd;
addpath('~/t2t/lib/')
addpath('~/t2t/lib/matlab')
cd('~/t2t/lib/')

% intialize command variables
 hostName = '169.254.7.52'; % psych retrieved by jmp 8-1-12
%hostName = '169.254.7.31'; % fuqua 
portName = '4455';

[status,history] = talk2tobii('GET_STATUS'); %%tetio_getTrackers()
if status(2) == 1
	display('tobii already connected');
	return
    cd(startdir)
end

%% try to connect to the eyeTracker
talk2tobii('CONNECT',hostName, portName);  %%tetio_connectTracker(productID)


%check status of Tobii connection
cond_res = check_status(2, 20, 1, 1); % see if tobii is connected, wait 30 sec, 1 sec intervals, for code 1 in slot 2 (connected)
tmp = find(cond_res==0);
if( ~isempty(tmp) )
	display('tobii unable to connect');
    cd(startdir);
	return
end

%change back to start directory
cd(startdir)


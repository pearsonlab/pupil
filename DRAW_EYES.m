% ASSUMES THAT PTB-3 HAS AN OPEN WINDOW (handleName = window)
% DRAW_EYES calls DrawEyes, but includes checks on tobii status and open PTB-windows
% needs to be tested, but code does not assume tobii is connected
	% if connected, recording/tracking left on
	% if not connected, tracking turned of for DrawEyes, then turned off before leaving

%find indices for correspond keys
ESCAPE=KbName('Escape');

% CHECK FOR OPEN PTB-3 WINDOWS
openWindows = Screen('Windows');
if (isempty(openWindows))
	display('PTB-3 window not open: cannot use DrawEyes');
	clear 'openWindows'
	return
end
clear 'openWindows'

% CHECK FOR TOBII CONNECTION
cond_res = check_status(2, 10, 1, 1); % check slot 2 (connected), wait 10 seconds max, in 1 sec intervals.
tmp = find(cond_res==0, 1);
if( ~isempty(tmp) )
	display('tobii not connected');
	return
end

if ~ exist('ifi','var')
	ifi = Screen('GetFlipInterval',window,100);
end



[status,history] = talk2tobii('GET_STATUS');

started_with_tracking_off = 0;
if ( status(7) == 0 ) % status slot 7 corresponds to recording

	started_with_tracking_off = 1;
	%% monitor/find eyes
	talk2tobii('START_TRACKING');

	%check status of Tobii connection
	cond_res = check_status(7, 30, 1, 1);
	tmp = find(cond_res==0, 1);
	if( ~isempty(tmp) )
		display('failed to start tracking');
		return
	end

end


flagNotBreak = 0;
disp('Press Esc to stop DRAW_EYES');
while ~flagNotBreak
	eyeTrack = talk2tobii('GET_SAMPLE');
	DrawEyes(window, eyeTrack(9), eyeTrack(10), eyeTrack(11), eyeTrack(12), eyeTrack(8), eyeTrack(7));

	if( IsKey(ESCAPE) )
		flagNotBreak = 1;
		if( flagNotBreak )
			break;
		end
	end
end

if started_with_tracking_off
	WaitSecs(0.5);
	talk2tobii('STOP_TRACKING');
	WaitSecs(0.5);
end

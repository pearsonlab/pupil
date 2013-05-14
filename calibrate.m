%jmp modified eye calibration routine for Tobii
%based on David Paulsen's version
%first created 8-1-12
startdir = pwd;
addpath /Users/participant/t2t/lib/

%%%%%%%% PTB preliminaries %%%%%%%%%%%%%
warning('off','MATLAB:dispatcher:InexactMatch');
Screen('Preference', 'SkipSyncTests',2); %disables all testing -- use only if ms timing is not at all an issue
Screen('Preference','VisualDebugLevel', 0);
Screen('Preference', 'SuppressAllWarnings', 1);
Screen('CloseAll')
%HideCursor; % turn off mouse cursor

%which screen do we display to?
which_screen=1;

%open window, blank screen
[window, screenRect] = Screen('OpenWindow',which_screen,[0 0 0],[],32);
horz=screenRect(3);
vert=screenRect(4);

%connect to Tobii
CONNECT

% CHECK FOR TOBII CONNECTION
cond_res = check_status(2, 10, 1, 1); % check slot 2 (connected), wait 10 seconds max, in 1 sec intervals.
tmp = find(cond_res==0, 1);
if( ~isempty(tmp) )
	display('tobii not connected');
	return
end


% calibration points in [X,Y] coordinates; [0, 0] is top-left corner
pos = [0.2 0.2;...
    0.5 0.2;
    0.8 0.2;
    0.2 0.5;
    0.5 0.5;
    0.8 0.5;
    0.2 0.8;
    0.5 0.8;
    0.8 0.8];
numpoints = size(pos,1);
pos=pos(randperm(numpoints),:); %shuffle calibration point order

if ~ exist('ifi','var')
	ifi = Screen('GetFlipInterval',window,100);
end

%need to add input of subject number
if ( exist('subjectNumber', 'var') )
	calFileName = ['./calibrations/', num2str(subjectNumber), '.cal'];
else
	calFileName = './calibrations/generic.cal';
end

%countdown to start of calibration stims
for (i = 1:4);
    
    when = GetSecs + 1;
    
    % PRESENT STARTING Screen
    BlankScreen = Screen('OpenOffScreenwindow', window,[0 0 0]);
    if i == 4
       txt = ''; 
    else
        txt = num2str(4-i);
    end
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, txt, floor(horz/2), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, window);
    flipTime = Screen('Flip', window, when);
end





%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%							START CALIBRATION
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%display stimulus in the four corners of the screen
totTime = 4;        % swirl total display time during calibration
n_samples_per_pnt = 16;
calib_not_suc = 1;
while calib_not_suc
	% TALK2TOBII('START_CALIBRATION', calib_pnts, clear_prev, n_samples, [,filename]);
	talk2tobii('START_CALIBRATION', pos, 1, n_samples_per_pnt);
	%talk2tobii('START_CALIBRATION', pos, 1,n_samples_per_pnt,calFileName);
	%had trouble with previous line (writing to file)
	WaitSecs(0.5);
	%% It is wrong to try to check the status here because the
	%% eyetracker waits for an 'ADD_CALIBRATION_POINT' and 'DREW_POINT'.

	for i=1:numpoints
		position = pos(i,:);
		% disp(position);
		when0 = GetSecs()+ifi;
		talk2tobii('ADD_CALIBRATION_POINT');
		StimulusOnsetTime = swirl(window, totTime, ifi, when0, position, 1);
		talk2tobii('DREW_POINT');
		WaitSecs(0.5);    
	end
	
	cond_res = check_status(11, 90, 1, 1); % check slot 11 (calibration finished), wait 90 seconds, check in 1 sec intervals, for code 1)
	tmp = find(cond_res==0, 1);
	if( ~isempty(tmp) )
		display('calibration failed');
		error('check_status has failed- CALIBRATION');
	end

	%check quality of calibration
	quality = talk2tobii('CALIBRATION_ANALYSIS');
    quality(:,5)=sign(quality(:,5)); %kludge added by JMP because returned values were outlandisly high 10-24-12
    quality(:,8)=sign(quality(:,8));
    cd(startdir)

	% check the quality of the calibration
	left_eye_used = find(quality(:,5) == 1);
	left_eye_data = quality(left_eye_used, 1:4);
	right_eye_used = find(quality(:,8) == 1);
	right_eye_data = quality(right_eye_used, [1,2,6,7]);
	
	fig = figure('Name','CALIBRATION PLOT');
	scatter(left_eye_data(:,1), left_eye_data(:,2), 'ok', 'filled');
	axis([0 1 0 1]);		
	hold on
	scatter(right_eye_data(:,1), right_eye_data(:,2), 'ok', 'filled');
	scatter(left_eye_data(:,3), left_eye_data(:,4), '+g');
	scatter(right_eye_data(:,3), right_eye_data(:,4), 'xb');		
	
    cont = 1;
    while (cont == 1)
        tt= input('enter "R" to retry calibration or "C" to continue to testing\n','s');
        
        if ( strcmpi(tt,'R') || strcmpi(tt,'r') )
            cont = 0; calib_not_suc = 1;
        elseif ( strcmpi(tt,'C') || strcmpi(tt,'c') )
            cont = 0; calib_not_suc = 0;
        end
        
    end
    % close figure if still open, if not, nothing (attempts to close nonhandle returns error)
    if ishghandle(fig); close(fig);end
        
    
end % END CALIBRATION
disp('End Of Calibration');
Screen('CopyWindow', BlankScreen, window);
flipTime = Screen('Flip', window);
cd(startdir)
%DISCONNECT -- don't disconnect, or calibration will be lost?!
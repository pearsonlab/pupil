%%jmp modified eye calibration routine for Tobii
%based on David Paulsen's version
%first created 8-1-12
startdir = pwd;



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
[win, screenRect] = Screen('OpenWindow',which_screen,[0 0 0],[],32);
horz=screenRect(3);
vert=screenRect(4);

%connect to Tobii


% *************************************************************************
%
% Initialization and connection to the Tobii Eye-tracker
%
% *************************************************************************

tetio_CONNECT;


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
	ifi = Screen('GetFlipInterval',win,100);
end

%need to add input of subject number
if ( exist('subjectNumber', 'var') )
	calFileName = ['./calibrations/', num2str(subjectNumber), '.cal'];
else
	calFileName = './calibrations/generic.cal';
end


WaitSecs(0.2)
%countdown to start of calibration stims
for (i = 1:4);
    
    when = GetSecs + 1;
    
    % PRESENT STARTING Screen
    BlankScreen = Screen('OpenOffScreenwindow', win,[0 0 0]);
    if i == 4
       txt = ''; 
    else
        txt = num2str(4-i);
    end
    Screen('TextSize', BlankScreen, 20);
    Screen('DrawText', BlankScreen, txt, floor(horz/2), floor(vert/2), [255 255 255], [0 0 0], 1);
    Screen('CopyWindow', BlankScreen, win);
    flipTime = Screen('Flip', win, when);
end




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%							START CALIBRATION
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%display stimulus in the four corners of the screen

[win, screenRect] = Screen('OpenWindow',which_screen,[0, 0, 0],[],32);

	%%check for time sync. (put into checkstatus)
   
    
totTime = 4;        % swirl total display time during calibration
n_samples_per_pnt = 16;
calib_not_suc = 1;


while calib_not_suc==1;
	
	tetio_startCalib;
    
WaitSecs(0.5)

	for i=1:numpoints;
		position = pos(i,:);
		disp(position);
		when0 = GetSecs()+ifi; 
		StimulusOnsetTime = tetio_swirl(win, totTime, ifi, when0, position, 0);
        tetio_addCalibPoint(pos(i,1), pos(i,2))
        WaitSecs(0.5);
        
   
    end

    
    
%% organizes Data to an easier to read format

quality = tetio_getCalibPlotData;

%Data organization

quality = quality';

%%% Organize data %%%
a = [1 2 3 4 5 6 7 8];
a = a';
organizevector = repmat(a, ((length(quality))/8), 1);
organized_quality = horzcat(quality, organizevector);

trueXpos=find(organized_quality(:,2)==1);
True_X=organized_quality((trueXpos),1);

trueYpos=find(organized_quality(:,2)==2);
True_Y=organized_quality((trueYpos),1);

leftXpos=find(organized_quality(:,2)==3);
Left_X=organized_quality((leftXpos),1);

leftYpos=find(organized_quality(:,2)==4);
Left_Y=organized_quality((leftYpos),1);

leftstat=find(organized_quality(:,2)==5);
Left_Status=organized_quality((leftstat),1);

rightXpos=find(organized_quality(:,2)==6);
Right_X=organized_quality((rightXpos),1);

rightYpos=find(organized_quality(:,2)==7);
Right_Y=organized_quality((rightYpos),1);

rightstat=find(organized_quality(:,2)==8);
Right_Status=organized_quality((rightstat),1);

CalibrationData=[True_X True_Y Left_X Left_Y Left_Status Right_X Right_Y Right_Status];      

%%% 
%%% check the quality of the calibration %%%
	left_eye_used = find(CalibrationData(:,5) == 1);
	left_eye_data = CalibrationData(left_eye_used, 1:4);
	right_eye_used = find(CalibrationData(:,8) == 1);
	right_eye_data = CalibrationData(right_eye_used, [1,2,6,7]);
	
	fig = figure('Name','CALIBRATION PLOT'); 
	scatter(left_eye_data(:,1), left_eye_data(:,2), 'ok', 'filled');
	axis([0 1 0 1]);		
	hold on
	scatter(right_eye_data(:,1), right_eye_data(:,2), 'ok', 'filled');
	scatter(left_eye_data(:,3), left_eye_data(:,4), '+g');
	scatter(right_eye_data(:,3), right_eye_data(:,4), 'xb');
   
  
    %asks if the calibration was good or not
    cont = 1;
    while (cont == 1)
        tt= input('enter "R" to retry calibration or "C" to continue to testing\n','s');
        
        if ( strcmpi(tt,'R') || strcmpi(tt,'r') )
            cont = 0; calib_not_suc = 1;
            tetio_stopCalib;
        elseif ( strcmpi(tt,'C') || strcmpi(tt,'c') )
            cont = 0; calib_not_suc = 0;
       try
        tetio_computeCalib;
    catch q     
        end
        
    end
    
end    
    
    
        disp('give up?')
    end
    
 tetio_stopCalib;

disp('End Of Calibration');
Screen('CopyWindow', BlankScreen, win);
flipTime = Screen('Flip', win);
cd(startdir)
%DISCONNECT -- don't disconnect, or calibration will be lost?!

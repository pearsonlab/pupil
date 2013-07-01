function [errcode, calibdata] = calibrate(numpts, outfile)
%perform Tobii calibration routine
% INPUTS:
% numpts: number of calibration points to use
% OUTPUTS:
% errcode = 0 (calibration worked), 1 (something went wrong)
% caldata: calibration data to be saved to file

%based on David Paulsen's version
%modded jmp 8-1-12 and thereafter
%switched to tobii sdk summer 2013

%%%%%%%% PTB preliminaries %%%%%%%%%%%%%
PTBprelims


% *************************************************************************
%
% Initialization and connection to the Tobii Eye-tracker
%
% *************************************************************************

tetio_CONNECT;

addpath('/Applications/tobiiSDK/matlab/EyeTrackingSample');
addpath('/Applications/tobiiSDK/matlab/tetio');
addpath('/matlab/pupil');

% calibration points in [X,Y] coordinates; [0, 0] is top-left corner
pos = [0.2 0.2;
    0.5 0.2;
    0.8 0.2;
    0.2 0.5;
    0.5 0.5;
    0.8 0.5;
    0.2 0.8;
    0.5 0.8;
    0.8 0.8];

% define some special subsets of pts
switch numpts
    case {1, 2, 3}
        disp('Warning! Calibrating with fewer than four points may result in poor calibration!')
    case 4
        idx = [1 3 7 9]; % 4-point calibration uses corners
    case 5
        idx = [1 3 5 7 9]; % 5-pt calibration uses corners + center
    case 6
        idx = [1 2 3 7 8 9]; % 6-pt calibration uses top and bottom rows
    otherwise
        idx = randperm(size(pos,1),numpts); % get a random subset of points
end

idx = Shuffle(idx); %randomize point order
pos = pos(idx,:); %take only points we need

if ~ exist('ifi','var')
    ifi = Screen('GetFlipInterval',win,100);
end

%display onscreen countdown
countdown

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%							START CALIBRATION
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
totTime = 2;        % swirl total display time during calibration
calibdone = 0;

while ~calibdone
    
    tetio_startCalib; %tell eyetracker we want to start calibration
    
    WaitSecs(0.5);
    
    %loop over calibration points
    for i = 1:numpts 
        position = pos(i,:);
        %disp(position);
        when0 = GetSecs()+ifi;
        swirl(win, totTime, ifi, when0, position);
        tetio_addCalibPoint(pos(i,1), pos(i,2));
        WaitSecs(0.2);
    end
    
    try
        calibdata = tetio_computeCalib;
    catch q
        errcode = 1;
        calibdata = q; %return error info as calibration data
    end
    
    
    %blank screen
    Screen('CopyWindow', BlankScreen, win);
    Screen('Flip', win);
    
    %% organizes Data to an easier to read format
    
    quality = tetio_getCalibPlotData;
    CalibrationData = reshape(quality,8,[])'; %reshape into 8-column matrix
    
    %%% Organize data %%%
%     a = [1 2 3 4 5 6 7 8];
%     a = a';
%     organizevector = repmat(a, ((length(quality))/8), 1);
%     organized_quality = horzcat(quality, organizevector);
%     
%     trueXpos=find(organized_quality(:,2)==1);
%     True_X=organized_quality((trueXpos),1);
%     
%     trueYpos=find(organized_quality(:,2)==2);
%     True_Y=organized_quality((trueYpos),1);
%     
%     leftXpos=find(organized_quality(:,2)==3);
%     Left_X=organized_quality((leftXpos),1);
%     
%     leftYpos=find(organized_quality(:,2)==4);
%     Left_Y=organized_quality((leftYpos),1);
%     
%     leftstat=find(organized_quality(:,2)==5);
%     Left_Status=organized_quality((leftstat),1);
%     
%     rightXpos=find(organized_quality(:,2)==6);
%     Right_X=organized_quality((rightXpos),1);
%     
%     rightYpos=find(organized_quality(:,2)==7);
%     Right_Y=organized_quality((rightYpos),1);
%     
%     rightstat=find(organized_quality(:,2)==8);
%     Right_Status=organized_quality((rightstat),1);
%     
%     CalibrationData=[True_X True_Y Left_X Left_Y Left_Status Right_X Right_Y Right_Status];

    %%% check the quality of the calibration %%%
    left_eye_used = CalibrationData(:,5) == 1;
    left_eye_data = CalibrationData(left_eye_used, 1:4);
    right_eye_used = CalibrationData(:,8) == 1;
    right_eye_data = CalibrationData(right_eye_used, [1,2,6,7]);
    
    figure('Name','CALIBRATION PLOT');
    scatter(left_eye_data(:,1), left_eye_data(:,2), 'ok', 'filled');
    axis([0 1 0 1]);
    hold on
    scatter(right_eye_data(:,1), right_eye_data(:,2), 'ok', 'filled');
    scatter(left_eye_data(:,3), left_eye_data(:,4), '+g');
    scatter(right_eye_data(:,3), right_eye_data(:,4), 'xb');
    
    keyboard
    
    %asks if the calibration was good or not
    while 1
        tt = input('Enter "R" to retry calibration or "C" to confirm calibration: ','s');
        
        switch lower(tt)
            case 'r'             
                break
            case 'c'
                calibdone = 1;
                break
        end
    end
    
end

tetio_stopCalib;

save(outfile,'numpts','calibdata')

disp('End Of Calibration');
Screen('CopyWindow', BlankScreen, win);
Screen('Flip', win);
function [errcode, CalibrationData] = calibrate(numpts, outfile)
%perform Tobii calibration routine
% INPUTS:
% numpts: number of calibration points to use
% OUTPUTS:
% errcode = 0 (calibration worked), 1 (something went wrong)
% caldata: calibration data to be saved to file

%based on David Paulsen's version
%modded jmp 8-1-12 and thereafter
%switched to tobii sdk summer 2013

errcode = 0;

%%%%%%%% PTB preliminaries %%%%%%%%%%%%%
PTBprelims


% *************************************************************************
%
% Initialization and connection to the Tobii Eye-tracker
%
% *************************************************************************

tetio_CONNECT;

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
    
    %blank screen
    Screen('CopyWindow', BlankScreen, win);
    Screen('Flip', win);
    
    WaitSecs(1); %let Tobii catch up
    
    try
        tetio_computeCalib;
        quality = tetio_getCalibPlotData;
        CalibrationData = reshape(quality,8,[])'; %reshape into 8-column matrix
    catch q
        errcode = 1;
        CalibrationData = []; %return error info as calibration data
    end

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

save(outfile,'numpts','CalibrationData')

disp('End Of Calibration');
Screen('CopyWindow', BlankScreen, win);
Screen('Flip', win);
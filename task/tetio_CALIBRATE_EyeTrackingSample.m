% *************************************************************************
%
% Calibration of a participant
%
% *************************************************************************

global Calib

screensize = get(0,'Screensize');
Calib.mondims1.x = screensize(1);
Calib.mondims1.y = screensize(2);
Calib.mondims1.width = screensize(3);
Calib.mondims1.height = screensize(4);

Calib.MainMonid = 1; 
Calib.TestMonid = 1;

Calib.points.x = [0.1 0.9 0.5 0.9 0.1];  % X coordinates in [0,1] coordinate system 
Calib.points.y = [0.1 0.1 0.5 0.9 0.9];  % Y coordinates in [0,1] coordinate system 
Calib.points.n = size(Calib.points.x, 2); % Number of calibration points
Calib.bkcolor = [0.85 0.85 0.85]; % background color used in calibration process
Calib.fgcolor = [0 0 1]; % (Foreground) color used in calibration process
Calib.fgcolor2 = [1 0 0]; % Color used in calibratino process when a second foreground color is used (Calibration dot)
Calib.BigMark = 25; % the big marker 
Calib.TrackStat = 25; % 
Calib.SmallMark = 7; % the small marker
Calib.delta = 200; % Moving speed from point a to point b
Calib.resize = 1; % To show a smaller window
Calib.NewLocation = get(gcf,'position');




disp('Starting TrackStatus');
% Display the track status window showing the participant's eyes (to position the participant).
tetio_TrackStatus; % Track status window will stay open until user key press.
disp('TrackStatus stopped');
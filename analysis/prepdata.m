% prepdata.m
% loads data in from file and munges it
% makes left and right eye data, mean of the two, and time axis

load(fullfile(newdir, dfile))

% munge data
lpup = cleanseries(eyedata.lefteye(:, 12));
rpup = cleanseries(eyedata.righteye(:, 12));
mpup = nanmean([lpup; rpup]);
pupil = mpup;

% get timestamps: convert microseconds to seconds
t0 = min(eyedata.timestamp);
taxis = us2secs(eyedata.timestamp, t0);
sr = 60;  % sampling rate of Tobii = 60 Hz
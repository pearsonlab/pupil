% prepdata.m
% loads data in from file and munges it
% makes left and right eye data, mean of the two, and time axis

clear task  % since not all files contain this variable, and we may need to infer from scratch

load(fullfile(newdir, dfile))

if ~exist('task','var')
    splitstr = regexp(dfile,'\.','split');
    task = splitstr{3};
end

% munge data
try
    lpup = cleanseries(eyedata.lefteye(:, 12));
    rpup = cleanseries(eyedata.righteye(:, 12));
    
    % get initial timestamp, convert microseconds to seconds
    t0 = min(eyedata.timestamp);
    taxis = us2secs(eyedata.timestamp, t0);
catch
    lpup = cleanseries(data.lefteye(:, 12));
    rpup = cleanseries(data.righteye(:, 12));
    t0 = min(data.timestamp);
    taxis = us2secs(data.timestamp, t0);
end
mpup = nanmean([lpup rpup], 2);
pupil = mpup;

sr = 60;  % sampling rate of Tobii = 60 Hz
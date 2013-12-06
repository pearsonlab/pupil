function out = cleanseries(data)
% performs data cleaning (replacing bad/missing data with nan) for tobii
% gaze data

data = data(:); %columnify


N = length(data);
bad = (data == -1); %points with invalid data

% now, remove places where the eye trace is highly discontinuous
dd = [0 ; diff(data)]; %high-pass filter
sig = median(abs(dd))/norminv(0.75); %robust estimator of standard deviation of dd
th = 5; %number of standard deviations to set as threshold
disc = abs(dd) > th * sig; %need to add 0 because diff has 

% lastly, remove isolated points
to_remove = find(bad | disc); %either bad data or discontinuous
% get all points that are one to the right of future NaNs and one to the
% left of future NaNs
isolated = intersect(to_remove+1, to_remove-1);

% combine
allbad = union(to_remove,isolated);

% remove data
newdat = data;
newdat(allbad) = NaN; %remove data

%now interpolate
goodinds = find(~isnan(newdat));
if isempty(goodinds)
    warning('Not enough good data to clean. Aborting.')
    out = nan(size(data));
else
    out = interp1(goodinds, newdat(~isnan(newdat)), 1:N,'linear','extrap');
end

% for definiteness, return a column vector
out = out(:);








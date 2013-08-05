%%%%% This function organizes data.%%%%%
% Output "outdat" is a struct containing left, right, average, leftnorm,
% rightnorm, and averagenorm.
% Output "datamat" is matrix containing 4 columns of data sequentially 
% concatenated: lefteye, righteye, timestamp, and average.
% Output "srtbins" finds bin # containing event.

function [outdat,trialvec,srtbins,testdata,datamat] = dataorg(data,testdata,task,trialvec)

% Find either sound or onscreen stimuli onset bins.
[~,srtbins] = findevents(testdata,data,task);

% Make matrix of L, R, timestamp, avg. L and R
[datamat] = makemat(testdata);

% Convert datamat time --> seconds.
[datamat] = makesecs(datamat);

% Make struct of chopped data called 'outdat'.
[outdat] = evtsplit2(srtbins,task,datamat);

% Normalize data to create normalized data within struct.
[outdat] = normdat(srtbins,0.2,60,outdat,datamat);

end
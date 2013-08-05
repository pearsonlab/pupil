%%%%% This function organizes data.

function [outdat,trialvec,srtbins,testdata,whicheye,datamat] = dataorg(data,testdata,task,trialvec,whicheye,twoeye)

% Find either sound or onscreen stimuli onset bins.
[~,srtbins] = findevents(testdata,data,task);

% Make matrix of L, R, timestamp, avg. L and R
[datamat] = makemat(testdata);

% Convert datamat time --> seconds.
[datamat] = makesecs(datamat);

% Find # bins before/after, make matrix of chopped data called 'outdat'
%[outdat,outdat2,whicheye] = evtsplit(srtbins,task,datamat,whicheye,twoeye,norm);
[outdat] = evtsplit2(srtbins,task,datamat);

% Normalize 
 [outdat] = normdat(srtbins,0.2,60,outdat,datamat);

% Plot raw data (avg. right and left eye)
plotraw(datamat,whicheye,twoeye);

end